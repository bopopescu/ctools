from fabric.api import env

host1 = 'root@server1_ip_manage'
host2 = 'root@server2_ip_manage'
host3 = 'root@server3_ip_manage'
host4 = 'root@server4_ip_manage'
host5 = 'root@server5_ip_manage'

ext_routers = []
router_asn = 64512

host_build = 'root@server1_ip_manage'

env.roledefs = {
    'all': [host1, host2, host3,host4,host5],
    'cfgm': [host1,host2,host3],
    'openstack': [host1,host2,host3],
    'webui': [host1,host2,host3],
    'control': [host1,host2,host3],
    'collector': [host1,host2,host3],
    'database': [host1,host2,host3],
    'compute': [host4, host5],
    'build': [host_build]
}

env.hostnames = {
    'all': ['server1', 'server2', 'server3', 'server4', 'server5']
}

control_data = {
    host1 : { 'ip': 'server1_ip_control/24', 'gw' : '192.168.51.1', 'device':'eth1' },
    host2 : { 'ip': 'server2_ip_control/24', 'gw' : '192.168.51.1', 'device':'eth1' },
    host3 : { 'ip': 'server3_ip_control/24', 'gw' : '192.168.51.1', 'device':'eth1' },
    host4 : { 'ip': 'server4_ip_control/24', 'gw' : '192.168.51.1', 'device':'eth1' },
    host5 : { 'ip': 'server5_ip_control/24', 'gw' : '192.168.51.1', 'device':'eth1' },
}

env.ha = {
    'internal_vip' : 'internalvip',
    'external_vip' : 'externalvip'
}

ha_setup = True

env.openstack_admin_password = 'c0ntrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
}
env.cluster_id='test-cluster'
minimum_diskGB=32
env.test_repo_dir='/home/stack/multi_interface_parallel/ubuntu/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename = False
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.log_scenario='Virtual testbed'
env.enable_lbaas = True
enable_ceilometer = True
ceilometer_polling_interval = 60
do_parallel = True


