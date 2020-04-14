from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@172.16.170.5'
host2 = 'root@172.16.170.6'
host3 = 'root@172.16.170.7'
host4 = 'root@172.16.170.8'
host5 = 'root@172.16.170.9'
host6 = 'root@172.16.170.10'
host7 = 'root@172.16.170.11'
host8 = 'root@172.16.170.12'
host9 = 'root@172.16.170.13'
host10 = 'root@172.16.170.14'
host11 = 'root@172.16.170.15'
host12 = 'root@172.16.170.16'
host13 = 'root@172.16.170.17'

#External routers if any
ext_routers = [('montreal', '10.87.140.185')]

#Autonomous system number
router_asn = 64512

#Host from which the fab commands are triggered to install and provision
host_build = 'root@172.16.170.5'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3,host4,host5,host6,host7,host8,host9,host10,host11,host12,host13],
    'cfgm': [host1,host2,host3],
    'openstack': [host1,host2,host3],
    'control': [host1,host2,host3],
    'compute': [host4, host5,host6,host7,host8,host9,host10,host11,host12,host13],
    'collector': [host1,host2,host3],
    'webui': [host1],
    'database': [host1,host2,host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['csol2-node5','csol2-node6','csol2-node7','csol2-node8','csol2-node9','csol2-node10','csol2-node11','csol2-node12','csol2-node13','csol2-node14','csol2-node15','csol2-node16','csol2-node17']
}

#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'contrail123'
#Passwords of each host
env.passwords = {
    host1: 'contrail123',
    host2: 'contrail123',
    host3: 'contrail123',
    host4: 'contrail123',
    host5: 'contrail123',
    host6: 'contrail123',
    host7: 'contrail123',
    host8: 'contrail123',
    host9: 'contrail123',
    host10: 'contrail123',
    host11: 'contrail123',
    host12: 'contrail123',
    host13: 'contrail123',
    host_build: 'contrail123',
}

#For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
    host6: 'ubuntu',
    host7: 'ubuntu',
    host8: 'ubuntu',
    host9: 'ubuntu',
    host10: 'ubuntu',
    host11: 'ubuntu',
    host12: 'ubuntu',
    host13: 'ubuntu',
}

#OPTIONAL BONDING CONFIGURATION
#==============================
#Inferface Bonding
#OPTIONAL BONDING CONFIGURATION
#==============================
#Inferface Bonding
#bond= {
#    host2 : { 'name': 'bond0', 'member': ['p2p0p0','p2p0p1','p2p0p2','p2p0p3'], 'mode':'balance-xor' },
#    host5 : { 'name': 'bond0', 'member': ['p4p0p0','p4p0p1','p4p0p2','p4p0p3'], 'mode':'balance-xor' },
#}

#OPTIONAL SEPARATION OF MANAGEMENT AND CONTROL + DATA
#====================================================
#Control Interface
#control = {
#    host1 : { 'ip': '10.87.140.197/22', 'gw' : '10.87.159.254', 'device':'eth0' },
#    host2 : { 'ip': '10.87.140.198/22', 'gw' : '10.87.159.254', 'device':'eth0' },
#    host3 : { 'ip': '10.87.140.199/22', 'gw' : '10.87.159.254', 'device':'eth0' },
#}

#Data Interface
control_data = {
   host1 : { 'ip': '172.16.180.5/24',  'gw' : '172.16.180.253', 'device':'bond0' },
   host2 : { 'ip': '172.16.180.6/24',  'gw' : '172.16.180.253', 'device':'bond0' },
   host3 : { 'ip': '172.16.180.7/24',  'gw' : '172.16.180.253', 'device':'bond0' },
   host4 : { 'ip': '172.16.180.8/24',  'gw' : '172.16.180.253', 'device':'bond0' },
   host5 : { 'ip': '172.16.180.9/24',  'gw' : '172.16.180.253', 'device':'bond0' },
   host6 : { 'ip': '172.16.180.10/24',  'gw' : '172.16.180.253', 'device':'bond0' },
   host7 : { 'ip': '172.16.180.11/24', 'gw' : '172.16.180.253', 'device':'bond0' },
   host8 : { 'ip': '172.16.180.12/24', 'gw' : '172.16.180.253', 'device':'bond0' },
   host9 : { 'ip': '172.16.180.13/24', 'gw' : '172.16.180.253', 'device':'bond0' },
   host10 : { 'ip': '172.16.180.14/24', 'gw' : '172.16.180.253', 'device':'bond0' },
   host11 : { 'ip': '172.16.180.15/24', 'gw' : '172.16.180.253', 'device':'bond0' },
   host12 : { 'ip': '172.16.180.16/24', 'gw' : '172.16.180.253', 'device':'bond0' },
   host13 : { 'ip': '172.16.180.17/24', 'gw' : '172.16.180.253', 'device':'bond0' },
}

#To disable installing contrail interface rename package
env.interface_rename = False

#To use existing service_token
#service_token = 'your_token'

#Specify keystone IP
#keystone_ip = '1.1.1.1'

#Specify Keystone admin user if not same as  admin
#keystone_admin_user = 'nonadmin'

#Specify Keystone admin password if not same as env.openstack_admin_password
#keystone_admin_password = 'contrail123'

#Specify Region Name
#region_name = 'RegionName'

#To enable multi-tenancy feature
#multi_tenancy = True

#To enable haproxy feature
#haproxy = True

#To Enable prallel execution of task in multiple nodes
#do_parallel = True

# To configure the encapsulation priority. Default: MPLSoGRE
#env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"

#Ceph related

