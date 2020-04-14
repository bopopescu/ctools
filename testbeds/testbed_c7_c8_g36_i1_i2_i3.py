from fabric.api import env
import os

host1 = 'root@10.204.216.64'
host2 = 'root@10.204.216.65'
host3 = 'root@10.204.217.76'
host4 = 'root@10.204.216.150'
host5 = 'root@10.204.217.114'
host6 = 'root@10.204.217.115'
host7 = 'root@10.204.216.153'

ext_routers = [('hooper','192.168.192.253')]
router_asn = 64512
public_vn_rtgt = 2223
public_vn_subnet = '10.204.221.176/28'

host_build = 'stack@10.204.216.49'


env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6, host7],
    'contrail-controller': [host4, host5, host6],
    'openstack': [host4, host5, host6],
    'contrail-analytics': [host4, host5, host6],
    'contrail-lb': [host3],
    'contrail-compute': [host1, host2, host7],
    'contrail-analyticsdb': [host4, host5, host6],
    'build': [host_build],
}

if os.getenv('AUTH_PROTOCOL',None) == 'https':
    env.log_scenario='Multi-Interface Container HA Sanity[mgmt, ctrl=data, SSL]'
    env.keystone = {
        'auth_protocol': 'https'
    }
    env.cfgm = {
        'auth_protocol': 'https'
    }
else:
    env.log_scenario='Multi-Interface Container HA Sanity[mgmt, ctrl=data]'

if os.getenv('ENABLE_RBAC',None) == 'true':
    cloud_admin_role = 'admin'
    aaa_mode = 'rbac'

env.hostnames = {
    'all': ['nodec7', 'nodec8', 'nodeg36', 'nodei1', 'nodei2', 'nodei3', 'nodec57']
}
env.physical_routers={
'hooper'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'hooper',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.240',
             }
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

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    host6:'ubuntu',
    host7:'ubuntu',
}

control_data = {
    host1 : { 'ip': '192.168.192.6/24', 'gw' : '192.168.192.254', 'device':'p1p2' },
    host2 : { 'ip': '192.168.192.5/24', 'gw' : '192.168.192.254', 'device':'p1p2' },
    host3 : { 'ip': '192.168.192.4/24', 'gw' : '192.168.192.254', 'device':'p1p2' },
    host4 : { 'ip': '192.168.192.1/24', 'gw' : '192.168.192.254', 'device':'em2' },
    host5 : { 'ip': '192.168.192.2/24', 'gw' : '192.168.192.254', 'device':'em2' },
    host6 : { 'ip': '192.168.192.3/24', 'gw' : '192.168.192.254', 'device':'em2' },
    host7 : { 'ip': '192.168.192.7/24', 'gw' : '192.168.192.254', 'device':'p1p2' },
}

env.ha = {
    'internal_vip' : '192.168.192.251',
    'external_vip' : '10.204.217.154',
    'contrail_internal_vip' : '192.168.192.4',
    'contrail_external_vip' : '10.204.217.76',
}
ha_setup = True

env.cluster_id='clusterc7c8g36i1i2i3'
minimum_diskGB=32
env.test_repo_dir='/home/stack/multi_interface_parallel/ubuntu-14.04/icehouse/contrail-test'
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename = True
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.enable_lbaas = True
do_parallel = True

enable_ceilometer = True
ceilometer_polling_interval = 60
