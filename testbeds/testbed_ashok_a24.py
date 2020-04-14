from fabric.api import env

os_username = 'admin'
os_password = 'c0ntrail123'
os_tenant_name = 'demo'

host1 = 'root@10.204.216.20'
host2 = 'root@10.204.216.21'

ext_routers = []
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = "10.84.46.0/24"

host_build = 'root@10.204.216.20'

env.interface_rename = False

env.roledefs = {
    'all': [host1,host2],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1, host2],
    'compute': [host1, host2],
    'collector': [host1],
    'webui': [host1],
    'build': [host_build],
    'database': [host1],
}

env.hostnames = {
    'all': ['nodea24', 'nodea25']
}

env.ostypes = {
    host1: 'centos',
    host2: 'centos',
}

env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

multi_tenancy=True
do_parallel=True
minimum_diskGB=32
env.test_repo_dir='/root/contrail-test'
env.mail_from='ashoksr@juniper.net'
env.mail_to='ashoksr@juniper.net'
