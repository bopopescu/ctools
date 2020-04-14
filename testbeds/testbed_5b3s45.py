from fabric.api import env

os_username = 'admin'
os_password = 'c0ntrail123'
os_tenant_name = 'demo'

# Management ip addresses of hosts in the cluster
host1 = 'root@10.87.64.147'  
host2 = 'root@10.87.64.157' 
host3 = 'root@10.87.64.158'  
#host4 = 'root@10.87.64.135' 

# Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.64.147'  # b4s342

# External routers if any
ext_routers = [('cmbu-lakewood', '10.87.140.181'),('5b4-mx240', '10.87.64.246')]

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
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
    'all': ['5b3s45', '5b4s30', '5b4s39']
}

bond= {
    host1 : { 'name': 'bond0', 'member': ['em1','em2'], 'mode':'802.3ad' },
    host2 : { 'name': 'bond0', 'member': ['p1p1','p1p2','p2p1','p2p2'], 'mode':'802.3ad' },
    host3 : { 'name': 'bond0', 'member': ['p1p1','p1p2','p2p1','p2p2'], 'mode':'802.3ad' },
}

control_data = {
    host1 : { 'ip': '5.5.5.232/24', 'gw' : '5.5.5.1', 'device' : 'p514p1'},
    host2 : { 'ip': '5.5.5.233/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
    host3 : { 'ip': '5.5.5.234/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
}

static_route  = {
     host1 : [{ 'ip': '5.5.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'p514p1' }, {'ip': '6.6.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'p514p1' }],
     host2 : [{ 'ip': '5.5.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'bond0' }, {'ip': '6.6.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'bond0' }],
     host3 : [{ 'ip': '5.5.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'bond0' }, {'ip': '6.6.0.0', 'netmask' : '255.255.0.0', 'gw':'5.5.5.1', 'intf': 'bond0' }]
}


# Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
#    host4: 'c0ntrail123',

    host_build: 'c0ntrail123',
}

env.vrouter_module_params = {
host2:{'vr_flow_entries':'4000000'},
host3:{'vr_flow_entries':'4000000'},
}

env.dpdk = {
#    host2: { 'huge_pages' : '75', 'coremask' : '0xff'},
    host3: { 'huge_pages' : '75', 'coremask' : '0xff'}
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
    '10.87.64.157': '10.87.122.116',
    '10.87.64.158': '10.87.122.117',
}


minimum_diskGB=32
env.test_repo_dir='/root/contrail-test1'
