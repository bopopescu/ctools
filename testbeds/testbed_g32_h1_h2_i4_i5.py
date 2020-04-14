from fabric.api import env

host1 = 'root@10.204.217.72'
host2 = 'root@10.204.217.105'
host3 = 'root@10.204.217.106'
host4 = 'root@10.204.217.116'
host5 = 'root@10.204.217.117'

ext_routers = [('hooper','10.204.217.240')]
router_asn = 64512
public_vn_rtgt = 2225
public_vn_subnet = '10.204.221.128/28'

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2, host3,host4,host5],
    'cfgm': [host1, host2],
    'webui': [host1],
    'openstack': [host1],
    'control': [host2, host3],
    'collector': [host1],
    'database': [host1],
    'compute': [host4, host5],
    'build': [host_build]
}

env.hostnames = {
    'all': ['nodeg32', 'nodeh1', 'nodeh2', 'nodei4', 'nodei5']
}
env.interface_rename = True

env.openstack_admin_password = 'contrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host_build: 'stack@123',
}

control_data = {
    host1 : { 'ip': '192.168.194.1/24', 'gw' : '192.168.194.254', 'device':'eth1' },
    host2 : { 'ip': '192.168.194.2/24', 'gw' : '192.168.194.254', 'device':'eth1' },
    host3 : { 'ip': '192.168.194.3/24', 'gw' : '192.168.194.254', 'device':'eth1' },
    host4 : { 'ip': '192.168.194.4/24', 'gw' : '192.168.194.254', 'device':'eth1' },
    host5 : { 'ip': '192.168.194.5/24', 'gw' : '192.168.194.254', 'device':'eth1' },
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
}
minimum_diskGB=32
env.test_repo_dir='/home/stack/multi_interface_parallel/ubuntu/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename = True
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario='MultiNode Multi Intf Sanity'
env.enable_lbaas = True
do_parallel = True
