import os
from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.204.217.194'
host2 = 'root@10.204.217.197'
host3 = 'root@10.204.217.198'
host4 = 'root@10.204.218.100'
host5 = 'root@10.204.218.101'
#host6 = 'root@10.204.218.102'

kvm_nodei33 = '10.204.217.145'
kvm_nodel2 = '10.204.218.50'

#External routers if any
#for eg. 
ext_routers = [('mx1', '10.204.216.253')]
#ext_routers = [('hooper', '192.168.1.11')]
router_asn = 64510
public_vn_rtgt = 10003
public_vn_subnet = "10.204.219.56/29"


#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.204.217.187'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3, host4, host5],
    'cfgm': [host1, host4, host5],
    'control': [host1, host4, host5],
    'compute': [host2, host3],
    'collector': [host1, host4, host5],
    'webui': [host1],
    'database': [host1, host4, host5],
    'build': [host_build],
    'contrail-kubernetes': [host1, host4, host5],
}

env.hostnames = {
    'all': ['testbed-1-vm1', 'testbed-1-vm2', 'testbed-1-vm3',
             'testbed-1-vm4', 'testbed-1-vm5', 'testbed-1-vm6']
}

#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'
#Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
#    host6: 'c0ntrail123',
    kvm_nodei33 : 'c0ntrail123',
    kvm_nodel2 : 'c0ntrail123',

    host_build: 'c0ntrail123',
}

#To enable multi-tenancy feature
multi_tenancy = False
minimum_diskGB=32
#To Enable prallel execution of task in multiple nodes
#do_parallel = True
#haproxy = True
env.log_scenario='Kubernets Single-yaml Sanity'

env.test = {
  'mail_to' : 'vjoshi@juniper.net',
  'webserver_host': '10.204.216.50',
  'webserver_user' : 'bhushana',
  'webserver_password' : 'c0ntrail!23',
  'webserver_log_path' :  '/home/bhushana/Documents/technical/logs',
  'webserver_report_path': '/home/bhushana/Documents/technical/sanity',
  'webroot' : 'Docs/logs',
  'mail_server' :  '10.204.216.49',
  'mail_port' : '25',
  'mail_sender': 'contrailbuild@juniper.net',
}
image_name = os.getenv('IMAGE_NAME', 'centos-7.3-1611.qcow2.gz')
vm_node_details = {
    'default': {
                'image_dest' : '/mnt/disk1/images/',
                'ram' : '16384',
                'vcpus' : '4',
                'disk_format' : 'qcow2',
                'image_source' : 'http://10.204.217.158/images/node_vm_images/%s' %(image_name)
                },
    host1 : {
                'name' : 'testbed-1-vm1',
                'server': kvm_nodei33,
                'network' : [{'bridge' : 'br1', 'mac':'52:54:00:01:00:01'},
                            ],
                'ram' : '16384',
                'vcpus' : '8',
            },
    host2 : {
                'name' : 'testbed-1-vm2',
                'server': kvm_nodei33,
                'network' : [{'bridge' : 'br1', 'mac':'52:54:00:01:00:02'},
                            ],
                'ram' : '8192',
                'vcpus' : '4',
            },
    host3 : {
                'name' : 'testbed-1-vm3',
                'server': kvm_nodei33,
                'network' : [{'bridge' : 'br1', 'mac':'52:54:00:01:00:03'},
                            ],
                'ram' : '8192',
                'vcpus' : '4',
            },
    host4 : {
                'name' : 'testbed-1-vm4',
                'server': kvm_nodel2,
                'network' : [{'bridge' : 'br0', 'mac':'52:54:00:01:00:06'},
                            ],
                'ram' : '16384',
                'vcpus' : '8',
                'image_dest' : '/var/lib/libvirt/images/',
            },
    host5 : {
                'name' : 'testbed-1-vm5',
                'server': kvm_nodel2,
                'network' : [{'bridge' : 'br0', 'mac':'52:54:00:01:00:07'},
                            ],
                'ram' : '16384',
                'vcpus' : '8',
                'image_dest' : '/var/lib/libvirt/images/',
            },
#    host6 : {
#                'name' : 'testbed-1-vm6',
#                'server': kvm_nodel2,
#                'network' : [{'bridge' : 'br0', 'mac':'52:54:00:01:00:08'},
#                            ],
#                'ram' : '8192',
#                'vcpus' : '4',
#                'image_dest' : '/var/lib/libvirt/images/',
#            },
}
env.test_repo_dir='/root/vjoshi/contrail-tools/contrail-test'
env.orchestrator='kubernetes'


env.kubernetes = {
'mode' : 'baremetal',
'master': host1,
'slaves': [host2, host3, host4, host5]
}

# 10.204.218.102 is the lb node testbed-1-vm6
#env.ha = {
#    'contrail_external_vip' : '10.204.218.102'
#}
