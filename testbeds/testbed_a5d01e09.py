from fabric.api import env

os_username = 'admin'
os_password = 'c0ntrail123'
os_tenant_name = 'demo'

# Management ip addresses of hosts in the cluster
host1 = 'root@10.87.143.105'  # a5d01e092
host2 = 'root@10.87.143.107'  # a5d01e093
host3 = 'root@10.87.143.109'  # a5d01e094

# Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.143.105'  # a5d01e092

# External routers if any
ext_routers = []

# Autonomous system number
router_asn = 64512
public_vn_rtgt = 12345
public_vn_subnet = "10.84.42.0/24"

# Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1],
    'compute': [host2, host3],
    'collector': [host2],
    'webui': [host1],
    'database': [host2],
    'build': [host_build],
}

env.hostnames = {
    'all': ['a5d01e09-1', 'a5d01e09-2', 'a5d01e09-3']
}


# Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',

    host_build: 'c0ntrail123',
}

# For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
}
minimum_diskGB = 64

# To Enable prallel execution of task in multiple nodes
do_parallel = False

# HA Test configuration
ha_setup = 'True'
ipmi_username = 'ADMIN'
ipmi_password = 'ADMIN'

env.hosts_ipmi = {
    '10.87.143.105': '10.87.143.104',
    '10.87.143.107': '10.87.143.106',
    '10.87.143.109': '10.87.143.108',
}


env.test_repo_dir='/root/contrail-test/'

