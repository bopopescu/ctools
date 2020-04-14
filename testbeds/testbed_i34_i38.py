from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

host2 = 'root@10.204.217.146'
host3 = 'root@10.204.217.147'
host4 = 'root@10.204.217.148'
host5 = 'root@10.204.217.149'
host6 = 'root@10.204.217.150'

ext_routers = [('blr-mx2', '10.204.216.245')]
router_asn = 64512
public_vn_rtgt = 30001
public_vn_subnet = "10.204.219.72/29"

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host2, host3, host4, host5, host6],
    'cfgm': [host2, host3],
    'openstack': [host2],
    'webui': [host3],
    'control': [host3, host4],
    'compute': [host5, host6],
    'collector': [host2, host3],
    'database': [host2, host3, host4],
    'build': [host_build],
}

env.hostnames = {
    'all': ['nodei34', 'nodei35', 'nodei36', 'nodei37', 'nodei38']
}

env.password = 'c0ntrail123'
env.passwords = {
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',

    host_build: 'stack@123',
}

env.ostypes = {
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    host6:'ubuntu',
}
minimum_diskGB=32
#env.test_repo_dir='/home/shettyp/parallel/contrail-test'
env.test_repo_dir='/home/shettyp/mainline/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename=True
env.log_scenario='MultiNode'
env.enable_lbaas = True
