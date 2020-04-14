from fabric.api import env
import os


os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'admin'

host1 = 'root@10.204.217.108'
host2 = 'root@10.204.217.98'
host3 = 'root@10.204.217.52'
host4 = 'root@10.204.217.100'
host5 = 'root@10.204.217.71'
host6 = 'root@10.204.217.101'

ext_routers = []
router_asn = 64512

host_build = 'stack@10.204.216.49'

host_build = 'stack@10.204.216.49'
env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6],
    'contrail-controller': [host1, host3, host5],
    'openstack': [host1],
    'contrail-compute': [host2, host4, host6],
    'contrail-analytics': [host1, host3, host5],
    'contrail-analyticsdb': [host1, host3, host5],
    'build': [host_build],
}

env.hostnames = {
     'all': ['nodeh4', 'nodec58', 'nodeg12', 'nodec60', 'nodeg31', 'nodec61']
}

bond= {
    host4 : { 'name': 'bond0', 'member': ['p2p1','p2p2'],'mode':'802.3ad' },
}

control_data = {
    host1 : { 'ip': '77.77.1.10/24', 'gw' : '77.77.1.254', 'device': 'p2p2' },
    host2 : { 'ip': '77.77.1.11/24', 'gw' : '77.77.1.254', 'device': 'p2p2' },
    host3 : { 'ip': '77.77.2.10/24', 'gw' : '77.77.2.254', 'device': 'p1p2' },
    host4 : { 'ip': '77.77.2.11/24', 'gw' : '77.77.2.254', 'device': 'bond0' },
    host5 : { 'ip': '77.77.3.10/24', 'gw' : '77.77.3.254', 'device': 'p1p2' },
    host6 : { 'ip': '77.77.3.11/24', 'gw' : '77.77.3.254', 'device': 'p2p2' },
}

static_route  = {
    host1 : [{ 'ip': '77.77.2.0', 'netmask' : '255.255.255.0', 'gw':'77.77.1.254', 'intf': 'p2p2' },
             { 'ip': '77.77.3.0', 'netmask' : '255.255.255.0', 'gw':'77.77.1.254', 'intf': 'p2p2' }],
    host2 : [{ 'ip': '77.77.2.0', 'netmask' : '255.255.255.0', 'gw':'77.77.1.254', 'intf': 'p2p2' },
             { 'ip': '77.77.3.0', 'netmask' : '255.255.255.0', 'gw':'77.77.1.254', 'intf': 'p2p2' }],
    host3 : [{ 'ip': '77.77.1.0', 'netmask' : '255.255.255.0', 'gw':'77.77.2.254', 'intf': 'p1p2' },
             { 'ip': '77.77.3.0', 'netmask' : '255.255.255.0', 'gw':'77.77.2.254', 'intf': 'p1p2' }],
    host4 : [{ 'ip': '77.77.1.0', 'netmask' : '255.255.255.0', 'gw':'77.77.2.254', 'intf': 'bond0' },
             { 'ip': '77.77.3.0', 'netmask' : '255.255.255.0', 'gw':'77.77.2.254', 'intf': 'bond0' }],
    host5 : [{ 'ip': '77.77.1.0', 'netmask' : '255.255.255.0', 'gw':'77.77.3.254', 'intf': 'p1p2' },
             { 'ip': '77.77.2.0', 'netmask' : '255.255.255.0', 'gw':'77.77.3.254', 'intf': 'p1p2' }],
    host6 : [{ 'ip': '77.77.1.0', 'netmask' : '255.255.255.0', 'gw':'77.77.3.254', 'intf': 'p2p2' },
             { 'ip': '77.77.2.0', 'netmask' : '255.255.255.0', 'gw':'77.77.3.254', 'intf': 'p2p2' }]
}

env.password = 'c0ntrail123'
env.openstack_admin_password = 'contrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',

    host_build: 'stack@123',
}

env.kernel_upgrade=False
env.openstack = {
    'manage_amqp': "true"
}

env.keystone = {
    'admin_password': 'contrail123'
}

env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
    host6: 'ubuntu',
}

env.cluster_id='cluster_pulkit_h4g12g31c58c60c61'
minimum_diskGB = 32
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
env.encap_priority="VXLAN,MPLSoUDP,MPLSoGRE"
env.test_repo_dir = '/home/stack/regression/contrail-test'
env.mail_from = 'contrail-build@juniper.net'
env.mail_to = 'dl-contrail-sw@juniper.net'
multi_tenancy = True
env.enable_lbaas = True
do_parallel = True
env.xmpp_auth_enable=True
env.xmpp_dns_auth_enable=True
enable_ceilometer = True
ceilometer_polling_interval = 60
