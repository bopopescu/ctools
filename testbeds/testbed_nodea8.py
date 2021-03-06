from fabric.api import env

host1 = 'root@10.204.216.46';
host_build = 'vishnuvv@nodeb11'

ext_routers = []
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = '10.1.1.0/24'


env.roledefs = {
    'all': [host1],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1],
    'compute': [host1],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}
env.hostnames = {
    'all': ['nodea8']
}

env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'secret',
}

env.ostypes = {
        host1: 'ubuntu',
}

env.test_repo_dir='/home/vishnuvv/test'
env.mail_from='vishnuvv@juniper.net'
env.mail_to='vishnuvv@juniper.net'
