from fabric.api import env
import os

host1 = 'root@10.204.216.115'
host2 = 'root@10.204.216.116'
host3 = 'root@10.204.216.117'
host4 = 'root@10.204.216.118'
host5 = 'root@10.204.216.119'
host6 = 'root@10.204.216.125'

kvm_nodel12 = '10.204.216.114'

ext_routers = [('hooper','10.204.217.240')]                                                                                                                                                             
router_asn = 64512                                                                                                                                                                                        
public_vn_rtgt = 2225                                                                                                                                              
public_vn_subnet = '10.204.221.160/28'
host_build = 'stack@10.204.216.49'

{env_roledefs}
#env.roledefs = {
#    'all': [host1,host2,host3,host4,host5,host6],
#    'cfgm': [host1, host2],
#    'webui': [host1],
#    'openstack': [host1],
#    'control': [host2, host3],
#    'collector': [host1],
#    'database': [host1, host2, host3],
#    'compute': [host4, host5, host6],
#    'build': [host_build]
#}

env.physical_routers={
'hooper'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'hooper',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.240',
             }
}

env.hostnames = {
    'all': ['nodel12-vm1', 'nodel12-vm2', 'nodel12-vm3', 'nodel12-vm4', 'nodel12-vm5', 'nodel12-vm6']
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

reimage_param = 'ubuntu-14.04.5'

vm_node_details = {
    'default': {
                'image_dest' : '/mnt/disk1/images/',
                'ram' : '32768',
                'server': kvm_nodel12,
                'vcpus' : '4',
                'disk_format' : 'qcow2',
                'image_source' : 'http://10.204.217.158/images/node_vm_images/%s-256G.img.gz' % (reimage_param),
                },
    host1 : {  
                'name' : 'nodel12-vm1',
                'network' : [{'bridge' : 'br1', 'mac':'52:53:59:01:00:01'}
                            ],
            },
    host2 : {   'name' : 'nodel12-vm2',
                'network' : [{'bridge' : 'br1', 'mac':'52:53:59:01:00:02'}
                            ]
            },
    host3 : {   'name' : 'nodel12-vm3',
                'network' : [{'bridge' : 'br1', 'mac':'52:53:59:01:00:03'}
                            ]
            },
    host4 : {   'name' : 'nodel12-vm4',
                'network' : [{'bridge' : 'br1', 'mac':'52:53:59:01:00:04'}
                            ]
            },
    host5 : {   'name' : 'nodel12-vm5',
                'network' : [{'bridge' : 'br1', 'mac':'52:53:59:01:00:05'}
                            ]
            },
    host6 : {   'name' : 'nodel12-vm6',
                'network' : [{'bridge' : 'br1', 'mac':'52:53:59:01:00:06'}
                            ]
            }
}

env.keystone = {'admin_password': 'c0ntrail123'}
env.openstack = {'manage_amqp': "true"}
minimum_diskGB=32
env.kernel_upgrade=False
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
env.test_repo_dir='/home/stack/multi_interface_parallel/centos65/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename = True
env.enable_lbaas = True
enable_ceilometer = True
ceilometer_polling_interval = 60
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.log_scenario='Multi-Node Nodel12 Contrainer Sanity[mgmt, ctrl=data]'
env.ntp_server = '10.204.217.158'
