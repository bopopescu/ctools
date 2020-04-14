from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

host1 = 'root@10.204.217.142'


ext_routers = [('blr-mx2', '10.204.216.245')]
router_asn = 64512
public_vn_rtgt = 19005
public_vn_subnet = "10.204.219.96/29"

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1],
    'cfgm': [host1],
    'control': [host1],
    'compute': [host1],
    'collector': [host1],
    'openstack': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
     'all': ['nodei30']
}

env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'stack@123',
}
env.ostypes = { 
    host1: 'ubuntu',
    }
minimum_diskGB=32
env.test_repo_dir='/homes/ganeshahv/git-hub/contrail-test'
env.mail_from='ganeshahv@juniper.net'
env.mail_to='ganeshahv@juniper.net'

#To enable haproxy feature
#haproxy = True

#enable ceilometer                                                                                                                                                                                                                          
enable_ceilometer = True                                                                                                                                                                                                                    
ceilometer_polling_interval = 60
