from fabric.api import env


host1 = 'root@10.204.216.15'
host2 = 'root@10.204.216.10'
host3 = 'root@10.204.217.209'
host4 = 'root@10.204.217.121'


ext_routers = [('blr-mx1', '10.204.216.253')]
router_asn = 64510
public_vn_rtgt = 19006
public_vn_subnet = "10.204.219.80/29"

host_build = 'stack@10.204.216.49'
#host_build = 'root@10.204.216.7'

env.roledefs = {
    'all': [ host1, host2,host3,host4],
    'cfgm': [host1],
    'openstack': [host1],
    'webui': [host1],
    'control': [host1],
    'collector': [host1],
    'database': [host1],
    'compute': [host2,host3,host4],
    'build': [host_build]
}

env.hostnames = {
    'all': ['nodea19', 'nodea14','nodel3','nodei9']
}

env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host_build: 'stack@123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
}

#env.orchestrator = 'vcenter'
control_data = {
    host1 : { 'ip': '192.168.250.4/24', 'gw' : '192.168.250.254', 'device':'em1' },
    host2 : { 'ip': '192.168.250.5/24', 'gw' : '192.168.250.254', 'device':'em1' },
    host3 : { 'ip': '192.168.250.8/24', 'gw' : '192.168.250.254', 'device':'em2' },
    host4 : { 'ip': '192.168.250.19/24', 'gw' : '192.168.250.254', 'device':'p6p2' },
}

minimum_diskGB=32
env.mail_from='contrail-build@juniper.net'
env.mail_to='sandipd@juniper.net'
multi_tenancy=True
env.interface_rename = False
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario='Vcenter Gateway'
env.enable_lbaas = True
do_parallel = True
env.ntp_server = 'ntp.juniper.net'

enable_ceilometer = True
ceilometer_polling_interval = 60
env.test_repo_dir='/root/contrail-test'
