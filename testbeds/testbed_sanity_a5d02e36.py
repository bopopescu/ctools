from fabric.api import env
import os

#Management ip addresses of hosts in the cluster
host1 = 'root@10.87.143.138'
host2 = 'root@10.87.143.133'
host3 = 'root@10.87.143.134'
host4 = 'root@10.87.143.135'
host5 = 'root@10.87.143.136'
host6 = 'root@10.87.143.137'

#External routers if any
ext_routers = [('montreal', '10.87.140.140')]

#Autonomous system number
router_asn = 64523

#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.84.24.64'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6 ],
    'cfgm': [host1, host2, host3],
    'openstack': [host1],
    'control': [host1, host2, host3],
    'compute': [host4, host5, host6],
    'collector': [host1, host2, host3],
    'webui': [host1, host2, host3],
    'database': [host1, host2, host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['a5d02e36','a5d02e37','a5d02e38','a5d02e39','a5d02e40','a5d02e41']
}

#Openstack admin password
env.openstack_admin_password = 'c0ntrail123'
env.physical_routers={
'montreal'     : {       'vendor': 'juniper',
                         'model' : 'mx',
                         'asn'   : '64515',
                         'name'  : 'montreal',
                         'ssh_username' : 'root',
                         'ssh_password' : 'Embe1mpls',
                         'mgmt_ip'  : '10.87.140.140',
                 }
}

env.password = 'c0ntrail123'
#Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

#For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
    host6: 'ubuntu',
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
   host1 : { 'ip': '192.168.12.1/24', 'gw' : '192.168.12.100', 'device':'enp2s0f1' },
   host2 : { 'ip': '192.168.12.2/24', 'gw' : '192.168.12.100', 'device':'enp2s0' },
   host3 : { 'ip': '192.168.12.3/24', 'gw' : '192.168.12.100', 'device':'enp2s0f1' },
   host4 : { 'ip': '192.168.12.4/24', 'gw' : '192.168.12.100', 'device':'enp2s0f1' },
   host5 : { 'ip': '192.168.12.5/24', 'gw' : '192.168.12.100', 'device':'enp2s0f1' },
   host6 : { 'ip': '192.168.12.6/24', 'gw' : '192.168.12.100', 'device':'enp2s0f1' },
}

#To disable installing contrail interface rename package
env.interface_rename = True

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

#storage_node_config = {
#    host2 : { 'disks' : ['/dev/sdc', '/dev/sdd'] , 'journal' : ['/dev/sdb'] },
#    host3 : { 'disks' : ['/dev/sdb'] , 'journal' : ['/dev/sdb'] },
#}
#if os.getenv('HA_TEST',None) == 'True':
env.ha = {
             'contrail_external_vip' : '10.87.129.225',
             'contrail_internal_vip' : '192.168.12.50',
	     'contrail_internal_virtual_router_id' : 113,
	     'contrail_external_virtual_router_id' : 114,
         }
ipmi_username = 'ADMIN'
ipmi_password = 'ADMIN'
env.hosts_ipmi = {
    '10.87.143.138': '10.87.129.41',
    '10.87.143.133': '10.87.129.24',
    '10.87.143.134': '10.87.129.26',
    '10.87.143.135': '10.87.129.28',
    '10.87.143.136': '10.87.129.44',
    '10.87.143.137': '10.87.129.39',
}
# HA Test configuration
ha_setup = 'True'
minimum_diskGB=32
env.mail_from='jebap@juniper.net'
env.mail_to='jebap@juniper.net'
multi_tenancy=True
env.encap_priority="'MPLSoUDP','MPLSoGRE','VXLAN'"
env.mail_server='10.84.24.64'
env.mail_port='4000'
#env.mx_gw_test=True
env.testbed_location='US'
env.interface_rename = False
env.image_web_server = '10.84.5.120'
env.log_scenario='Multi-Interface Sanity[mgmt, ctrl=data, CEPH]'
env.enable_lbaas = True
env.test = {
     'mail_to': 'dl-contrail-sw@juniper.net',
     'mail_server': '10.84.24.64',
     'mail_port': '4000',
     'image_web_server': '10.84.5.120',
     'log_scenario': 'Multi-Interface Sanity[mgmt, ctrl=data]',
           }
env.ntp_server = '10.84.5.100'
enable_ceilometer = True
ceilometer_polling_interval = 60


storage_replica_size = 2
env.test_repo_dir="/home/stack/centos_sanity/contrail-test"
