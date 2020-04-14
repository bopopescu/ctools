from fabric.api import env
import os


os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'admin'

host1 = 'root@10.204.217.6'
host2 = 'root@10.204.217.4'
host3 = 'root@10.204.217.5'
host4 = 'root@10.204.216.31'
host5 = 'root@10.204.217.128'
host6 = 'root@10.204.217.130'
host7 = 'root@10.204.216.120'

ext_routers = [('blr-mx2', '192.168.10.254')]
router_asn = 64512
public_vn_rtgt = 33333
public_vn_subnet = '10.204.219.48/29'

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6, host7],
    'contrail-compute': [host5, host6, host7],
    'openstack': [host1],
    'contrail-controller': [host1, host2, host3],
    'contrail-analytics': [host1, host2, host3],
    'contrail-analyticsdb': [host1, host2, host3],
    'contrail-lb':[host4],
    'build': [host_build],
}

if os.getenv('AUTH_PROTOCOL',None) == 'https':
    env.log_scenario = 'Multi-Interface contrail HA Sanity[mgmt, ctrl=data, SSL]'
    env.keystone = {
        'auth_protocol': 'https'
    }
    env.cfgm = {
        'auth_protocol': 'https'
    }
else:
    env.log_scenario = 'Multi-Interface contrail HA Sanity[mgmt, ctrl=data]'

if os.getenv('ENABLE_RBAC',None) == 'true':
    cloud_admin_role = 'admin'
    aaa_mode = 'rbac'


env.physical_routers={
'blr-mx2'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'blr-mx2',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.216.245',
             }
}

env.hostnames = {
    'all': ['nodec19', 'nodec20', 'nodec21', 'nodea35', 'nodei16', 'nodei18', 'nodea4']
}

bond= {
    host5 : { 'name': 'bond0', 'member': ['p6p1','p6p2'],'mode':'802.3ad' },
    host6 : { 'name': 'bond0', 'member': ['p6p1','p6p2'],'mode':'balance-xor' },
}

control_data= {

    host1 : { 'ip': '192.168.10.1/24', 'gw' : '192.168.10.254', 'device':'p1p2' },
    host2 : { 'ip': '192.168.10.2/24', 'gw' : '192.168.10.254', 'device':'p1p2' },
    host3 : { 'ip': '192.168.10.3/24', 'gw' : '192.168.10.254', 'device':'p1p2' },
    host4 : { 'ip': '192.168.10.4/24', 'gw' : '192.168.10.254', 'device':'em1' },
    host5 : { 'ip': '192.168.10.5/24', 'gw' : '192.168.10.254', 'device':'bond0' },
    host6 : { 'ip': '192.168.10.6/24', 'gw' : '192.168.10.254', 'device':'bond0' },
    host7 : { 'ip': '192.168.10.7/24', 'gw' : '192.168.10.254', 'device':'p2p4' }
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
    host7: 'c0ntrail123',
    host_build: 'stack@123',
}
env.ha = {
    'contrail_internal_vip' : '192.168.10.4',
    'contrail_external_vip' : '10.204.216.31'
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
    host7: 'ubuntu'
}

env.cluster_id='clusterc19c20c21a35i16i18'
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
