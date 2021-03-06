from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

#host1 = 'root@10.204.216.7'
host1 = 'root@10.204.216.17'

ext_routers = []
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = "10.84.46.0/24"

host_build = 'sandipd@10.204.216.4'

env.roledefs = {
    'all': [host1], 
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1 ],
    'compute': [host1],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
    #'all': ['nodea11']
    'all': ['nodea21']
}


env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'c0ntrail123',
}
env.ostypes = {
    host1:'ubuntu',
}

minimum_diskGB=32
enable_ceilometer = True

#env.test_repo_dir='/home/sandipd/multinode/contrail-test/contrail-test/'
env.test_repo_dir='/home/sandipd/testr_bhushana_fork/contrail-test/'
env.mail_from='sandipd@juniper.net'
env.mail_to='sandipd@juniper.net'
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
