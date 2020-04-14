from fabric.api import env

os_username = 'admin'
#os_password = 'contrail123'
os_tenant_name = 'demo'

host1 = 'root@10.204.221.58'
host2 = 'root@10.204.221.59'
host3 = 'root@10.204.221.60'
host4 = 'root@10.204.221.61'

ext_routers = []
router_asn = 64512
database_dir = '/home/cassandra'

host_build = 'root@10.204.216.4'

env.roledefs = {
    'all': [host1, host2, host3, host4],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1,host2],
    'compute': [host3,host4],
    'collector': [host2],
    'webui': [host2],
    'database': [host1],
    'build': [host_build],
}


env.hostnames = {
    'all': [ 'nodec35', 'nodec33', 'nodea4', 'nodec57']
}

#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu'	
}

bond= {
    host3 : { 'name': 'bond0', 'member': ['eth1','eth2','eth3','eth4'],'mode':'802.3ad' },
}

control_data = {
    host2 : { 'ip': '192.168.100.3/24', 'gw' : '', 'device':'eth1' },
    host1 : { 'ip': '192.168.100.4/24', 'gw' : '', 'device':'eth1' },
    host3 : { 'ip': '192.168.100.1/24', 'gw' : '', 'device':'bond0' },
    host4 : { 'ip': '192.168.100.2/24', 'gw' : '', 'device':'eth1' },
}


env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host_build: 'stack@123',
}

env.xmpp_auth_enable=True
env.xmpp_dns_auth_enable=True

multi_tenancy = True
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.test_repo_dir='/home/stack/smgr_github_multi_interface/contrail-test'
env.enable_lbaas = True
do_parallel = True
enable_ceilometer = True
ceilometer_polling_interval = 60
minimum_diskGB=32
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
env.log_scenario='Server Manager Ubuntu Multi-Interface Sanity'
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
