from fabric.api import env
import os

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'admin'


host1 = 'root@10.204.216.95'
host2 = 'root@10.204.216.96'
host3 = 'root@10.204.216.97'
host4 = 'root@10.204.216.98'
host5 = 'root@10.204.216.99'
host6 = 'root@10.204.216.103'
host7 = 'root@10.204.216.160'

kvm_nodek7 = '10.204.216.227'

ext_routers = [('blr-mx1', '10.10.10.101')]
#IP Fabric gateway info, name and IP tuple
#eg: [('mx1', '1.1.1.1')]
fabric_gw =[('sw166', '10.204.217.254')]
router_asn = 64512
public_vn_rtgt = 19005
public_vn_subnet = "10.204.219.120/29"
use_devicemanager_for_md5 = True

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6, host7],
    'contrail-controller': [host6, host2, host1],
    'contrail-analytics': [host6, host2, host1],
    'contrail-analyticsdb': [host6, host2, host1],
    'openstack': [host6, host2, host1],
    'contrail-compute': [host3, host4, host5],
    'contrail-lb': [host7],
    'build': [host_build]
}

env.physical_routers={
'blr-mx1'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'blr-mx1',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.216.253',
             }
}

env.dm_mx={
'yuvaraj'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'yuvaraj',
                     'control_ip' : '10.10.10.100',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.190',
             }
}

env.hostnames = {
    'all': ['nodem6', 'nodem7', 'nodem8', 'nodem9', 'nodem10', 'nodem14', 'nodec35']
}

env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'

env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
    host7: 'c0ntrail123',
    host_build: 'stack@123',
}

vm_node_details = {
    'default': {
                'image_dest' : '/mnt/disk1/images/',
                'ram' : '32768',
                'vcpus' : '4',
                'disk_format' : 'qcow2',
                'image_source' : 'http://10.204.217.158/images/node_vm_images/centos-7.5.qcow2',
                },
    host1 : {   'name' : 'nodek7-vm1',
                'server': kvm_nodek7,
                'network' : [{'bridge' : 'br0', 'mac':'52:53:57:01:00:01'},{'bridge': 'br1'}
                            ]
            }
}



env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    host6:'ubuntu',
    host7:'ubuntu',
}

bond= {
    host3 : { 'name': 'bond0', 'member': ['p514p1','p514p2'], 'mode': '802.3ad' },
}

control_data = {
    host1: {'ip': '10.10.10.6/24', 'gw': '10.10.10.100', 'device': 'p514p2'},
    host2: {'ip': '10.10.10.7/24', 'gw': '10.10.10.100', 'device': 'p514p2'},
    host3: {'ip': '10.10.10.8/24', 'gw': '10.10.10.100', 'device': 'bond0'},
    host4: {'ip': '10.10.10.9/24', 'gw': '10.10.10.100', 'device': 'p514p2'},
    host5: {'ip': '10.10.10.10/24', 'gw': '10.10.10.100', 'device': 'p514p2'},
    host6: {'ip': '10.10.10.14/24', 'gw': '10.10.10.100', 'device': 'p514p2'},
    host7: {'ip': '10.10.10.35/24', 'gw': '10.10.10.100', 'device': 'p1p2'}
}

env.ha = {
    'contrail_internal_vip' : '10.10.10.35',
    'contrail_external_vip' : '10.204.216.160',
    'internal_vip' : '10.10.10.20',
    'external_vip' : '10.204.216.140',
}

env.qos = {host3: [{'hardware_q_id': '3', 'logical_queue':['1', '6-10', '12-15']},
                   {'hardware_q_id': '11', 'logical_queue':['40-46']},
                   {'hardware_q_id': '18', 'logical_queue':['70-74', '75', '80-95']},
                   {'hardware_q_id': '28', 'logical_queue':['115']},
                   {'hardware_q_id': '36', 'logical_queue':['140-143', '145']},
                   {'hardware_q_id': '43', 'logical_queue':['175']},
                   {'hardware_q_id': '53', 'logical_queue':['215'], 'default': 'True'},
                   {'hardware_q_id': '61', 'logical_queue':['245']}],
            host4: [{'hardware_q_id': '3', 'logical_queue':['1', '6-10', '12-15']},
                   {'hardware_q_id': '11', 'logical_queue':['40-46']},
                   {'hardware_q_id': '18', 'logical_queue':['70-74', '75', '80-95']},
                   {'hardware_q_id': '28', 'logical_queue':['115']},
                   {'hardware_q_id': '36', 'logical_queue':['140-143', '145']},
                   {'hardware_q_id': '43', 'logical_queue':['175']},
                   {'hardware_q_id': '53', 'logical_queue':['215'], 'default': 'True'},
                   {'hardware_q_id': '61', 'logical_queue':['245']}]}

env.qos_niantic = {host3:[
                          { 'priority_id': '0', 'scheduling': 'strict', 'bandwidth': '0'},
                          { 'priority_id': '1', 'scheduling': 'rr', 'bandwidth': '10'},
                          { 'priority_id': '2', 'scheduling': 'strict', 'bandwidth': '0'},
                          { 'priority_id': '3', 'scheduling': 'rr', 'bandwidth': '20'},
                          { 'priority_id': '4', 'scheduling': 'strict', 'bandwidth': '0'},
                          { 'priority_id': '5', 'scheduling': 'rr', 'bandwidth': '30'},
                          { 'priority_id': '6', 'scheduling': 'strict', 'bandwidth': '0'},
                          { 'priority_id': '7', 'scheduling': 'rr', 'bandwidth': '40'}],
                   host4:[
                          { 'priority_id': '0', 'scheduling': 'strict', 'bandwidth': '0'},
                          { 'priority_id': '1', 'scheduling': 'rr', 'bandwidth': '10'},
                          { 'priority_id': '2', 'scheduling': 'strict', 'bandwidth': '0'},
                          { 'priority_id': '3', 'scheduling': 'rr', 'bandwidth': '20'},
                          { 'priority_id': '4', 'scheduling': 'strict', 'bandwidth': '0'},
                          { 'priority_id': '5', 'scheduling': 'rr', 'bandwidth': '30'},
                          { 'priority_id': '6', 'scheduling': 'strict', 'bandwidth': '0'},
                          { 'priority_id': '7', 'scheduling': 'rr', 'bandwidth': '40'}]}

env.cluster_id='new_regr_cluster'
minimum_diskGB = 32
#env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
#env.test_repo_dir = '/home/stack/regression/contrail-test'
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.mail_from = 'contrail-build@juniper.net'
env.mail_to = 'dl-contrail-sw@juniper.net'
multi_tenancy = True
#env.interface_rename = True
env.log_scenario = 'SMLite Openstack HA Regression'
env.enable_lbaas = True
do_parallel = True
env.test_repo_dir='/root/contrail-test'
env.xmpp_auth_enable=True
env.xmpp_dns_auth_enable=True
