from fabric.api import env
import os

host1 = 'root@10.87.36.10'
host2 = 'root@10.87.36.11'
host3 = 'root@10.87.36.12'
host4 = 'root@10.87.36.18'
contrail_vm11a = 'root@10.87.36.19'
contrail_vm11b = 'root@10.87.36.20'
contrail_vm12a = 'root@10.87.36.21'
host0 = 'root@10.87.36.15'


#If there is only single interface,  MX ip is 10.87.36.30
ext_routers = [('a5-mx80-2', '10.87.36.62')]
#For multi-interface setup, mx ip is 192.168.10.200

#ext_routers = [('a5-mx80-2', '192.168.10.200')]
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = "10.84.51.96/27"

host_build = 'stack@10.84.24.64'

if os.getenv('HA_TEST',None) == 'True':
    env.roledefs = {
        'all': [host1, host2, host3, host4, contrail_vm11a, contrail_vm11b, contrail_vm12a, host0],
        'cfgm': [host1, host2, host3],
        'openstack': [host1, host2, host3],
        'control': [host1, host2, host3],
        'compute': [host4, contrail_vm11a, contrail_vm11b, contrail_vm12a],
        'vcenter_compute':[host3, host0],
        'collector': [host1, host2, host3],
        'webui': [host1, host2, host3],
        'database': [host1, host2, host3],
        'build': [host_build],
    }
else:
    env.roledefs = {
        'all': [host1, host2, host3, host4, contrail_vm11a, contrail_vm11b, contrail_vm12a, host0],
        'cfgm': [host1, host2],
        'openstack': [host1],
        'control': [host1, host3],
        'compute': [host4, contrail_vm11a, contrail_vm11b, contrail_vm12a],
        'vcenter_compute':[host3, host0],
        'collector': [host1],
        'webui': [host1],
        'database': [host1, host2, host3],
        'build': [host_build],
    }
env.hostnames = {
    'all': ['5a10s31', '5a10s30', '5a10s29', '5a10s23', 'ContrailVM-5a10s27', 'ContrailVM-5a10s25', 'ContrailVM-5a10s31', '5a10s26']
}

env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    contrail_vm11a: 'c0ntrail123',
    contrail_vm11b: 'c0ntrail123',
    contrail_vm12a: 'c0ntrail123',
    host0: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    contrail_vm11a:'ubuntu',
    contrail_vm11b:'ubuntu',
    contrail_vm12a:'ubuntu',
    host0:'ubuntu',
}

#OPTIONAL BONDING CONFIGURATION
#==============================
#Inferface Bonding
bond = {
    host0 : { 'name': 'bond0', 'member': ['eth2','eth1'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host1 : { 'name': 'bond0', 'member': ['eth2','eth1'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host2 : { 'name': 'bond0', 'member': ['eth2','eth1'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host3 : { 'name': 'bond0', 'member': ['p8p1','p8p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host4 : { 'name': 'bond0', 'member': ['eth2','eth1'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    contrail_vm11a : { 'name': 'bond0', 'member': ['eth2','eth1'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    contrail_vm11b : { 'name': 'bond0', 'member': ['eth2','eth1'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    contrail_vm12a : { 'name': 'bond0', 'member': ['eth2','eth1'], 'mode': 'active-backup', 'fail_over_mac': '1' },
}

#OPTIONAL SEPARATION OF MANAGEMENT AND CONTROL + DATA and OPTIONAL VLAN INFORMATION
#==================================================================================
control_data = {
    host0 : { 'ip': '172.16.80.10/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host1 : { 'ip': '172.16.80.11/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host2 : { 'ip': '172.16.80.12/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host3 : { 'ip': '172.16.80.13/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host4 : { 'ip': '172.16.80.14/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    contrail_vm11a : { 'ip': '172.16.80.15/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    contrail_vm11b : { 'ip': '172.16.80.16/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    contrail_vm12a : { 'ip': '172.16.80.17/24', 'gw' : '172.16.80.254', 'device':'bond0' },
}

static_route  = {
    host0 : [{ 'ip': '172.16.0.0', 'netmask' : '255.255.0.0', 'gw':'172.16.80.254', 'intf': 'bond0' }],
    host1 : [{ 'ip': '172.16.0.0', 'netmask' : '255.255.0.0', 'gw':'172.16.80.254', 'intf': 'bond0' }],
    host2 : [{ 'ip': '172.16.0.0', 'netmask' : '255.255.0.0', 'gw':'172.16.80.254', 'intf': 'bond0' }],
    host3 : [{ 'ip': '172.16.0.0', 'netmask' : '255.255.0.0', 'gw':'172.16.80.254', 'intf': 'bond0' }],
    host4 : [{ 'ip': '172.16.0.0', 'netmask' : '255.255.0.0', 'gw':'172.16.80.254', 'intf': 'bond0' }],
    contrail_vm11a : [{ 'ip': '172.16.0.0', 'netmask' : '255.255.0.0', 'gw':'172.16.80.254', 'intf': 'bond0' }],
    contrail_vm11b : [{ 'ip': '172.16.0.0', 'netmask' : '255.255.0.0', 'gw':'172.16.80.254', 'intf': 'bond0' }],
    contrail_vm12a : [{ 'ip': '172.16.0.0', 'netmask' : '255.255.0.0', 'gw':'172.16.80.254', 'intf': 'bond0' }],
}

#To enable multi-tenancy
multi_tenancy = True


##############################################################
#vcenter provisioning
#server is the vcenter server ip
#port is the port on which vcenter is listening for connection
#username is the vcenter username credentials
#password is the vcenter password credentials
#auth is the autentication type used to talk to vcenter, http or https
#datacenter is the datacenter name we are operating on
#cluster is the clustername we are operating on
#dvswitch section contains distributed switch related para,s
#       dv_switch_name and the nic which will be put on it
#dvportgroup section contains the distributed port group info
#       dv_portgroupname and the number of ports the group has
######################################
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
                        'Sanity-dvswitch-2': {
                            'dv_switch_version': '5.5.0',
                            'dv_port_group': {
                                 'dv_portgroup_name': 'Sanity-dvportgroup-2',
                                 'number_of_ports': '18',
                            },
                            'vcenter_compute': '10.87.36.15',
                            'clusters': ['cluster-2'], #for mitaka, has to be a single cluster in the list
                        },
           		'dv_switch_sr_iov': {
                            'dv_switch_version': '5.5.0',
			    'dv_port_group': {
                                 'dv_portgroup_name': 'dvs-sriov-pg': {
                                 'number_of_ports': '2',
                            },
           		},
                    },
               },
           },
       },
}


#######################################
#The compute vm provisioning on ESXI host
#This section is used to copy a vmdk on to the ESXI box and bring it up# . the contrailVM which comes up will be setup as a compute node with 
# only vrouter running on it.
# Each host has an associated esxi to it. For example in the below
# section host1 is associated with esxi inside that section.
# esx_ip: the esxi ip on which the contrailvm(host/compute) runs
# esx_username: username used to login to esxi
# esx_password: password for esxi
# esx_uplinck_nic: the nic usedfor underlay
# esx_fab_vswitch: the name of the underlay vswitch that runs on esxi
# esx_fab_port_group: the name of the underlay port group for esxi
# esx_ssl_thumbprint: the ssl thumbprint on esxi host,needed by vcenter
#               Run this and get the ssl thumbprint on host: openssl x509 -in /etc/vmware/ssl/rui.crt -fingerprint -sha1 -noout
# server_mac: the virt mac address for the contrail vm
# server_ip the contrailvm ip to be associated with the virtual mac
# esx_vm_name: the contrailvm name which is brought up on esxi
# esx_data_store: the datastore on esxi where the vmdk is copied to
# esx_vmdk: the absolute path of the contrail-vmdk used to spawn vm
# vm: the name used by esxi for vmdk changes, same as esx_vm_name
# vmdk: name of the vmdk file without the vmdk extension
# vm_deb: absolute path of the contrail package installed on contrailvm
# esx_vm_switch: name of vswitch crated for vm interaction
# esx_vm_portgroup: name of port group for vm interaction
# server_id: hostname of the contrailvm
# password: root password for the contrailvm
# domain: domain of the contrailvm
##############################################
esxi_hosts = {
    '5a10s27' : {
        'ip' : '10.87.36.14',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'datastore': "/vmfs/volumes/datastore2",
        'vcenter_server': 'vcenter1',
        'cluster': 'cluster-1',
        'datacenter': 'A6s32-VC-Compute-Sanity',
        'skip_reimage'  : 'true',
        'contrail_vm': {
            'name' : 'ContrailVM-5a10s27',
            'mac' : "00:77:56:aa:bb:01",
            'host' : "root@10.87.36.19",
            'mode': "vcenter",
            'vmdk_download_path': "http://10.84.5.120/cs-shared/contrail-vcenter/vmdk/14.04/LATEST/ContrailVM-disk1.vmdk",
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
        'skip_reimage'  : 'true',
        'contrail_vm' : {
            'name' : 'ContrailVM-5a10s25',
            'mac' : "00:77:56:aa:bb:02",
            'host' : "root@10.87.36.20",
            'pci_devices': {
            	 'nic': ["04:00.0", "04:00.1"],
            },
            'mode': "vcenter",
            'vmdk_download_path': "http://10.84.5.120/cs-shared/contrail-vcenter/vmdk/14.04/LATEST/ContrailVM-disk1.vmdk",
        }
    },

    '5a10s01a' : {
        'ip' : '10.87.36.29',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'datastore': "/vmfs/volumes/datastore4",
        'vcenter_server': 'vcenter1',
        'cluster': 'cluster-2',
        'datacenter': 'A6s32-VC-Compute-Sanity',
        'skip_reimage'  : 'true',
        'contrail_vm' : {
            'name' : 'ContrailVM-5a10s31',
            'mac' : "00:77:56:aa:bb:03",
            'host' : "root@10.87.36.21",
	    'sr_iov_nics': ['vmnic0', 'vmnic1'],
            'mode': "vcenter",
            'vmdk_download_path': "http://10.84.5.120/cs-shared/contrail-vcenter/vmdk/14.04/LATEST/ContrailVM-disk1.vmdk",
        }
    },

}

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
env.encap_priority="'MPLSoUDP','MPLSoGRE','VXLAN'"
env.mail_server='10.84.24.64'
env.mail_port='4000'
env.mx_gw_test=True
env.testbed_location='US'
env.interface_rename = False 
env.image_web_server = '10.84.5.120'
env.log_scenario='Vcenter-Compute MultiDC, Multi-Cluster, MultiNode Single Intf Sanity'
env.enable_lbaas = True

env.ntp_server = '10.84.5.100'
env.test = {
     'mail_to': 'dl-contrail-sw@juniper.net',
     'mail_server': '10.84.24.64',
     'mail_port': '4000',
     'image_web_server': '10.84.5.120',
     'log_scenario': 'Vcenter-Compute MultiDC, Multi-Cluster, MultiNode Single Intf Sanity',
           }
#enable_ceilometer = True
#ceilometer_polling_interval = 60
