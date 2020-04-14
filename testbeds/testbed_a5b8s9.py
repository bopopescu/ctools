from fabric.api import env

host1 = 'root@10.87.66.137'
host2 = 'root@10.87.66.138'
host3 = 'root@10.87.66.139'
host4 = 'root@10.87.66.156'
host5 = 'root@10.87.66.141'
host6 = 'root@10.87.66.142'

ext_routers = [('5b8-mx80-2','10.87.66.250')]
router_asn = 64512
public_vn_rtgt = 2224
public_vn_subnet = '10.204.221.192/28'

host_build = 'stack@10.84.24.64'

env.roledefs = {
    'all': [host1, host2, host3,host4,host5, host6],
    'cfgm': [host1],
    'openstack': [host1],
    'webui': [host1],
    'control': [host1],
    'collector': [host1],
    'database': [host1],
    'compute': [host2, host3, host4, host5, host6],
    'build': [host_build]
}

env.hostnames = {
    'all': ['5b8s9', '5b8s10', '5b8s11', '5b8s12', '5b8s13', '5b8s14']
}
env.interface_rename = False
env.physical_routers={
'5b8-mx80-2'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : '5b8-mx80-2',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '10.87.66.250',
             }
}

control_data = {
    host1 : { 'ip': '192.168.15.1/24', 'gw' : '192.168.15.254', 'device':'p514p1' },
    host2 : { 'ip': '192.168.15.2/24', 'gw' : '192.168.15.254', 'device':'p514p1' },
    host3 : { 'ip': '192.168.15.3/24', 'gw' : '192.168.15.254', 'device':'p514p1' },
    host4 : { 'ip': '192.168.15.4/24', 'gw' : '192.168.15.254', 'device':'p514p1' },
    host5 : { 'ip': '192.168.15.5/24', 'gw' : '192.168.15.254', 'device':'p514p1' },
    host5 : { 'ip': '192.168.15.6/24', 'gw' : '192.168.15.254', 'device':'p514p1' },
}

#env.ha = {
#    'internal_vip' : '10.204.217.170'
#}
ha_setup = False

env.openstack_admin_password = 'c0ntrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
    host_build: 'stack@123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    host6:'ubuntu',
}
env.cluster_id='cluster-5b8s9'
minimum_diskGB=32
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
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
