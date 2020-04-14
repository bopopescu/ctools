from fabric.api import env
import os
c4 = '10.204.216.61'
c5 = '10.204.216.62'
c6 = '10.204.216.63'
k4 = '10.204.216.224'
k5 = '10.204.216.225'
k6 = '10.204.216.226'
nodek4_vm = '10.204.216.181'
nodek5_vm = '10.204.216.182'
nodek6_vm = '10.204.216.183'
#host1 = 'root@' + c4
#host2 = 'root@' + c5
#host3 = 'root@' + c6
#host4 = 'root@' + nodek4_vm
#host5 = 'root@' + nodek5_vm
#host6 = 'root@' + nodek6_vm
#esx1 = 'root@' + k4
#esx2 = 'root@' + k5
#esx3 = 'root@' + k6

host1 = 'root@10.204.216.61'
host2 = 'root@10.204.216.62'
host3 = 'root@10.204.216.63'
host4 = 'root@10.204.216.181'
host5 = 'root@10.204.216.182'
host6 = 'root@10.204.216.183'
esx1 = 'root@10.204.216.224'
esx2 = 'root@10.204.216.225'
esx3 = 'root@10.204.216.226'

ext_routers = [('hooper','10.204.217.240')]
router_asn = 64512
public_vn_rtgt = 2227
public_vn_subnet = '10.204.221.224/28'

host_build = 'stack@10.204.216.49'
if os.getenv('HA_TEST',None) == 'True':
    env.roledefs = {
        'all': [host1, host2, host3, host4, host5, host6],
        'cfgm': [host1, host2, host3],
        'webui': [host1, host2, host3],
        'control': [host2, host3],
        'collector': [host1],
        'database': [host1, host2, host3],
        'compute': [host4, host5, host6],
        'build': [host_build]
    }
else:
    env.roledefs = {
        'all': [host1, host2, host3, host4, host5, host6],
        'cfgm': [host1],
        'webui': [host1],
        'control': [host2, host3],
        'collector': [host1],
        'database': [host1],
        'compute': [host4, host5, host6],
        'build': [host_build]
    }
env.hostnames = {
    'all': ['nodec4', 'nodec5', 'nodec6', 'nodek4-compute-vm', 'nodek5-compute-vm', 'nodek6-compute-vm']
}

env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
    esx1: 'c0ntrail123',
    esx2: 'c0ntrail123',
    esx3: 'c0ntrail123',
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

env.orchestrator = 'vcenter'

env.vcenter_servers = {
     'vcenter1':{
        'server':'10.204.217.189',
        'port': '443',
        'username': 'administrator@vsphere.local',
        'password': 'Contrail123!',
        'auth': 'https',
        'datacenter': 'c4k4u14',
        'cluster': ['c4k4rack14'],
        'dv_switch': { 'dv_switch_name': 'c4k4u14_dvs', 'nic': 'vmnic0', },
        'dv_port_group': { 'dv_portgroup_name': 'c4k4u14_dvpg', 'number_of_ports': '3', },
    }
}

esxi_hosts = {
    'nodek4' : {
        'ip' : k4,
        'vcenter_server':'vcenter1',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'cluster' : 'c4k4rack14',
        'datastore' : '/vmfs/volumes/k4-ds',
        'contrail_vm' : {
            'name' : 'nodek4-compute-vm',
            'mac' : '00:50:56:aa:aa:03',
            'host' : host4,
            'cluster' : 'c4k4rack14',
            'vmdk' : '/cs-shared/images/vcenter-vmdk/ContrailVM-disk1.vmdk',
        }
    },
    'nodek5' : {
        'vcenter_server':'vcenter1',
        'ip' : k5,
        'username' : 'root',
        'password' : 'c0ntrail123',
        'cluster' : 'c4k4rack14',
        'datastore' : '/vmfs/volumes/k5-ds',
        'contrail_vm' : {
            'name' : 'nodek5-compute-vm',
            'mac' : '00:50:56:aa:aa:04',
            'host' : host5,
            'vmdk' : '/cs-shared/images/vcenter-vmdk/ContrailVM-disk1.vmdk',
        }
    },
    'nodek6' : {
        'vcenter_server':'vcenter1',
        'ip' : k6,
        'username' : 'root',
        'password' : 'c0ntrail123',
        'cluster' : 'c4k4rack14',
        'datastore' : '/vmfs/volumes/k6-ds',
        'contrail_vm' : {
            'name' : 'nodek6-compute-vm',
            'mac' : '00:50:56:aa:aa:05',
            'host' : host6,
            'vmdk' : '/cs-shared/images/vcenter-vmdk/ContrailVM-disk1.vmdk',
        }
    },

}
# HA configuration:

if os.getenv('HA_TEST',None) == 'True':
    env.ha = {
        'contrail_internal_vip' : '10.204.216.252',
    }
    ha_setup = 'True'
    ipmi_username = 'ADMIN'
    ipmi_password = 'ADMIN'
    env.hosts_ipmi = {

    '10.204.216.61':'10.207.25.58',
    '10.204.216.62':'10.207.25.59',
    '10.204.216.61':'10.207.25.60',
    '10.204.216.224':'10.204.216.248',
    '10.204.216.225':'10.204.216.249',
    '10.204.216.226':'10.204.216.250',
    }

env.test = {
     'mail_to': 'dl-contrail-sw@juniper.net',
           }

minimum_diskGB=32
env.test_repo_dir='/home/stack/multi_interface_parallel/centos65/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
env.interface_rename = False
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario='Vcenter MultiNode Single Intf Sanity'
#do_parallel = True
env.ntp_server = '10.204.217.158'
env.optional_services = {
    'cfgm' : ['device-manager'],
}
