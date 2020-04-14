from fabric.api import env
import os

host1 = 'root@10.204.217.103'
host2 = 'root@10.204.217.232'
host3 = 'root@10.204.216.110'
host4 = 'root@10.204.217.68'
host5 = 'root@10.204.217.69'
host6 = 'root@10.204.217.70'

kvm_nodei13 = '10.204.217.192'
kvm_nodei14 = '10.204.217.126'
kvm_nodek7 = '10.204.216.227'

ext_routers = [('hooper','192.168.196.10')]
router_asn = 64511
public_vn_rtgt = 2226
public_vn_subnet = '10.204.221.144/28'

host_build = 'stack@10.204.216.49'

if os.getenv('AUTH_PROTOCOL',None) == 'https':
    env.log_scenario='MultiNode Multi-Interface Virtual Testbed Sanity [SSL]'
    env.roledefs = {
        'all': [host1, host2, host3, host4, host5, host6],
        'cfgm': [host1],
        'webui': [host2],
        'openstack': [host3],
        'control': [host1, host3],
        'collector': [host1, host3],
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
    env.log_scenario='MultiNode Multi-Interface Virtual Testbed Sanity'
    env.roledefs = {
        'all': [host1, host2, host3, host4, host5, host6],
        'cfgm': [host1, host3],
        'webui': [host2],
        'openstack': [host3],
        'control': [host1, host3],
        'collector': [host1, host3],
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
    'all': ['nodei13-vm1', 'nodei14-vm1', 'nodek7-vm1', 'nodeg28', 'nodeg29', 'nodeg30']
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

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    host6:'ubuntu',
}

control_data = {
    host1 : { 'ip': '192.168.196.1/24', 'gw' : '192.168.196.254', 'device':'eth1' },
    host2 : { 'ip': '192.168.196.2/24', 'gw' : '192.168.196.254', 'device':'eth1' },
    host3 : { 'ip': '192.168.196.3/24', 'gw' : '192.168.196.254', 'device':'eth1' },
    host4 : { 'ip': '192.168.196.4/24', 'gw' : '192.168.196.254', 'device':'p1p2' },
    host5 : { 'ip': '192.168.196.5/24', 'gw' : '192.168.196.254', 'device':'p1p2' },
    host6 : { 'ip': '192.168.196.6/24', 'gw' : '192.168.196.254', 'device':'p1p2' },
}

reimage_param = os.getenv('REIMAGE_PARAM', 'ubuntu-14.04.2')

vm_node_details = {
    'default': {
                'image_dest' : '/mnt/disk1/images/',
                'ram' : '32768',
                'vcpus' : '4',
                'disk_format' : 'qcow2',
                'image_source' : 'http://10.204.217.158/images/node_vm_images/%s-256G.img.gz' % (reimage_param),
                },
    host1 : {
                'name' : 'nodei13-vm1',
                'server': kvm_nodei13,
                'network' : [{'bridge' : 'br1', 'mac':'52:53:55:01:00:01'},
                             {'bridge' : 'br0'}
                            ],
            },
    host2 : {   'name' : 'nodei14-vm1',
                'server': kvm_nodei14,
                'network' : [{'bridge' : 'br1', 'mac':'52:53:56:01:00:01'},
                             {'bridge' : 'br0'}
                            ]
            },
    host3 : {   'name' : 'nodek7-vm1',
                'server': kvm_nodek7,
                'network' : [{'bridge' : 'br1', 'mac':'52:53:57:01:00:01'},
                             {'bridge' : 'br0'}
                            ]
            }
}

minimum_diskGB=32
env.test_repo_dir='/home/stack/multi-node/ubuntu/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
env.interface_rename = True
multi_tenancy=True
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"

#enable ceilometer
enable_ceilometer = True
ceilometer_polling_interval = 60
env.ntp_server = '10.204.217.158'
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
