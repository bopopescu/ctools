from fabric.api import env
import os

host1 = 'root@10.84.13.32'
host2 = 'root@10.84.13.33'
host3 = 'root@10.84.13.38'
host4 = 'root@10.84.13.2'
host5 = 'root@10.84.14.143'
contrail_vm2 = 'root@10.84.13.222'
contrail_vm3 = 'root@10.84.13.223'
contrail_vm4 = 'root@10.84.20.240'
contrail_vm5 = 'root@10.84.20.242'
host0 = 'root@10.84.14.142'


#If there is only single interface,  MX ip is 10.84.13.200
ext_routers = [('a5-mx80-2', '10.84.13.200')]
#For multi-interface setup, mx ip is 192.168.10.200

#ext_routers = [('a5-mx80-2', '192.168.10.200')]
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = "10.84.51.96/27"

# env.orchestrator = 'vcenter'

host_build = 'stack@10.84.24.64'

if os.getenv('HA_TEST',None) == 'True':
    env.roledefs = {
        'all': [host1, host2, host3, host4, host5, contrail_vm2, contrail_vm3, contrail_vm4, contrail_vm5, host0],
        'cfgm': [host1, host2, host3],
        'openstack': [host1, host2, host3],
        'control': [host1, host2, host3],
        'compute': [host4, host5, contrail_vm2, contrail_vm3, contrail_vm4, contrail_vm5],
        'vcenter_compute':[host3, host0],
        'collector': [host1, host2, host3],
        'webui': [host1, host2, host3],
        'database': [host1, host2, host3],
        'build': [host_build],
    }
else:
    env.roledefs = {
        'all': [host1, host2, host3, host4, host5, contrail_vm2, contrail_vm3, contrail_vm4, contrail_vm5, host0],
        'cfgm': [host1, host2],
        'openstack': [host1],
        'control': [host1, host3],
        'compute': [host4, host5, contrail_vm2, contrail_vm3, contrail_vm4, contrail_vm5],
        'vcenter_compute':[host3, host0],
        'collector': [host1],
        'webui': [host1],
        'database': [host1, host2, host3],
        'build': [host_build],
    }
env.hostnames = {
    'all': ['a6s32', 'a6s33', 'a6s38', 'a6s2', 'a5s43', 'ContrailVM-a6s22', 'ContrailVM-a6s44', 'ContrailVM-a6s41', 'ContrailVM-a6s42', 'a5s42']
}

env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    contrail_vm2: 'c0ntrail123',
    contrail_vm3: 'c0ntrail123',
    contrail_vm4: 'c0ntrail123',
    contrail_vm5: 'c0ntrail123',
    host0: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    contrail_vm2:'esxi-5.5',
    contrail_vm3:'esxi-5.5',
    contrail_vm4:'esxi-5.5',
    contrail_vm5:'esxi-5.5',
    host0:'ubuntu',
}

env.vcenter_servers = {
       'Datacenter1': {
            'server':'10.84.22.104',
            'port': '443',
            'username': 'Administrator@vsphere.local',
            'password': 'Contrail123!',
            'auth': 'https',
            'datacenter': 'VC-Compute-Sanity-DC-1',
            'vcenter_compute': '10.84.13.38',
            'cluster': ['cluster-A', 'cluster-B'],
            'dv_switch': { 'dv_switch_name': 'Sanity-dvswitch-1',
                         },
            'dv_port_group': { 'dv_portgroup_name': 'Sanity-dvportgroup-1',
                              'number_of_ports': '1800',
                         },
     },
       'Datacenter2': {
            'server':'10.84.22.104',                 
            'port': '443',
            'username': 'Administrator@vsphere.local',
            'password': 'Contrail123!',
            'auth': 'https',
            'datacenter': 'VC-Compute-Sanity-DC-2',
            'vcenter_compute': '10.84.14.142',            
            'cluster': ['cluster-A'],
            'dv_switch': { 'dv_switch_name': 'Sanity-dvswitch-1',
                         },
            'dv_port_group': { 'dv_portgroup_name': 'Sanity-dvportgroup-1',
                              'number_of_ports': '1800',
                         },
     },
}



esxi_hosts = {
    'a6s22' : {
        'ip' : '10.84.13.22',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'datastore': "/vmfs/volumes/datastore2",
        'vcenter_server': 'Datacenter1',
        'cluster': 'cluster-A',
	'datacenter': 'VC-Compute-Sanity-DC-1'
        'contrail_vm' : {
            'name' : 'ContrailVM-a6s22',
            'mac' : '00:50:56:a9:1b:66',
            'host' : 'root@10.84.13.222',
            'mode': "vcenter",
            'vmdk_download_path': "http://10.84.5.120/cs-shared/contrail-vcenter/vmdk/LATEST/ContrailVM-disk1.vmdk",
        }
    },

    'a6s44' : {
        'ip' : '10.84.13.44',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'datastore': "/vmfs/volumes/datastore3",
        'vcenter_server': 'Datacenter1',
        'cluster': 'cluster-A',
	'datacenter': 'VC-Compute-Sanity-DC-1'
        'contrail_vm' : {
            'name' : 'ContrailVM-a6s44',
            'mac' : '00:50:56:aa:31:7c',
            'host' : 'root@10.84.13.223',
            'mode': "vcenter",
            'vmdk_download_path': "http://10.84.5.120/cs-shared/contrail-vcenter/vmdk/LATEST/ContrailVM-disk1.vmdk",
        }
    },

    'a6s41' : {
        'ip' : '10.84.20.40',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'datastore': "/vmfs/volumes/datastore3",
        'vcenter_server': 'Datacenter1',
        'cluster': 'cluster-B',
	'datacenter': 'VC-Compute-Sanity-DC-1'
        'contrail_vm' : {
            'name' : 'ContrailVM-a6s41',
            'mac' : '00:50:56:aa:ee:7c',
            'host' : 'root@10.84.20.240',
            'mode': "vcenter",
            'vmdk_download_path': "http://10.84.5.120/cs-shared/contrail-vcenter/vmdk/LATEST/ContrailVM-disk1.vmdk",
        }
    },

    'a6s42' : {
        'ip' : '10.84.20.42',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'datastore': "/vmfs/volumes/datastore3",
        'vcenter_server': 'Datacenter1',
        'cluster': 'cluster-A',
	'datacenter': 'VC-Compute-Sanity-DC-2'
        'contrail_vm' : {
            'name' : 'ContrailVM-a6s42',
            'mac' : '00:50:56:aa:ff:7c',
            'host' : 'root@10.84.20.242',
            'mode': "vcenter",
            'vmdk_download_path': "http://10.84.5.120/cs-shared/contrail-vcenter/vmdk/LATEST/ContrailVM-disk1.vmdk",
        }
    },

}

#control_data= {
#
#    host1 : { 'ip': '192.168.10.1/24', 'gw' : '192.168.10.254', 'device':'em1' },
#    host2 : { 'ip': '192.168.10.2/24', 'gw' : '192.168.10.254', 'device':'em1' },
#    host3 : { 'ip': '192.168.10.3/24', 'gw' : '192.168.10.254', 'device':'em1' },
#    host4 : { 'ip': '192.168.10.4/24', 'gw' : '192.168.10.254', 'device':'em2' },
#    host5 : { 'ip': '192.168.10.5/24', 'gw' : '192.168.10.254', 'device':'em1' },
#    host6 : { 'ip': '192.168.10.6/24', 'gw' : '192.168.10.254', 'device':'em1' },
#}

# VIP cofiguration for HA
if os.getenv('HA_TEST',None) == 'True':
    env.ha = {
        'internal_vip' : '10.84.13.201'
       # 'internal_vip' : '192.168.10.210',
       # 'external_vip' : '10.84.13.201'
    }
# HA Test configuration
    ha_setup = 'True'
    ipmi_username = 'ADMIN'
    ipmi_password = 'ADMIN'
    env.hosts_ipmi = {
        '10.84.13.32': '10.84.6.82',
        '10.84.13.33': '10.84.6.83',
        '10.84.13.38': '10.84.6.88',
        '10.84.13.2': '10.84.6.22',
	'10.84.14.143': '10.84.6.77',
        '10.84.13.22': '10.84.6.72',
        '10.84.13.44': '10.84.6.94',
	'10.84.20.40': '10.84.6.74',
	'10.84.20.42': '10.84.6.75',
	'10.84.14.142': '10.84.6.76',
    }
do_parallel=True
minimum_diskGB=32
env.test_repo_dir="/home/stack/ubuntu_sanity/contrail-test"
env.mail_from='nsarath@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.encap_priority="'MPLSoUDP','MPLSoGRE','VXLAN'"
env.mail_server='10.84.24.64'
env.mail_port='4000'
env.mx_gw_test=True
env.testbed_location='US'
env.interface_rename = False 
env.image_web_server = '10.84.5.120'
env.log_scenario='Vcenter-Compute MultiDC, MultiCluster, MultiNode Single Intf Sanity'
env.enable_lbaas = True

env.ntp_server = '10.84.5.100'
env.test = {
     'mail_to': 'dl-contrail-sw@juniper.net',
     'mail_server': '10.84.24.64',
     'mail_port': '4000',
     'image_web_server': '10.84.5.120',
     'log_scenario': 'Vcenter-Compute MultiDC, MultiCluster, MultiNode Single Intf Sanity',
           }
#enable_ceilometer = True
#ceilometer_polling_interval = 60
