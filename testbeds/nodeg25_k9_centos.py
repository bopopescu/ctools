from fabric.api import env

host1 = 'root@10.204.217.65'
host2 = 'root@10.204.217.66'
host3 = 'root@10.204.217.67'
host4 = 'root@10.204.216.230'
host5 = 'root@10.204.216.228'
host6 = 'root@10.204.216.229'

ext_routers = [('hooper', '40.47.1.1')]
router_asn = 64512
public_vn_rtgt = 19006
public_vn_subnet = "10.204.219.104/29"

host_build = 'sandipd@10.204.216.4'


env.roledefs = {
#    'all': [host1, host2, host3, host5,host6],
    'all': [host1, host2, host3,host4, host5,host6],
    'cfgm': [host1,host2,host3],
    'webui': [host1],
    'openstack': [host1],
    'control': [host2, host3],
    'collector': [host1],
    'database': [host1],
    'compute': [host4, host5,host6],
    #'compute': [host5,host6],
    'build': [host_build]
}

env.hostnames = {
    'all': ['nodeg25', 'nodeg26', 'nodeg27', 'nodek10', 'nodek8', 'nodek9']
    #'all': ['nodeg25', 'nodeg26', 'nodeg27', 'nodek8', 'nodek9']
}
#env.interface_rename = False
#

#Inferface Bonding
bond= {
    host4 : { 'name': 'bond0', 'member': ['eth4','eth3'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host5 : { 'name': 'bond0', 'member': ['eth3','eth2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
}

control_data = {
    host1 : { 'ip': '40.43.1.5/24', 'gw' : '40.43.1.1', 'device':'eth1'},
    host2 : { 'ip': '40.43.1.6/24', 'gw' : '40.43.1.1', 'device':'eth1' },
    host3 : { 'ip': '40.43.1.7/24', 'gw' : '40.43.1.1', 'device':'eth1' },
    host4 : { 'ip': '40.41.1.5/24', 'gw' : '41.41.1.2', 'device':'bond0','vlan': '4001' },
    host5 : { 'ip': '40.40.40.5/24', 'gw' : '40.40.40.1', 'device':'bond0' ,'vlan': '4000'},
    host6 : { 'ip': '40.40.40.6/24','gw' : '40.40.40.1', 'device':'eth2','vlan': '4000' },
}

static_route  = {
    host1 : [{ 'ip': '40.40.0.0', 'netmask' : '255.248.0.0', 'gw':'40.43.1.1', 'intf': 'eth1' }
    ],
    host2 : [{ 'ip': '40.40.0.0', 'netmask' : '255.248.0.0', 'gw':'40.43.1.1', 'intf': 'eth1' }
    ],
    host3 : [{ 'ip': '40.40.0.0', 'netmask' : '255.248.0.0', 'gw':'40.43.1.1', 'intf': 'eth1' }
    ],
    host4 : [{ 'ip': '40.40.0.0', 'netmask' : '255.248.0.0', 'gw':'40.41.1.1', 'intf': 'bond0.vlan4001' }
    ],
    host5 : [{ 'ip': '40.40.0.0', 'netmask' : '255.248.0.0', 'gw':'40.40.40.1', 'intf': 'bond0.vlan4000' }
    ],
    host6 : [{ 'ip': '40.40.0.0', 'netmask' : '255.248.0.0', 'gw':'40.40.40.1', 'intf': 'eth2.vlan4000' }
    ],
}

env.openstack_admin_password = 'contrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
    host_build: 'stack@123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    host6:'ubuntu',
}
minimum_diskGB=32
env.test_repo_dir='/home/stack/multi_interface_parallel/ubuntu/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='sandipd@juniper.net'
multi_tenancy=True
env.interface_rename = False
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario='Five node sanity'

env.enable_lbaas = True
