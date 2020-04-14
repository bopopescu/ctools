from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

# Management ip addresses of hosts in the cluster
host1 = 'root@10.87.66.133'  
host2 = 'root@10.87.66.134' 
host3 = 'root@10.87.66.135'  
#host4 = 'root@10.87.66.129' #Netronome 40G 
host4 = 'root@10.87.66.130' #Netronome 40G 
host5 = 'root@10.87.66.131' #Netronome 20G 
host6 = 'root@10.87.66.132' #Netronome 20G 
#host8 = 'root@10.87.66.136' 


# Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.66.133'  

env.ha = {
    'internal_vip'   : '5.5.5.140',               #Internal Virtual IP of the openstack HA Nodes.
    'external_vip'   : '10.87.66.140',               #External Virtual IP of the openstack HA Nodes.
}



# External routers if any
ext_routers = []

#env.ns_agilio_vrouter = {
#    host4: {'name' : 'nfp_p0', 'accelerated' : True},
#    host5: {'name' : 'nfp_p0', 'accelerated' : True},
#    host5: {'name' : 'nfp_p0', 'accelerated' : True},
#    host5: {'name' : 'nfp_p0', 'accelerated' : True},
#    host6: {'name' : 'nfp_p0', 'accelerated' : True},
#}

# Setup Netronome Agilio vRouter on specified nodes
env.ns_agilio_vrouter = {
    host4: {'huge_page_alloc': '24G', 'huge_page_size': '1G',  'coremask': '2,4', 'pinning_mode': 'auto:combine'},
    host5: {'huge_page_alloc': '24G', 'huge_page_size': '1G',  'coremask': '2,4', 'pinning_mode': 'auto:combine'},
    host6: {'huge_page_alloc': '24G', 'huge_page_size': '1G',  'coremask': '2,4', 'pinning_mode': 'auto:combine'}
}

# Autonomous system number
router_asn = 64512
public_vn_rtgt = 12345
public_vn_subnet = "10.84.42.0/24"

# Role definition of the hosts.
env.roledefs = {
    #'all': [host1, host2, host3,host4, host5, host6],
    #'all': [host1, host2, host3, host4, host5,host6,host7,host8],
    'all': [host1, host2, host3, host4, host5,host6],
    'cfgm': [host1,host2,host3],
    'openstack': [host1,host2,host3],
    'control': [host2,host3],
    'compute': [host4,host5,host6],
    'collector': [host1],
    'webui': [host1],
    'database': [host1,host2,host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['5b8s5','5b8s6','5b8s7','5b8s2','5b8s3', '5b8s4']
}

bond= {
    host5 : { 'name': 'bond0', 'member': ['nfp_p0','nfp_p1'], 'mode':'802.3ad','xmit_hash_policy': 'layer3+4' },
    host6 : { 'name': 'bond0', 'member': ['nfp_p0','nfp_p1'], 'mode':'802.3ad','xmit_hash_policy': 'layer3+4' },
    #host8 : { 'name': 'bond0', 'member': ['p1p1','p1p2'], 'mode':'802.3ad' },
}

control_data = {
    host1 : { 'ip': '5.5.5.232/24', 'gw' : '5.5.5.1', 'device' : 'p514p1'},
    host2 : { 'ip': '5.5.5.233/24', 'gw' : '5.5.5.1', 'device' : 'p514p1'},
    host3 : { 'ip': '5.5.5.234/24', 'gw' : '5.5.5.1', 'device' : 'p514p1'},
    host4 : { 'ip': '5.5.5.235/24', 'gw' : '5.5.5.1', 'device' : 'nfp_p0'},
    host5 : { 'ip': '5.5.5.236/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
    host6 : { 'ip': '5.5.5.237/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
}

static_route  = {
}


# Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',

    host_build: 'c0ntrail123',
}

env.vrouter_module_params = {
}

env.dpdk = {
}

# For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
    host6: 'ubuntu',
    #host7: 'ubuntu',
    #host8: 'ubuntu',
}
do_parallel = True

# HA Test configuration
ipmi_username = 'ADMIN'
ipmi_password = 'ADMIN'

env.hosts_ipmi = {
}


minimum_diskGB=32
env.test_repo_dir='/root/contrail-test'

#Openstack admin password
env.openstack_admin_password = 'contrail123'
