from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.87.140.197'
host2 = 'root@10.87.140.198'
host3 = 'root@10.87.140.199'
host4 = 'root@10.87.140.200'

#External routers if any
ext_routers = [('montreal', '10.87.140.185')]

#Autonomous system number
router_asn = 64512

#Host from which the fab commands are triggered to install and provision
host_build = 'stack@10.87.140.230'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3,host4],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1],
    'compute': [host2, host3,host4],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'storage-main': [host1],
    'storage-compute': [host2, host3,host4],
    'build': [host_build],
}

env.hostnames = {
    'all': ['cmbu-ceph-perf1','cmbu-ceph-perf2','cmbu-ceph-perf3','cmbu-ceph-perf4']
}

#Openstack admin password
env.openstack_admin_password = 'n1keenA'

env.password = 'n1keenA'
#Passwords of each host
env.passwords = {
    host1: 'n1keenA',
    host2: 'n1keenA',
    host3: 'n1keenA',
    host4: 'n1keenA',
    host_build: 'stack@123',
}

#For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
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
   host1 : { 'ip': '5.0.0.1/24', 'gw' : '5.0.0.1', 'device':'HOST1_IFACE' },
   host2 : { 'ip': '5.0.0.2/24', 'gw' : '5.0.0.1', 'device':'HOST2_IFACE' },
   host3 : { 'ip': '5.0.0.3/24', 'gw' : '5.0.0.1', 'device':'HOST3_IFACE' },
   host4 : { 'ip': '5.0.0.4/24', 'gw' : '5.0.0.1', 'device':'HOST4_IFACE' },
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

storage_node_config = {

    host2 : { 'disks' : ['/dev/sdc', '/dev/sdd'], 
         'ssd-disks': ['/dev/sde'], 
         'local-disks' : ['/dev/sdf'], 
         'nfs' : ['10.87.129.119:/localstore/ceph/multibackend_mount1', '10.87.129.119:/localstore/ceph/multibackend_mount2'],
         'journal' : ['/dev/sdb']
    },
    host3 : { 'disks' : ['/dev/sdc', '/dev/sdd','/dev/sde','/dev/sdf'] , 'journal' : ['/dev/sdb'] },
    host4 : { 'disks' : ['/dev/sdc', '/dev/sdd','/dev/sde','/dev/sdf'] , 'journal' : ['/dev/sdb'] },
}

live_migration = True
ceph_nfs_livem = True
ceph_nfs_livem_subnet = '192.168.101.253/24'
ceph_nfs_livem_image =  '/store/livemnfs.qcow2'
ceph_nfs_livem_host = host2

storage_replica_size=2
