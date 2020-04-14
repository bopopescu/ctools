from fabric.api import env
import os

#Management ip addresses of hosts in the cluster
host1 = 'root@10.87.143.10'
host2 = 'root@10.87.143.12'
host3 = 'root@10.87.143.16'
host4 = 'root@10.87.143.18'
host5 = 'root@10.87.143.35'
host6 = 'root@10.87.143.37'
host7 = 'root@10.87.143.90'
host8 = 'root@10.87.143.92'
host9 = 'root@10.87.143.94'
host10 = 'root@10.87.143.84'
host11 = 'root@10.87.143.100'

#External routers if any
ext_routers = [('montreal', '10.87.140.140')]

#Autonomous system number
router_asn = 64515

#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.84.24.64'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6, host7, host8, host9, host10, host11],
    'cfgm': [host4, host5, host6],
    'openstack': [host1, host2, host3],
    'control': [host4, host5, host6],
    'compute': [host10, host11],
    'collector': [host4, host5, host6],
    'webui': [host4, host5, host6],
    'database': [host7, host8, host9],
    'build': [host_build],
}

env.hostnames = {
    'all': ['a5d11e42','a5d06e38','a5d10e33','a5d10e34','a5d11e37','a5d11e38','a5d11e14','a5d11e13','a5d11e12','a5d11e35','a5d11e09']
}

env.openstack = {
    'manage_amqp':'yes'
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
    host7: 'c0ntrail123',
    host8: 'c0ntrail123',
    host9: 'c0ntrail123',
    host10: 'c0ntrail123',
    host11: 'c0ntrail123',
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
    host7: 'ubuntu',
    host8: 'ubuntu',
    host9: 'ubuntu',
    host10: 'ubuntu',
    host11: 'ubuntu',
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
   host1 : { 'ip': '192.168.11.1/24', 'gw' : '192.168.11.100', 'device':'p5p2' },
   host2 : { 'ip': '192.168.11.2/24', 'gw' : '192.168.11.100', 'device':'p5p2' },
   host3 : { 'ip': '192.168.11.3/24', 'gw' : '192.168.11.100', 'device':'p5p2' },
   host4 : { 'ip': '192.168.11.4/24', 'gw' : '192.168.11.100', 'device':'p5p2' },
   host5 : { 'ip': '192.168.11.5/24', 'gw' : '192.168.11.100', 'device':'p5p2' },
   host6 : { 'ip': '192.168.11.6/24', 'gw' : '192.168.11.100', 'device':'p5p2' },
   host7 : { 'ip': '192.168.11.7/24', 'gw' : '192.168.11.100', 'device':'p51p1' },
   host8 : { 'ip': '192.168.11.8/24', 'gw' : '192.168.11.100', 'device':'p51p1' },
   host9 : { 'ip': '192.168.11.9/24', 'gw' : '192.168.11.100', 'device':'p51p1' },
   host10 : { 'ip': '192.168.11.10/24', 'gw' : '192.168.11.100', 'device':'p51p2' },
   host11 : { 'ip': '192.168.11.11/24', 'gw' : '192.168.11.100', 'device':'p51p1' },
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
             'external_vip' : '10.87.143.50',
             'internal_vip' : '192.168.11.50',
	     'internal_virtual_router_id' : 111,
	     'external_virtual_router_id' : 112,
             'contrail_external_vip' : '10.87.143.151',
             'contrail_internal_vip' : '192.168.11.51',
	     'contrail_internal_virtual_router_id' : 113,
	     'contrail_external_virtual_router_id' : 114,
         }
ipmi_username = 'root'
ipmi_password = 'superuser'
env.hosts_ipmi = {
    '10.87.143.84': '10.87.143.85',
    '10.87.143.90': '10.87.143.89',
    '10.87.143.92': '10.87.143.91',
    '10.87.143.94': '10.87.143.93',
    '10.87.143.100': '10.87.143.99',
    '10.87.143.10': '10.87.143.9',
    '10.87.143.12': '10.87.143.11',
    '10.87.143.16': '10.87.143.15',
    '10.87.143.18': '10.87.143.17',
    '10.87.143.35': '10.87.143.34',
    '10.87.143.37': '10.87.143.36',
}
# HA Test configuration
ha_setup = 'True'
minimum_diskGB=32
env.mail_from='dl-contrail-sw@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
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
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}


storage_replica_size = 2
env.test_repo_dir="/home/stack/ubuntu_sanity/contrail-test"
