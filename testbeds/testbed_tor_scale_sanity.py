from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 ='root@10.87.121.68'
host2 ='root@10.87.121.69'
host3 ='root@10.87.121.70'
host4 ='root@10.87.121.71'
host5 ='root@10.87.121.72'
host6 ='root@10.87.121.73'
host7 ='root@10.87.121.74'
host8 ='root@10.87.121.75'
host9 ='root@10.87.121.76'
host10 ='root@10.87.121.77'


#External routers if any
#for eg.
ext_routers = [('5b7-mx80-2', '7.7.7.77')]
#ext_routers = []

#Autonomous system number
router_asn = 64513

#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.121.68'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1,host2,host3,host4,host5,host6,host7,host8,host9,host10],
    'cfgm': [host1,host2,host3],
    'openstack': [host1,host2,host3],
    'webui': [host1],
    'control': [host2,host3],
    'compute': [host4,host5,host6,host7,host8,host9,host10],
    'tsn': [host4,host5,host6,host7],
    'toragent': [host4,host5,host6,host7],
    'collector': [host2,host3],
    'database': [host1,host2,host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['5b7s1','5b7s2','5b7s3','5b7s4','5b7s5','5b7s6','5b7s7','5b7s8','5b7s9','5b7s10']
}
#Openstack admin password
env.openstack_admin_password = 'contrail123'

# Passwords of each host
# for passwordless login's no need to set env.passwords,
# instead populate env.key_filename in testbed.py with public key.
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
    host_build: 'c0ntrail123',
}

# SSH Public key file path for passwordless logins
# if env.passwords is not specified.  
#env.key_filename = '/root/.ssh/id_rsa.pub'

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
}
#env.orchestrator = 'openstack' #other values are 'vcenter', 'none' default:openstack

#ntp server the servers should point to
#env.ntp_server = 'ntp.juniper.net'

# OPTIONAL COMPUTE HYPERVISOR CHOICE:
#======================================
# Compute Hypervisor
#env.hypervisor = {
#    host5: 'docker',
#    host6: 'libvirt',
#    host10: 'docker',
#}
#  Specify the hypervisor to be provisioned in the compute node.(Default=libvirt)

# INFORMATION FOR DB BACKUP/RESTORE ..
#=======================================================
#Optional,Backup Host configuration if it is not available then it will put in localhost
#backup_node = 'root@2.2.2.2'

# Optional, Local/Remote location of backup_data path
# if it is not passed then it will use default path
#backup_db_path= ['/home/','/root/']G
#cassandra backup can be defined either "full" or "custom"
#full -> take complete snapshot of cassandra DB
#custom -> take snapshot except defined in skip_keyspace
#cassandra_backup='custom'  [ MUST OPTION]
#skip_keyspace=["ContrailAnalytics"]  IF cassandra_backup is selected as custom
#service token need to define to do  restore of backup data
#service_token = '53468cf7552bbdc3b94f'


#OPTIONAL ANALYTICS CONFIGURATION
#================================
# database_dir is the directory where cassandra data is stored
#
# If it is not passed, we will use cassandra's default
# /var/lib/cassandra/data
#
#database_dir = '<separate-partition>/cassandra'
#
# analytics_data_dir is the directory where cassandra data for analytics
# is stored. This is used to seperate cassandra's main data storage [internal
# use and config data] with analytics data. That way critical cassandra's
# system data and config data are not overrun by analytis data
#
# If it is not passed, we will use cassandra's default
# /var/lib/cassandra/data
#
#analytics_data_dir = '<separate-partition>/analytics_data'
#
# ssd_data_dir is the directory where cassandra can store fast retrievable
# temporary files (commit_logs). Giving cassandra an ssd disk for this
# purpose improves cassandra performance
#
# If it is not passed, we will use cassandra's default
# /var/lib/cassandra/commit_logs
#
#ssd_data_dir = '<seperate-partition>/commit_logs_data'

#following variables allow analytics data to have different TTL in cassandra database
#analytics_config_audit_ttl controls TTL for config audit logs
#analytics_statistics_ttl controls TTL for stats/control_data
#following parameter allows to specify minimum amount of disk space in the analytics
#database partition, if configured amount of space is not present, it will fail provisioning
#minimum_diskGB = 256

#OPTIONAL BONDING CONFIGURATION
#==============================
#Inferface Bonding
#bond= {
#    b7s31 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
#    b7s32 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
#    b7s33 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
#    b7s34 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
#    b7s35 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
#    b7s36 : { 'name': 'bond0', 'member': ['p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
#    b7s37 : { 'name': 'bond0', 'member': ['p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
#}

env.sriov = {
     host9 :[ {'interface' : 'p514p2', 'VF' : 25, 'physnets' : ['physnet1']}],
     host10 :[ {'interface' : 'p514p2', 'VF' : 25, 'physnets' : ['physnet1']}],
}

#OPTIONAL SEPARATION OF MANAGEMENT AND CONTROL + DATA and OPTIONAL VLAN INFORMATION
#==================================================================================
control_data = {
    host1 : { 'ip': '172.17.90.1/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host2 : { 'ip': '172.17.90.2/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host3 : { 'ip': '172.17.90.3/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host4 : { 'ip': '172.17.90.4/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host5 : { 'ip': '172.17.90.5/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host6 : { 'ip': '172.17.90.6/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host7 : { 'ip': '172.17.90.7/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host8 : { 'ip': '172.17.90.8/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host9 : { 'ip': '172.17.90.9/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host10 : { 'ip': '172.17.90.10/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
}

#OPTIONAL STATIC ROUTE CONFIGURATION  
#===================================  
static_route  = {
    host1 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],
    host2 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],  
    host3 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],
             
    host4 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],
    host5 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],
    host6 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],
    host7 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],
    host8 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],
    host9 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],
    host10 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],
}


# VIP
env.ha = {
    'internal_vip' : '172.17.90.90',
    'external_vip' : '10.87.121.90'
}

# OPTIONAL vrouter limit parameter
# ==================================
env.vrouter_module_params = {
     host4:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host5:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host6:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host8:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host9:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host10:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
}

env.tor_agent = {host4:[{
                    'tor_ip':'172.18.90.1',
                    'tor_agent_id':'1',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4321',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.17.90.4',
                    'tor_tsn_name':'5b7s4',
                    'tor_name':'5b7-qfx2',
                    'tor_tunnel_ip':'34.34.34.34',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1234',
                    'tor_agent_ovs_ka': '10000',
                       },
                       {
                    'tor_ip':'172.18.90.2',
                    'tor_agent_id':'2',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4322',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.17.90.4',
                    'tor_tsn_name':'5b7s4',
                    'tor_name':'5b7-qfx3',
                    'tor_tunnel_ip':'33.33.33.33',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1233',
                    'tor_agent_ovs_ka': '10000',
                       },
                       ],
                   
                 host5:[{
                    'tor_ip':'172.18.90.1',
                    'tor_agent_id':'1',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4321',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.17.90.5',
                    'tor_tsn_name':'5b7s5',
                    'tor_name':'5b7-qfx2',
                    'tor_tunnel_ip':'34.34.34.34',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1234',
                    'tor_agent_ovs_ka': '10000',
                       },
                       {
                    'tor_ip':'172.18.90.2',
                    'tor_agent_id':'2',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4322',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.17.90.5',
                    'tor_tsn_name':'5b7s5',
                    'tor_name':'5b7-qfx3',
                    'tor_tunnel_ip':'33.33.33.33',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1233',
                    'tor_agent_ovs_ka': '10000',
                       },
                       ],
                 host6:[{
                    'tor_ip':'172.18.90.3',
                    'tor_agent_id':'3',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4323',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.17.90.6',
                    'tor_tsn_name':'5b7s6',
                    'tor_name':'5b7-qfx4',
                    'tor_tunnel_ip':'32.32.32.32',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1231',
                    'tor_agent_ovs_ka': '10000',
                       },
                       {
                    'tor_ip':'172.18.90.4',
                    'tor_agent_id':'4',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4324',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.17.90.6',
                    'tor_tsn_name':'5b7s6',
                    'tor_name':'5b7-qfx5',
                    'tor_tunnel_ip':'31.31.31.31',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1230',
                    'tor_agent_ovs_ka': '10000',
                       },
                       ],
 
                 host7:[{
                    'tor_ip':'172.18.90.3',
                    'tor_agent_id':'3',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4323',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.17.90.7',
                    'tor_tsn_name':'5b7s7',
                    'tor_name':'5b7-qfx4',
                    'tor_tunnel_ip':'32.32.32.32',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1231',
                    'tor_agent_ovs_ka': '10000',
                       },
                       {
                    'tor_ip':'172.18.90.4',
                    'tor_agent_id':'4',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4324',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.17.90.7',
                    'tor_tsn_name':'5b7s7',
                    'tor_name':'5b7-qfx5',
                    'tor_tunnel_ip':'31.31.31.31',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1230',
                    'tor_agent_ovs_ka': '10000',
                       },
                       ] 
                }                
                   

env.tor_hosts={
'172.18.90.1': [{'tor_port': 'xe-0/0/46',
                    'host_port' : 'p2p2',
                    'mgmt_ip' : '10.87.65.143',
                    'username' : 'root',
                    'password' : 'c0ntrail123',
                  }],
'172.18.90.2': [{'tor_port': 'xe-0/0/46',
                    'host_port' : 'p2p1',
                    'mgmt_ip' : '10.87.65.143',
                    'username' : 'root',
                    'password' : 'c0ntrail123',
                  }]
}

env.physical_routers={
'5b7-mx80-2'          : {     
                     'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64513',
                     'name'  : '5b7-mx80-2',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'   : '172.18.90.77',
                     'tunnel_ip' : '7.7.7.77',
                     'ports' : [],
                     'type'  : 'router',
                 },
'5b7-qfx2'       : {
                     'vendor': 'juniper',
                     'model' : 'qfx5100',
                     'asn'   : '64513',
                     'name'  : '5b7-qfx2',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '172.18.90.1',
                     'tunnel_ip' : '34.34.34.34',
                     'ports' : ['xe-0/0/46'],
                     'type'  : 'tor',
},
'5b7-qfx3'       : { 
                     'vendor': 'juniper',
                     'model' : 'qfx5100',
                     'asn'   : '64513',
                     'name'  : '5b7-qfx3',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '172.18.90.2',
                     'tunnel_ip' : '33.33.33.33',
                     'ports' : ['xe-0/0/46'],
                     'type'  : 'tor',
},
}

do_parallel = True
env.mail_from='chhandak@juniper.net'
env.mail_to='chhandak@juniper.net'
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.test_repo_dir='/root/contrail-test'
env.ca_cert_file='/root/cacert.pem'
