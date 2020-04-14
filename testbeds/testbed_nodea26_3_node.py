from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

host1 = 'root@10.204.216.22'
host2 = 'root@10.204.217.56'
host3 = 'root@10.204.217.66'


ext_routers = [('blr-mx1', '10.204.216.253')]
router_asn = 64510
public_vn_rtgt = 19005
public_vn_subnet = "10.204.220.168/29"

host_build = 'ganeshahv@10.204.216.3'

env.roledefs = {
    'all': [host1, host2, host3],
    'cfgm': [host1],
    'control': [host2, host3],
    'compute': [host2, host3],
    'collector': [host1],
    'openstack': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
     'all': ['nodea26', 'nodeg16', 'nodeg26']
}

env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host_build: 'secret',
}
env.ostypes = { 
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    }

env.test_repo_dir='/homes/ganeshahv/git-hub/contrail-test'
#env.test_repo_dir='/homes/ganeshahv/commit_queue/Feb-02/contrail-test'
env.mail_from='ganeshahv@juniper.net'
env.mail_to='ganeshahv@juniper.net'

#To enable haproxy feature
#haproxy = True

