from fabric.api import env
import os
#Management ip addresses of hosts in the cluster
host1 = 'root@10.87.129.43'
host2 = 'root@10.87.129.27'
host3 = 'root@10.87.129.25'
host4 = 'root@10.87.129.23'
host5 = 'root@10.87.141.28'
#External routers if any
ext_routers = [('montreal', '10.87.140.140')]

#Autonomous system number
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = "10.87.129.224/27"


#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.141.90'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3, host4, host5],
    'cfgm': [host1,host2,host3],
    'openstack': [host1,host2,host3],
    'control': [host1,host2,host3],
    'compute': [host4,host5],
    'collector': [host1,host2,host3],
    'webui': [host1,host2,host3],
    'database': [host1,host2,host3],
    'storage-main': [host1,host2,host3],
    'storage-compute': [ host4, host5],
    'build': [host_build],
}

env.hostnames = {
    'all': ['esbu-mflab-lnx-c08', 'esbu-mflab-lnx-c03', 'esbu-mflab-lnx-c02','esbu-mflab-lnx-c01',"cmbu-gravity-09" ]
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
    host5: 'n1keenA',
    host_build: 'n1keenA',
}

#For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
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
   host1 : { 'ip': '16.0.0.2/24', 'gw' : '16.0.0.1', 'device':'p2p2' },
   host2 : { 'ip': '16.0.0.3/24', 'gw' : '16.0.0.1', 'device':'p2p2' },
   host3 : { 'ip': '16.0.0.4/24', 'gw' : '16.0.0.1', 'device':'p2p2' },
   host4 : { 'ip': '16.0.0.5/24', 'gw' : '16.0.0.1', 'device':'p2p1' },
   host5 : { 'ip': '16.0.0.6/24', 'gw' : '16.0.0.1', 'device':'p2p2' },
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
#if os.getenv('HA_TEST',None) == 'True':

env.ha = {
    'internal_vip' : '16.0.0.92',
    'external_vip' : '10.87.141.92',

}

# HA Test configuration
#ha_setup = 'True'
#    ipmi_username = 'ADMIN'
#    ipmi_password = 'ADMIN'
#    env.hosts_ipmi = {
#        '10.87.140.213': '10.87.140.214',
#        '10.87.129.224': '10.87.129.225',
#        '10.87.129.226': '10.87.129.233',
#        '10.87.141.26' : '10.87.141.25',
#    }
minimum_diskGB=128
env.test_repo_dir="/home/stack/ubuntu_sanity/contrail-test"
env.mail_from='vivekgarg@juniper.net'
env.mail_to='vivekgarg@juniper.net'
multi_tenancy=True
env.encap_priority="'MPLSoUDP','MPLSoGRE','VXLAN'"
env.mail_server='10.84.24.64'
env.mail_port='4000'
env.mx_gw_test=True
env.testbed_location='US'
env.interface_rename = False
env.image_web_server = '10.84.5.120'
env.log_scenario='Multi-Interface Sanity[mgmt, ctrl=data, CEPH]'

