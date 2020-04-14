from fabric.api import env
import os

host1 = 'root@10.87.36.10'
host2 = 'root@10.87.36.11'
host3 = 'root@10.87.36.12'
host4 = 'root@10.87.36.18'
contrail_vm2 = 'root@10.87.36.19'
contrail_vm3 = 'root@10.87.36.20'


#If there is only single interface,  MX ip is 10.87.36.30
ext_routers = [('a5-mx80-2', '10.87.36.30')]
#For multi-interface setup, mx ip is 192.168.10.200

#ext_routers = [('a5-mx80-2', '192.168.10.200')]
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = "10.84.51.96/27"

# env.orchestrator = 'vcenter'

host_build = 'stack@10.84.24.64'

if os.getenv('HA_TEST',None) == 'True':
    env.roledefs = {
        'all': [host1, host2, host3, host4, contrail_vm2, contrail_vm3],
        'cfgm': [host1, host2, host3],
        'openstack': [host1, host2, host3],
        'control': [host1, host2, host3],
        'compute': [host4, contrail_vm2, contrail_vm3],
        'vcenter_compute':[host3],
        'collector': [host1, host2, host3],
        'webui': [host1, host2, host3],
        'database': [host1, host2, host3],
        'build': [host_build],
    }
else:
    env.roledefs = {
        'all': [host1, host2, host3, host4, contrail_vm2, contrail_vm3],
        'cfgm': [host1, host2],
        'openstack': [host1],
        'control': [host1, host3],
        'compute': [host4, contrail_vm2, contrail_vm3],
        'vcenter_compute':[host3],
        'collector': [host1],
        'webui': [host1],
        'database': [host1, host2, host3],
        'build': [host_build],
    }
env.hostnames = {
    'all': ['5a10s31', '5a10s30', '5a10s29', '5a10s23', 'ContrailVM-5a10s27', 'ContrailVM-5a10s25']
}

env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    contrail_vm2: 'c0ntrail123',
    contrail_vm3: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    contrail_vm2:'esxi-5.5',
    contrail_vm3:'esxi-5.5',
}

env.vcenter_servers = {
       'vcenter1': {
           'server':'10.84.22.104',
           'port': '443',
           'username': 'administrator@vsphere.local',
           'password': 'Contrail123!',
           'auth': 'https',
           'datacenters': {
               'A6s32-VC-Compute-Sanity': {
                    'datacenter_mtu': 1500,
                    'dv_switches': {
                        'Sanity-dvswitch-1': {
                            'dv_switch_version': '5.5.0',
                            'dv_port_group': {
                                 'dv_portgroup_name': 'Sanity-dvportgroup-1',
                                 'number_of_ports': '18',
                            },
                            'vcenter_compute': '10.87.36.12',
                            'clusters': ['cluster-1'], #for mitaka, has to be a single cluster in the list
                        },
                    },
               },
           },
       },
}


esxi_hosts = {
    '5a10s27' : {
        'ip' : '10.87.36.14',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'datastore': "/vmfs/volumes/datastore2",
        'vcenter_server': 'vcenter1',
        'cluster': 'cluster-1',
        'datacenter': 'A6s32-VC-Compute-Sanity',
        'contrail_vm': {
            'name' : 'ContrailVM-5a10s27',
            'mac' : "00:77:56:aa:bb:01",
            'host' : "root@10.87.36.19",
            'mode': "vcenter",
            'vmdk_download_path': "http://10.84.5.120/cs-shared/contrail-vcenter/vmdk/LATEST/ContrailVM-disk1.vmdk",
        }
    },

    '5a10s25' : {
        'ip' : '10.87.36.16',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'datastore': "/vmfs/volumes/datastore3",
        'vcenter_server': 'vcenter1',
        'cluster': 'cluster-1',
        'datacenter': 'A6s32-VC-Compute-Sanity',
        'contrail_vm' : {
            'name' : 'ContrailVM-5a10s25',
            'mac' : "00:77:56:aa:bb:02",
            'host' : "root@10.87.36.20",
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
#    host6 : { 'ip': '192.168.10.6/24', 'gw' : '192.168.10.254', 'device':'em1' },
#}

# VIP cofiguration for HA
if os.getenv('HA_TEST',None) == 'True':
    env.ha = {
        'internal_vip' : '10.87.36.25'
       # 'internal_vip' : '192.168.10.210',
       # 'external_vip' : '10.84.13.201'
    }
# HA Test configuration
    ha_setup = 'True'
    ipmi_username = 'ADMIN'
    ipmi_password = 'ADMIN'
    env.hosts_ipmi = {
        '10.87.36.10': '10.87.36.1',
        '10.87.36.11': '10.87.36.2',
        '10.87.36.12': '10.87.36.3',
        '10.87.36.14': '10.87.36.5',
        '10.87.36.16': '10.87.36.7',
        '10.87.36.18': '10.87.36.9',
    }
#do_parallel=True
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
env.log_scenario='Vcenter-Compute MultiDC, SingleCluster, MultiNode Single Intf Sanity'
env.enable_lbaas = True

env.ntp_server = '10.84.5.100'
env.test = {
     'mail_to': 'dl-contrail-sw@juniper.net',
     'mail_server': '10.84.24.64',
     'mail_port': '4000',
     'image_web_server': '10.84.5.120',
     'log_scenario': 'Vcenter-Compute MultiDC,SingleCluster, MultiNode Single Intf Sanity',
           }
#enable_ceilometer = True
#ceilometer_polling_interval = 60

