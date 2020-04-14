from fabric.api import env
import os

#Management ip addresses of hosts in the cluster
host1 ='root@10.87.70.65'
host2 ='root@10.87.70.66'
host3 ='root@10.87.70.67'
host4 ='root@10.87.70.68'
host5 ='root@10.87.70.69'
host6 ='root@10.87.70.70'
host7 ='root@10.87.70.71'
host8 ='root@10.87.70.72'
host9 ='root@10.87.70.73'
host10 ='root@10.87.70.74'
host11 ='root@10.87.70.75'
host12 ='root@10.87.70.76'
host13 ='root@10.87.70.77'
host14 ='root@10.87.70.78'

host15 ='root@10.87.70.31'
host16 ='root@10.87.70.32'

kvm_5c1s13-node4 ='root@10.87.70.28'
kvm_5c1s15-node1 ='root@10.87.70.29'
kvm_5c1s15-node2 ='root@10.87.70.30'

reimage_param = os.getenv('REIMAGE_PARAM', 'ubuntu-14.04.4')

vm_node_details = {
    'default': {
                'image_dest' : '/mnt/disk1/images/',
                'disk_format' : 'qcow2',
                'image_source' : 'http://10.84.5.120/images/node_vm_images/%s-256G.img.gz' % (reimage_param),
                },
    host1 : {
                'name' : '5c1s13-node4-vm1',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s13-node4,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:13:04:01', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host2 : {
                'name' : '5c1s13-node4-vm2',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s13-node4,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:13:04:02', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host3 : {
                'name' : '5c1s13-node4-vm3',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s13-node4,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:13:04:03', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host4 : {
                'name' : '5c1s13-node4-vm4',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s13-node4,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:13:04:04', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host5 : {
                'name' : '5c1s15-node1-vm1',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s15-node1,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:15:01:01', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host6 : {
                'name' : '5c1s15-node1-vm2',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s15-node1,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:15:01:02', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host7 : {
                'name' : '5c1s15-node1-vm3',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s15-node1,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:15:01:03', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host8 : {
                'name' : '5c1s15-node1-vm4',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s15-node1,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:15:01:04', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host9 : {
                'name' : '5c1s15-node1-vm5',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s15-node1,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:15:01:05', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host10 : {
                'name' : '5c1s15-node2-vm1',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s15-node2,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:15:02:01', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host11 : {
                'name' : '5c1s15-node2-vm2',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s15-node2,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:15:02:02', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host12 : {
                'name' : '5c1s15-node2-vm3',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s15-node2,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:15:02:03', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host13 : {
                'name' : '5c1s15-node2-vm4',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s15-node2,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:15:02:04', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            },
    host14 : {
                'name' : '5c1s15-node2-vm5',
                'ram' : '32768',
                'vcpus' : '4',
                'server': kvm_5c1s15-node2,
                'network' : [{'bridge' : 'br0', 'mac':'62:53:55:15:02:05', 'model':'virtio'},
                             {'bridge' : 'br1', 'model':'virtio'}
                            ],
            }
}

#External routers if any
#for eg.
ext_routers = [('5c1-mx80-1', '7.7.7.77')]
#ext_routers = []

#Autonomous system number
router_asn = 64513

#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.70.66'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1,host2,host3,host4,host5,host6,host7,host8,host9,host10,host11,host12,host13,host14,host15,host16],
    'openstack': [host1,host5,host10],
    'contrail-controller': [host2,host6,host11],
    'contrail-compute': [host9,host14,host17,host18],
    'tsn': [host9,host14],
    'contrail-lb': [host1],
    'contrail-analytics': [host3,host7,host12],
    'contrail-analyticsdb': [host4,host8,host13],
    'build': [host_build],
}

env.hostnames = {
    'all': ['5c1s13-node4-vm1','5c1s13-node4-vm2','5c1s13-node4-vm3','5c1s13-node4-vm4','5c1s15-node1-vm1','5c1s15-node1-vm2','5c1s15-node1-vm3','5c1s15-node1-vm4','5c1s15-node1-vm5','5c1s15-node2-vm1','5c1s15-node2-vm2','5c1s15-node2-vm3','5c1s15-node2-vm4','5c1s15-node2-vm5','5c1s15-node3','5c1s15-node4']
}
#Openstack admin password
env.openstack_admin_password = 'c0ntrail123'

env.openstack = {
    'manage_amqp': "true"
}

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
    host11: 'c0ntrail123',
    host12: 'c0ntrail123',
    host13: 'c0ntrail123',
    host14: 'c0ntrail123',
    host15: 'c0ntrail123',
    host16: 'c0ntrail123',
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
    host11: 'ubuntu',
    host12: 'ubuntu',
    host13: 'ubuntu',
    host14: 'ubuntu',
    host15: 'ubuntu',
    host16: 'ubuntu',
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
bond= {
    5c1s15-node3 : { 'name': 'bond0', 'member': ['eth0', 'eth2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    5c1s15-node4 : { 'name': 'bond0', 'member': ['eth0', 'eth2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
}

#env.sriov = {
#     host16 :[ {'interface' : 'p514p2', 'VF' : 25, 'physnets' : ['physnet1']}],
#     host17 :[ {'interface' : 'p514p2', 'VF' : 25, 'physnets' : ['physnet1']}],
#}

#OPTIONAL SEPARATION OF MANAGEMENT AND CONTROL + DATA and OPTIONAL VLAN INFORMATION
#==================================================================================
control_data = {
    host1 : { 'ip': '172.16.90.1/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host2 : { 'ip': '172.16.90.2/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host3 : { 'ip': '172.16.90.3/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host4 : { 'ip': '172.16.90.4/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host5 : { 'ip': '172.16.90.5/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host6 : { 'ip': '172.16.90.6/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host7 : { 'ip': '172.16.90.7/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host8 : { 'ip': '172.16.90.8/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host9 : { 'ip': '172.16.90.9/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host10 : { 'ip': '172.16.90.10/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host11 : { 'ip': '172.16.90.11/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host12 : { 'ip': '172.16.90.12/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host13 : { 'ip': '172.16.90.13/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host14 : { 'ip': '172.16.90.14/24', 'gw' : '172.16.90.254', 'device':'eth1' },
    host15 : { 'ip': '172.16.90.15/24', 'gw' : '172.16.90.254', 'device':'bond0' },
    host16 : { 'ip': '172.16.90.16/24', 'gw' : '172.16.90.254', 'device':'bond0' },
}

#OPTIONAL STATIC ROUTE CONFIGURATION  
#===================================  
static_route  = {
    host1 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host2 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],  
    host3 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host4 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host5 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host6 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host7 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host8 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host9 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host10 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host11 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host12 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host13 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host14 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'eth1' }],
    host15 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' }],
    host16 : [{ 'ip': '172.16.91.0', 'netmask' : '255.255.255.0', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' },
             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.16.90.254', 'intf': 'bond0' }],
}


# VIP
env.ha = {
    'contrail_internal_vip' : '172.16.90.20',
    'contrail_external_vip' : '10.87.70.80',
    'internal_vip' : '172.16.90.91',
    'external_vip' : '10.87.70.79'
}

# OPTIONAL vrouter limit parameter
# ==================================
env.vrouter_module_params = {
     host9:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host14:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host15:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host16:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
}

env.tor_agent = {host9:[{
                    'tor_ip':'172.16.91.1',
                    'tor_agent_id':'1',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4321',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.16.90.9',
                    'tor_tsn_name':'5c1s15-node1-vm5',
		    'tor_agent_name':'5c1s15-node1-vm5-1',
                    'tor_name':'5c1-qfx5',
                    'tor_tunnel_ip':'34.34.34.34',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1234',
                    'tor_agent_ovs_ka': '10000',
                       },
                       {
                    'tor_ip':'172.16.91.2',
                    'tor_agent_id':'2',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4322',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.16.90.14',
                    'tor_tsn_name':'5c1s15-node1-vm5',
		    'tor_agent_name':'5c1s15-node1-vm5-2',
                    'tor_name':'5c1-qfx-6',
                    'tor_tunnel_ip':'33.33.33.33',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1233',
                    'tor_agent_ovs_ka': '10000',
                       },
                       ],
                   
                 host14:[{
                    'tor_ip':'172.16.91.1',
                    'tor_agent_id':'1',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4321',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.16.90.14',
                    'tor_tsn_name':'5c1s15-node2-vm5',
		    'tor_agent_name':'5c1s15-node2-vm5-1',
                    'tor_name':'5c1-qfx-6',
                    'tor_tunnel_ip':'34.34.34.34',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1234',
                    'tor_agent_ovs_ka': '10000',
                       },
                       {
                    'tor_ip':'172.16.91.2',
                    'tor_agent_id':'2',
                    'tor_type':'ovs',
                    'tor_ovs_port':'4322',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.16.90.14',
                    'tor_tsn_name':'5c1s15-node2-vm5',
		    'tor_agent_name':'5c1s15-node2-vm5-2',
                    'tor_name':'5c1-qfx-6',
                    'tor_tunnel_ip':'33.33.33.33',
                    'tor_vendor_name':'Juniper',
                    'tor_product_name':'QFX5100',
                    'tor_agent_http_server_port': '1233',
                    'tor_agent_ovs_ka': '10000',
                       },
                       ] 
                }                
                   

#env.tor_hosts={
#'10.84.61.156': [{'tor_port': 'xe-0/0/7',
#                    'host_port' : 'p6p1',
#                    'mgmt_ip' : '10.84.26.37',
#                    'username' : 'root',
#                    'password' : 'c0ntrail123',
#                  }]
#}

#env.physical_routers={
#'b6-qfx1'       : {
#                     'vendor': 'juniper',
#                     'model' : 'qfx5100',
#                     'asn'   : '64512',
#                     'name'  : 'b6-qfx1',
#                     'ssh_username' : 'root',
#                     'ssh_password' : 'Embe1mpls',
#                     'mgmt_ip'  : '10.84.61.156',
#                     'tunnel_ip' : '34.34.34.34',
#                     'ports' : ['xe-0/0/7'],
#                     'type'  : 'tor',
#}
#}

env.tor_hosts={
'172.16.91.1': [{'tor_port': 'xe-0/0/0',
                    'host_port' : 'eth1',
                    'mgmt_ip' : '10.84.130.15',
                    'username' : 'root',
                    'password' : 'c0ntrail123',
                  }],
'172.16.91.2': [{'tor_port': 'xe-0/0/0',
                    'host_port' : 'eth1',
                    'mgmt_ip' : '10.84.130.16',
                    'username' : 'root',
                    'password' : 'c0ntrail123',
                  }]
}

env.physical_routers={
'5c1-mx80-1'          : {
                     'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64513',
                     'name'  : '5c1-mx80-1',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'   : '172.16.91.77',
                     'tunnel_ip' : '7.7.7.77',
                     'ports' : [],
                     'type'  : 'router',
                 },
'5c1-qfx5'       : {
                     'vendor': 'juniper',
                     'model' : 'qfx5100',
                     'asn'   : '64513',
                     'name'  : '5c1-qfx5',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '172.16.91.1',
                     'tunnel_ip' : '34.34.34.34',
                     'ports' : ['xe-0/0/0'],
                     'type'  : 'tor',
},
'5c1-qfx6'       : {
                     'vendor': 'juniper',
                     'model' : 'qfx5100',
                     'asn'   : '64513',
                     'name'  : '5c1-qfx6',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '172.16.91.2',
                     'tunnel_ip' : '33.33.33.33',
                     'ports' : ['xe-0/0/0'],
                     'type'  : 'tor',
},
}



do_parallel = True
env.mail_from='jebap@juniper.net'
env.mail_to='jebap@juniper.net'
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.test_repo_dir='/root/contrail-test'
env.ca_cert_file='/root/cacert.pem'
