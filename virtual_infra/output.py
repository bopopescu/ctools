from netaddr import *
import yaml
import sys
import argparse
import copy
import os
import copy

MANAGEMENT_NETWORK='management'
LOOPBACK_CIDR='172.16.11.128/26'

CONTROLLER_ROLES = ['control', 'analytics', 'config', 'webui',
                    'config_database', 'analytics_database']

class Output(object):
    def __init__(self, instances, networks, instances_info, global_configs=None,
                 contrail_configs=None, test_configs=None,
                 deployment=None, provider=None, orchestrator_configs=None,
                 version=None, sku=None, branch=None, report_path=None,
                 appformix_version=None):
        self.instances = instances
        self.networks = networks
        self.instances_info = instances_info
        self.global_configs = global_configs or dict()
        self.contrail_configs = contrail_configs or dict()
        self.test_configs = test_configs or dict()
        self.deployment = deployment or dict()
        self.provider = provider or dict()
        self.orchestrator_configs = orchestrator_configs or dict()
        self.version = version
        self.sku = sku
        self.branch = branch
        self.report_path = report_path
        self.appformix_version = appformix_version
        self.static_routes = dict()

    def update_branch(self):
        if self.branch and 'type' in self.deployment:
            for k,v in self.deployment['type'].iteritems():
                if k in ['openshift', 'helm', 'contrail']:
                    self.deployment['type'][k]['branch'] = self.branch

    def update_report_path(self):
        if self.report_path:
            webserver = self.test_configs.get('web_server', {})
            webserver['report_path'] = self.report_path
            self.test_configs['web_server'] = webserver

    def _get_instance(self, instance_name):
        for instance in self.instances:
            if instance_name == instance['name']:
                return instance

    def get_mgmt_ip(self, vm_name):
        return self.instances_info[vm_name][MANAGEMENT_NETWORK]['ip']

    def get_ctrl_data(self, vm_name):
        instance_name = self.instances_info[vm_name]['name']
        inst = self._get_instance(instance_name)
        pindex = 1
        if inst['type'] in ['leaf', 'spine']:
            pindex = 3
        elif inst['type'] == 'mx':
            pindex = 2
        net_name = inst['ports'][pindex]['network']
        dct = {'ip': self.instances_info[vm_name][net_name]['ip'],
               'mac': self.instances_info[vm_name][net_name]['mac']}
        return dct

    def get_tunnel_ip(self, vm_name):
        instance_name = self.instances_info[vm_name]['name']
        inst = self._get_instance(instance_name)
        if inst['type'] not in ['leaf', 'spine', 'mx']:
            return
        pindex = 3 if inst['type'] == 'mx' else 4
        net_name = inst['ports'][pindex]['network']
        return self.instances_info[vm_name][net_name]['aap_ip']

    def get_roles(self, instance_name):
        return self._get_instance(instance_name).get('roles') or {}

    def get_instances(self):
        instances = dict()
        for vm_name, instance in self.instances_info.iteritems():
            inst = self._get_instance(instance['name'])
            roles = copy.deepcopy(self.get_roles(instance['name']))
            if 'vrouter' in roles and \
                self.deployment.get('orchestrator') == 'kubernetes':
                if not roles['vrouter']:
                    roles['vrouter'] = dict()
                roles['vrouter'].update({'VROUTER_HOSTNAME': vm_name})
            if inst['type'] in ['leaf', 'spine', 'mx', 'bms']:
                continue
            instances[vm_name] = {'provider': 'bms',
                                  'roles': roles,
                                  'ip': self.get_mgmt_ip(vm_name),
                                  'fip': instance.get('fip')}
        return instances

    @property
    def has_ctrl_data(self):
        if not getattr(self, '_has_ctrl_data', None):
            for instance in self.instances:
                if 'control' in instance['roles'] and \
                   len(instance['ports']) > 1:
                   self._has_ctrl_data = True
                   break
            else:
                self._has_ctrl_data = False
        return self._has_ctrl_data

    def get_controller_nodes(self):
        controller_nodes = list()
        for vm_name, instance in self.instances_info.iteritems():
            if 'config' not in self.get_roles(instance['name']):
                continue
            controller_nodes.append(self.get_mgmt_ip(vm_name))
        return ','.join(controller_nodes)

    def get_nodes(self, role):
        nodes = list()
        for vm_name, instance in self.instances_info.iteritems():
            roles = self.get_roles(instance['name'])
            if role not in roles:
                continue
            if set(CONTROLLER_ROLES).issubset(set(roles.keys())):
                if role != 'control' or self.has_ctrl_data == False:
                    return
            if role == 'control' and self.has_ctrl_data:
                nodes.append(self.get_ctrl_data(vm_name)['ip'])
            else:
                nodes.append(self.get_mgmt_ip(vm_name))
        return ','.join(nodes)

    def get_csn_nodes(self):
        nodes = list()
        for vm_name, instance in self.instances_info.iteritems():
            roles = self.get_roles(instance['name'])
            if 'vrouter' not in roles or 'TSN_EVPN_MODE' not in (roles['vrouter'] or {}):
                continue
            if self.has_ctrl_data:
                nodes.append(self.get_ctrl_data(vm_name)['ip'])
            else:
                nodes.append(self.get_mgmt_ip(vm_name))
        return ','.join(nodes)

    def get_openstack_ip(self, interface='external'):
        for vm_name, instance in self.instances_info.iteritems():
            roles = self.get_roles(instance['name'])
            if not set(roles.keys()).intersection(
                   set(['openstack', 'openstack_control'])):
                continue
            network = MANAGEMENT_NETWORK
            if self.has_ctrl_data and interface == 'internal':
                inst = self._get_instance(instance['name'])
                network = inst['ports'][1]['network']
            if instance[network].get('aap_ip'):
                return instance[network]['aap_ip']
            return instance[network]['ip']

    def get_ctrl_data_network(self, name):
        for vm_name, instance in self.instances_info.iteritems():
            if name == vm_name:
                inst = self._get_instance(instance['name'])
                return inst['ports'][1]['network']

    def get_vrouter_gateway(self, name=None):
        for vm_name, instance in self.instances_info.iteritems():
            if 'vrouter' not in self.get_roles(instance['name']) \
               or (name and name != vm_name):
               continue
            network = MANAGEMENT_NETWORK
            if self.has_ctrl_data:
                inst = self._get_instance(instance['name'])
                network = inst['ports'][1]['network']
            return self.get_gateway(vm_name, network)

    def get_gateway(self, name, network):
        return self.instances_info[name][network]['gw']

    def get_cidr(self, network):
        return self.networks[network]['cidr']

    def update_k8s_fabric_subnets(self):
        for vm_name, instance in self.instances_info.iteritems():
            if 'vrouter' not in self.get_roles(instance['name']):
               continue
            network = MANAGEMENT_NETWORK
            if self.has_ctrl_data:
                inst = self._get_instance(instance['name'])
                network = inst['ports'][1]['network']
            cidr = self.get_cidr(network)
            fabric_subnet = str(IPNetwork(str(IPNetwork(cidr)[96])+'/27'))
            self.update_kv(self.contrail_configs,
                           KUBERNETES_IP_FABRIC_SUBNETS=fabric_subnet)
            return

    def update_kv(self, dct, **kwargs):
        if not dct:
            return
        for k, v in kwargs.iteritems():
            if v:
                dct[k] = v

    def update_deployment_configs(self):
        self.update_branch()
        self.update_kv(self.deployment,
                       sku=self.sku,
                       version=self.version,
                       appformix_version=self.appformix_version)

    def update_orchestrator_configs(self):
        openstack_internal_vip = self.get_openstack_ip('internal')
        openstack_external_vip = self.get_openstack_ip('external')
        self.update_kv(self.orchestrator_configs,
                       internal_vip=openstack_internal_vip,
                       external_vip=openstack_external_vip)

    def update_contrail_configs(self):
        controller_nodes = self.get_controller_nodes()
        config_nodes = self.get_nodes('config')
        control_nodes = self.get_nodes('control')
        analytics_nodes = self.get_nodes('analytics')
        webui_nodes = self.get_nodes('webui')
        configdb_nodes = self.get_nodes('config_database')
        analyticsdb_nodes = self.get_nodes('analytics_database')
        vrouter_gateway = self.get_vrouter_gateway()
        csn_nodes = self.get_csn_nodes()
        self.update_k8s_fabric_subnets()
        self.update_kv(self.contrail_configs,
                       CONTROLLER_NODES=controller_nodes,
                       CONFIG_NODES=config_nodes,
                       CONTROL_NODES=control_nodes,
                       ANALYTICS_NODES=analytics_nodes,
                       ANALYTICSDB_NODES=analyticsdb_nodes,
                       CONFIGDB_NODES=configdb_nodes,
                       WEBUI_NODES=webui_nodes,
                       TSN_NODES=csn_nodes,
                       VROUTER_GATEWAY=vrouter_gateway)

    def update_fabric(self):
        loopback = [LOOPBACK_CIDR]
        asn = [{'max': 64512, 'min': 64512}]
        ebgp_asn = [{'max': 65010, 'min': 65020}]
        node_profiles = ['juniper-mx', 'juniper-qfx10k', 'juniper-qfx5k']
        creds = {'username': 'root', 'password': 'c0ntrail123',
                 'vendor': 'Juniper', 'device_family': 'qfx'}
        management = list()
        peer = list()
        for vm_name, instance in self.instances_info.iteritems():
            inst = self._get_instance(instance['name'])
            if inst['type'] not in ['leaf', 'spine', 'mx']:
                continue
	    gw = self.get_gateway(vm_name, MANAGEMENT_NETWORK)
            cidr = str(IPNetwork(self.get_mgmt_ip(vm_name)))
            management.append({'cidr': cidr, 'gateway': gw})
            peer.append(str(IPNetwork(self.get_ctrl_data(vm_name)['ip'])))
        if not management:
            return
        namespaces = {'management': management,
                      'asn': asn,
                      'peer': peer,
                      'loopback': loopback,
                      'ebgp_asn': ebgp_asn}
        self.test_configs['fabric'] = [{'namespaces': namespaces,
                                        'node_profiles': node_profiles,
                                        'credentials': [creds]}]

    def get_connected_devices(self, network):
        devices = list()
        for vm_name, instance in self.instances_info.iteritems():
            if network not in instance:
                continue
            inst = self._get_instance(instance['name'])
            devices.append({'type': inst['type'],
                            'interface': instance[network].get('interface'),
                            'vm_name': vm_name,
                            'mac': instance[network]['mac'],
                            'ip': instance[network]['ip'],
                            })
        return devices

    def update_bms(self):
        bms = dict()
        for vm_name, instance in self.instances_info.iteritems():
            inst = self._get_instance(instance['name'])
            if inst['type'] != 'bms':
                continue
            interfaces = list()
            for port in inst['ports'][1:]:
                for device in self.get_connected_devices(port['network']):
                    if device['vm_name'] == vm_name:
                        continue
                    interfaces.append({'tor': device['vm_name'],
                                       'tor_port': device['interface'],
                                       'host_mac': instance[port['network']]['mac']})
                    break
            bms[vm_name] = {'interfaces': interfaces,
                            'mgmt_ip': self.get_mgmt_ip(vm_name),
                            'username': 'root',
                            'password': 'c0ntrail123'}
        if bms:
            self.test_configs['bms'] = bms

    def update_physical_routers(self):
        routers = dict()
        for vm_name, instance in self.instances_info.iteritems():
            inst = self._get_instance(instance['name'])
            if inst['type'] not in ['leaf', 'spine', 'mx']:
                continue
            peers = list()
            ports = inst['ports'][4:]
            model = 'vmx'
            if inst['type'] in ['leaf', 'spine']:
                ports = inst['ports'][4:]
                model = 'vqfx10k'
            for port in ports:
                port_info = instance[port['network']]
                for device in self.get_connected_devices(port['network']):
                    if device['type'] == 'bms' or device['vm_name'] == vm_name:
                        continue
                    peers.append({'peer_name': device['vm_name'],
                                  'peer_ip': device['ip'],
                                  'local_port': port_info['interface'],
                                  'local_mac': port_info['mac'],
                                  'local_ip': port_info['ip']})
                    break
            ctrl = self.get_ctrl_data(vm_name)
            routers[vm_name] = {'vendor': 'juniper',
                                'role': inst['type'],
                                'name': vm_name,
                                'peers': peers,
                                'tunnel_ip': self.get_tunnel_ip(vm_name),
                                'mgmt_ip': instance.get('fip') or self.get_mgmt_ip(vm_name),
                                'control_ip': ctrl['ip'],
                                'control_mac': ctrl['mac'],
                                'type': inst['type'],
                                'model': model,
                                'ssh_username': 'root',
                                'ssh_password': 'c0ntrail123'
                                }
        if routers:
            for vm_name, instance in self.instances_info.iteritems():
                inst = self._get_instance(instance['name'])
                if 'control' not in (inst.get('roles') or {}):
                    continue
                if vm_name not in self.static_routes:
                    self.static_routes[vm_name] = list()
                for rtr_name, rtr_details in routers.iteritems():
                    self.static_routes[vm_name].append(
                        {'ip': rtr_details['tunnel_ip'],
                         'gw': self.get_gateway(vm_name,
                               self.get_ctrl_data_network(vm_name))})
            self.test_configs['physical_routers'] = routers

    def update_test_configs(self):
        self.update_report_path()
        self.update_fabric()
        self.update_bms()
        self.update_physical_routers()

    def generate_all_yml(self):
        self.update_test_configs()
        self.update_deployment_configs()
        self.update_orchestrator_configs()
        self.update_contrail_configs()
        all_yml = {'deployment': self.deployment,
                   'provider_config': self.provider,
                   'global_configuration': self.global_configs,
                   'orchestrator_configuration': self.orchestrator_configs,
                   'test_configuration': self.test_configs,
                   'contrail_configuration': self.contrail_configs,
                   'instances': self.get_instances(),
                   'static_routes': self.static_routes}
        return all_yml

def parse_cli(args):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--topology', required=True, metavar="FILE",
                        help='location of the topology file')
    parser.add_argument('-c', '--configs', metavar="FILE",
                        help='location of the configuration file')
    parser.add_argument('-i', '--instance_info', metavar="FILE",
                        help='location of the instance info file')
    parser.add_argument('-f', '--filename',
                        help='where to store the generated all.yml')
    pargs = parser.parse_args(args)
    return pargs

def read_yaml(filename):
    with open(filename, 'r') as fd:
        yargs = yaml.load(fd)
    return yargs

def write_yaml(content, filename):
    with open(filename, 'w') as fd:
        yaml.safe_dump(content, fd, default_flow_style=False)

def write_all_yml(topology, configs, instances_info, filename,
                  version, sku, branch, report_path):
    tcontent = read_yaml(topology)
    ccontent = read_yaml(configs)
    output = Output(tcontent['instances'], tcontent['networks'],
                    instances_info,
                    ccontent.get('global_configuration'),
                    ccontent.get('contrail_configuration'),
                    ccontent.get('test_configuration'),
                    ccontent.get('deployment'),
                    ccontent.get('provider_config'),
                    ccontent.get('orchestrator_configuration'),
                    version, sku, branch, report_path)
    ocontent = output.generate_all_yml()
    write_yaml(ocontent, filename)

if __name__ == '__main__':
    pargs = parse_cli(sys.argv[1:])
    instance_info = read_yaml(pargs.instance_info)
    write_all_yml(pargs.topology, pargs.configs, instance_info,
                  pargs.filename, 'latest', 'ocata',
                  'master', '/var/tmp/msenthil/test')
