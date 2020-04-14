from fabric.api import env

nodea7 = '10.204.216.45'
nodea30 = '10.204.216.26'
nodea31 = '10.204.216.27'
host1 = 'root@' + nodea31
host2 = 'root@' + nodea7
host3 = 'root@' + nodea30

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

ext_routers = []
router_asn = 64510
public_vn_rtgt = 10003
public_vn_subnet = '10.204.219.64/29'

host_build = 'stack@10.204.216.56'

env.roledefs = {
    'all': [host1, host2, host3],
    'cfgm': [host1],
    'control': [host1],
    'compute': [host3, host2],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'openstack': [host1],
    'build': [host_build],
}

env.hostnames = {
    'all': ['nodea31', 'nodea7', 'nodea30']
}

env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

env.ostypes = {
   host1 : 'ubuntu',
   host2 : 'ubuntu',
   host3 : 'ubuntu',
}

minimum_diskGB=32
# Folder where you have checked out the field-test git repo
env.test_repo_dir = '/homes/sunilbasker/test'
env.mail_to = 'sunilbasker@juniper.net'
env.mail_server = '10.204.216.49'
env.mail_port = '25'
env.log_scenario = 'OS test'
