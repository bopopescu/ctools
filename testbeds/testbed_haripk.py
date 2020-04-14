from fabric.api import env

host1 = 'root@10.204.216.16'
host2 = 'root@10.204.216.24'

ext_routers = []
router_asn = 64510
public_vn_rtgt = 10003
public_vn_subnet = '10.204.219.32/28'
minimum_diskGB=32

env.ostypes = {
      host1: 'centos',
      host2: 'centos',
}

host_build = 'haripk@10.204.216.3'

env.roledefs = {
    'all': [host1, host2],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1],
    'compute': [host1, host2],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
#    'vgw': [host2],
}

env.hostnames = {
    'all': ['nodea20', 'nodea28']
}

env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host_build: 'c0ntrail123'
}

env.test_repo_dir='/homes/haripk/contrail-test'
env.mail_from='haripk@juniper.net'
env.mail_to='haripk@juniper.net'

