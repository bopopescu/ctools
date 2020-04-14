# This script needs to run from undercloud as stack user after sourcing stackrc
# Usage: python testbed_generator_rhosp.py --overcloudrc overcloudrc

import subprocess
import argparse
import json
import re
import os
import sys
from neutronclient.neutron import client as neutron_client
from novaclient import client as nova_client
from keystoneclient.v2_0 import client as ks_client
from ironicclient import client as ironic_client
from collections import defaultdict
import ast
class Openstack(object):
    def __init__(self, auth_url, username, password, tenant, auth_token=None):
        ''' Get keystone client obj '''
        self.keystone = ks_client.Client(username=username,
                                         password=password,
                                         tenant_name=tenant,
                                         auth_url=auth_url,
                                         insecure=True)
        ''' Get nova client handle '''
        self.nova = nova_client.Client('2',
                                       auth_url=auth_url,
                                       username=username,
                                       api_key=password,
                                       project_id=tenant,
                                       insecure=True)
        ''' Get neutron client handle '''
        self.neutron = neutron_client.Client('2.0',
                                             auth_url=auth_url,
                                             username=username,
                                             password=password,
                                             tenant_name=tenant,
                                             insecure=True)
        ''' Get ironic client handle '''
        self.ironic = ironic_client.get_client(1, os_username=username,
                                               os_password=password,
                                               os_auth_url=auth_url,
                                               os_tenant_name=tenant,
                                               insecure=True)

def get_hosts_dict(auth_url, username, password, tenant):
    obj = Openstack(auth_url, username, password, tenant)
    hosts = list()
    for node in obj.ironic.node.list(fields=['name', 'instance_info', 'instance_uuid']):
        if not node.instance_info:
            continue
        host = dict()
        role = ast.literal_eval(node.instance_info['capabilities'])['profile']
        if 'contrail-controller' == role:
            host['role'] = 'controller'
        elif 'compute' == role or 'compute-dpdk' == role:
            host['role'] = 'compute'
        elif 'contrail-analytics-database' == role:
            host['role'] = 'analyticsdb'
        elif 'contrail-analytics' == role:
            host['role'] = 'analytics'
        elif 'control' == role:
            host['role'] = 'openstack'
        host['uuid'] = node.instance_uuid
        host['host_name'] = node.name
        fixed_ip = obj.neutron.list_ports(device_id=node.instance_uuid, fields='fixed_ips')
        host['mgmt_ip'] = fixed_ip['ports'][0]['fixed_ips'][0]['ip_address']
        hosts.append(host)
    return hosts

def parse_openrc(filename):
    openrc_dict = dict()
    openrc_values = dict()
    for line in open(filename, 'r').readlines():
        obj = re.match("export\s+(\w+)\s*=\s*(.*)", line)
        if obj:
            val = obj.group(2).strip("'")
            val = val.strip('"')
            openrc_values.update({obj.group(1):val})

    openrc_dict['admin_tenant'] = openrc_values.get('OS_PROJECT_NAME', '')
    openrc_dict['admin_user'] = openrc_values.get('OS_USERNAME', '')
    openrc_dict['admin_password'] = openrc_values.get('OS_PASSWORD', '')
    openrc_dict['region_name'] = openrc_values.get('OS_REGION_NAME', 'regionOne')
    url = openrc_values['OS_AUTH_URL']
    obj = re.match("(?P<protocol>\w+)://(?P<ip>\S+):(?P<port>\d+)", url)
    if obj:
        openrc_dict['auth_ip'] = obj.group('ip')
        openrc_dict['auth_port'] = obj.group('port')
        openrc_dict['auth_protocol'] = obj.group('protocol')
    return openrc_dict

def gen_host_name(hostname):
    special_char = ['-', ':', '.']
    for char in special_char:
        hostname = hostname.replace(char, '_')
    return 'host_'+hostname

def fixup_tb_string(tb_string, hosts):
    for host in hosts:
        tb_string = tb_string.replace('"'+host+'"', host)
    tb_string = tb_string.replace('null', 'None')
    tb_string = tb_string.replace('true', 'True')
    tb_string = tb_string.replace('false', 'False')
    return tb_string

def create_testbed_file(pargs, hosts, openrc_dict):
    tb_filename = pargs.tb_filename
    host_string = set()
    host_names = list()
    env_roledefs = defaultdict(list)
    control_data = {}
    env_keystone = {}
    env_test = {}
    env_ha = {}
    env_cfgm = {}
    env_password = {}
    login_name = 'heat-admin'
    is_analytics_isolated = False
    for host in hosts:
        host_name = gen_host_name(host['host_name'])
        host_names.append(host_name)
        host_string.add("%s = '%s@%s'" %(host_name, login_name, host['mgmt_ip']))
        env_roledefs['all'].append(host_name)
        env_password.update({host_name : 'SSH-KEY-SHARED'})
        node_vm_ip = host['mgmt_ip']
        role = host['role']
        grep_cmd = "/usr/sbin/ip address | grep 10.0.0. | cut -d '/' -f1 | awk '{print $2}'"
        api_int_ip = subprocess.check_output("sshpass ssh -o StrictHostKeyChecking=no heat-admin@%s %s"
                      % (node_vm_ip, grep_cmd), shell=True)
        control_data_ip=api_int_ip.split('\n')[0]
        #control_data.append(control_data_ip)
        ctrl_int_cmd = "/usr/sbin/route -n | grep 10.0.0 | awk '{print $8}'"
        gw_ip = subprocess.check_output("sshpass ssh -o StrictHostKeyChecking=no heat-admin@%s %s" 
                 % (node_vm_ip, ctrl_int_cmd), shell=True)
        ctrl_gw = gw_ip.split('\n')[0]
        control_data.update({host_name : {'ip': control_data_ip + '/24', 'gw': '10.0.0.1', 'device':ctrl_gw},})
        if 'openstack' == host['role']:
            env_roledefs['openstack'].append(host_name)
        elif 'controller' == host['role']:
            env_roledefs['cfgm'].append(host_name)
            env_roledefs['webui'].append(host_name)
            env_roledefs['control'].append(host_name)
        elif 'analytics' == host['role']:
            env_roledefs['collector'].append(host_name)
        elif 'analyticsdb' == host['role']:
            env_roledefs['database'].append(host_name)
        elif 'compute' == host['role']:
            env_roledefs['compute'].append(host_name)

    for k,v in env_roledefs.iteritems():
        env_roledefs[k] = list(set(v))
    env_ha.update({'contrail_external_vip': openrc_dict['auth_ip']})
    env_keystone.update({'keystone_ip': openrc_dict['auth_ip']})
    env_keystone.update({'auth_protocol': openrc_dict['auth_protocol']})
    env_keystone.update({'auth_port': openrc_dict['auth_port']})
    env_keystone.update({'admin_user': openrc_dict['admin_user']})
    env_keystone.update({'admin_password': openrc_dict['admin_password']})
    env_keystone.update({'admin_tenant': openrc_dict['admin_tenant']})
    env_keystone.update({'region_name': openrc_dict.get('region_name', 'regionOne')})
    env_keystone.update({'insecure': 'True'})

#    update mail and web server detail under env_test
#    env_test.update({'discovery_ip': hosts_dict['contrail_vip']})
#    env_test.update({'config_api_ip': hosts_dict['contrail_vip']})
#    env_test.update({'analytics_api_ip': hosts_dict['contrail_vip']})

    tb_list = list()
#    tb_list.append("env.test = %s"%json.dumps(env_test, sort_keys=True, indent=4))
    tb_list.append("env.keystone = %s"%json.dumps(env_keystone, sort_keys=True, indent=4))
    tb_list.append("env.ha = %s"%json.dumps(env_ha, sort_keys=True, indent=4))
#    tb_list.append("control_data = %s"%json.dumps(control_data, sort_keys=True, indent=4))
    tb_list.append("env.roledefs = %s"%json.dumps(env_roledefs, sort_keys=True, indent=4))
    tb_list.append("env.openstack_admin_password = '%s'"%
                    env_keystone['admin_password'])
    tb_list.append("env.passwords = %s"%json.dumps(env_password, sort_keys=True, indent=4))
    tb_list.append("control_data = %s"%json.dumps(control_data, sort_keys=True, indent=4))
    replaced_tb_string = fixup_tb_string('\n'.join(tb_list), host_names)

    tb_list = ['from fabric.api import env']
    tb_list.extend(sorted(host_string))
    tb_list.append(replaced_tb_string)
    with open(tb_filename, 'w+') as fd:
        fd.write('\n'.join(tb_list))

def parse_cli(args):
    parser = argparse.ArgumentParser(description='testbed.py file generator for RHOSP env')
    parser.add_argument('--overcloudrc', help='openrc file path')
    parser.add_argument('--username', help='undercloud username', default=os.getenv('OS_USERNAME'))
    parser.add_argument('--password', help='undercloud password', default=os.getenv('OS_PASSWORD'))
    parser.add_argument('--tenant', help='undercloud tenant name', default=os.getenv('OS_TENANT_NAME'))
    parser.add_argument('--auth_url', help='undercloud auth url', default=os.getenv('OS_AUTH_URL'))
    parser.add_argument('--tb_filename', default='testbed.py', help='Testbed output file name')
    parser.add_argument('--stackrc', help='stackrc file path')
    return parser.parse_args(args)

def main(args):
    pargs = parse_cli(args)
    hosts_dict = get_hosts_dict(pargs.auth_url, pargs.username, pargs.password, pargs.tenant)
    print hosts_dict
    openrc_dict = parse_openrc(pargs.overcloudrc)
    print openrc_dict
    create_testbed_file(pargs, hosts_dict, openrc_dict)

if __name__ == "__main__":
    main(sys.argv[1:])
