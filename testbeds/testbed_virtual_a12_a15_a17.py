from fabric.api import env
import os

host1 = 'root@10.204.217.172'
host2 = 'root@10.204.217.179'
host3 = 'root@10.204.216.111'
host4 = 'root@10.204.216.8'
host5 = 'root@10.204.216.11'
host6 = 'root@10.204.216.13'

kvm_nodei13 = '10.204.217.192'
kvm_nodei14 = '10.204.217.126'
kvm_nodek7 = '10.204.216.227'

ext_routers = [('hooper','10.204.217.240')]                                                                                                                                                             
router_asn = 64512                                                                                                                                                                                        
public_vn_rtgt = 2225                                                                                                                                              
public_vn_subnet = '10.204.221.160/28'
host_build = 'stack@10.204.216.49'

if os.getenv('AUTH_PROTOCOL',None) == 'https':
    env.log_scenario='Multi-Node Virtual Testbed Sanity[mgmt, ctrl=data, SSL]'
    env.roledefs = {
        'all': [host1,host2,host3,host4,host5,host6],
        'cfgm': [host1],
        'webui': [host1],
        'openstack': [host1],
        'control': [host2, host3],
        'collector': [host1],
        'database': [host1, host2, host3],
        'compute': [host4, host5, host6],
        'build': [host_build]
    }
    env.keystone = {
        'auth_protocol': 'https'
    }
    env.cfgm = {
        'auth_protocol': 'https'
    }
else:
    env.log_scenario='Multi-Node Virtual Testbed Sanity[mgmt, ctrl=data]'
    env.roledefs = {
        'all': [host1,host2,host3,host4,host5,host6],
        'cfgm': [host1, host2],
        'webui': [host1],
        'openstack': [host1],
        'control': [host2, host3],
        'collector': [host1],
        'database': [host1, host2, host3],
        'compute': [host4, host5, host6],
        'build': [host_build]
    }

if os.getenv('ENABLE_RBAC',None) == 'true':
    cloud_admin_role = 'admin'
    aaa_mode = 'rbac'

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
    'all': ['nodei13-vm2', 'nodei14-vm2', 'nodek7-vm2', 'nodea12', 'nodea15', 'nodea17']
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

reimage_param = os.getenv('REIMAGE_PARAM', 'ubuntu-14.04.2')

vm_node_details = {
    'default': {
                'image_dest' : '/mnt/disk1/images/',
                'ram' : '32768',
                'vcpus' : '4',
                'disk_format' : 'qcow2',
                'image_source' : 'http://10.204.217.158/images/node_vm_images/centos-7.5.qcow2',
                },
    host1 : {   'name' : 'nodek7-vm3',
                'server': kvm_nodek7,
                'network' : [{'bridge' : 'br0', 'mac':'52:53:57:01:00:03'},{'bridge': 'br1'}
                            ]
            }
}


minimum_diskGB=32
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
env.test_repo_dir='/home/stack/multi_interface_parallel/centos65/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename = True
env.ntp_server = '10.204.217.158'
env.enable_lbaas = True
enable_ceilometer = True
ceilometer_polling_interval = 60
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
