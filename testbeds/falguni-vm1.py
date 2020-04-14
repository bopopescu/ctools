from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.204.217.203'

kvm_node1 = '10.204.217.130'

ext_routers = []
router_asn = 64512
public_vn_rtgt = 44444


#Host from which the fab commands are triggered to install and provision
host_build = 'stack@10.204.216.49'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1],
    'compute': [host1],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
    'all': ['falguni-vm1']
}

#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'
#Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    kvm_node1: 'c0ntrail123',

    host_build: 'stack@123',
}

#To disable installing contrail interface rename package
env.interface_rename = True

#To enable multi-tenancy feature
multi_tenancy = True
minimum_diskGB=32
#To Enable prallel execution of task in multiple nodes
do_parallel = True
#haproxy = True
env.test_repo_dir='/home/stack/jenkins/workspace/falguni-vm1/contrail-tools/contrail-test'
env.mail_to='vjoshi@juniper.net'
env.log_scenario='falguni-vm1 Single Node Virtual Testbed Results'
env.enable_lbaas = True

#enable ceilometer
enable_ceilometer = True
ceilometer_polling_interval = 60

vm_node_details = {
    'default': {
                'server': kvm_node1,
                'image_dest' : '/mnt/disk1/images/',
                'ram' : '16384',
                'vcpus' : '4',
                'disk_format' : 'qcow2',
                'image_source' : 'http://10.204.217.158/images/node_vm_images/ubuntu-14.04.2-256G.img.gz',
                },
    host1 : {   
                'name' : 'falguni-vm1',
                'network' : [{'bridge' : 'br1', 'mac':'52:54:00:03:00:01'},
                            ],
            }
}

env.cluster_id='falguni'
