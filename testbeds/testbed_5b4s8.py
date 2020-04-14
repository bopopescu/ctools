from fabric.api import env

os_username = 'admin'
os_password = 'c0ntrail123'
os_tenant_name = 'demo'

# Management ip addresses of hosts in the cluster
host1 = 'root@10.87.64.132'  # b4s342
host2 = 'root@10.87.64.133'  # b4s343
host3 = 'root@10.87.64.134'  # b4s344
#host4 = 'root@10.87.64.135'  # b4s376

# Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.64.132'  # b4s342

# External routers if any
ext_routers = []

# Autonomous system number
router_asn = 64512
public_vn_rtgt = 12345
public_vn_subnet = "10.84.42.0/24"

# Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2 ],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1],
    'compute': [host2 ],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
    'all': ['5b4s8', '5b4s10', '5b4s12', '5b4s14']
}

bond= {
    host1 : { 'name': 'bond0', 'member': ['em1','em2'], 'mode':'802.3ad' },
    host2 : { 'name': 'bond0', 'member': ['em1','em2','em3','p2p1'], 'mode':'802.3ad' },
    host3 : { 'name': 'bond0', 'member': ['em1','em2','em3','p2p1'], 'mode':'802.3ad' },
}

control_data = {
    host1 : { 'ip': '5.5.5.132/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
    host2 : { 'ip': '5.5.5.133/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
    host3 : { 'ip': '5.5.5.134/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
}

static_route  = {
     host1 : [{ 'ip': '5.5.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'bond0' }, {'ip': '6.6.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'bond0' }],
     host2 : [{ 'ip': '5.5.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'vhost0' }, {'ip': '6.6.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'vhost0' }],
     host3 : [{ 'ip': '5.5.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'vhost0' }, {'ip': '6.6.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'vhost0' }]
}


# Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
#    host4: 'c0ntrail123',

    host_build: 'c0ntrail123',
}

env.dpdk = {
#    host2: { 'huge_pages' : '75', 'coremask' : '0xff'},
#    host3: { 'huge_pages' : '75', 'coremask' : '0xff'},
#    host4: { 'huge_pages' : '75', 'coremask' : '0xff'},
}

# For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
#    host4: 'ubuntu',
}
do_parallel = False

# HA Test configuration
ipmi_username = 'ADMIN'
ipmi_password = 'ADMIN'

env.hosts_ipmi = {
    '10.87.64.132': '10.87.122.29',
    '10.87.64.133': '10.87.122.30',
    '10.87.64.134': '10.87.122.31',
    '10.87.64.136': '10.87.122.32',
}


minimum_diskGB=32
env.test_repo_dir='/root/contrail-test'
