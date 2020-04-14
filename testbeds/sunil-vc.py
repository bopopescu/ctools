from fabric.api import env

nodea7 = '10.204.216.45'
nodeb3_vm = '10.204.216.180'
nodeb7_vm = '10.204.216.190'
nodeb3 = '10.204.216.34'
nodeb7 = '10.204.216.48'

host1 = 'root@' + nodea7
host2 = 'root@' + nodeb3_vm
host3 = 'root@' + nodeb7_vm
esx1 = 'root@' + nodeb3
esx2 = 'root@' + nodeb7

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

ext_routers = []
router_asn = 64510
public_vn_rtgt = 10003
public_vn_subnet = '10.204.219.64/29'

host_build = 'stack@10.204.216.56'

env.roledefs = {
    'all': [host1, host2, host3],
    'cfgm': [host1],
    'control': [host1],
    'compute': [host2, host3],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.orchestrator = 'vcenter' 
env.password = 'secret'

env.hostnames = {
    'all': ['nodea7', 'sunilvm1', 'sunilvm2' ]
}

env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host_build: 'c0ntrail123',
    esx1: 'c0ntrail123',
    esx2: 'c0ntrail123',
}

env.ostypes = {
   host1 : 'ubuntu',
   host2 : 'ubuntu',
   host3 : 'ubuntu',
}

env.vcenter = {
        'server':'10.204.217.189',
        'port': '443',
        'username': 'administrator@vsphere.local',
        'password': 'Contrail123!',
        'auth': 'https',
        'datacenter': 'sunil_dc',
        'cluster': ['s1', 's2'],
        'dv_switch': { 'dv_switch_name': 'sunil_dvswitch', 'nic': 'vmnic0', },
        'dv_port_group': { 'dv_portgroup_name': 'sunil_dvportgroup', 'number_of_ports': '3', },
}

esxi_hosts = {
    'nodeb3' : {
          'ip' : '10.204.216.34',
          'username' : 'root',
          'password' : 'c0ntrail123',
          'datastore' : '/vmfs/volumes/b3-ds',
          'cluster' : 's1',
          'contrail_vm' : {
               'name' : 'sunilvm1',
               'mac' : '00:50:56:aa:aa:01',
               'host' : host2,
               'vmdk' : '/root/Ubuntu-precise-14.04-LTS.vmdk'
          }
    },
    'nodeb7' : {
          'ip' : '10.204.216.38',
          'username' : 'root',
          'password' : 'c0ntrail123',
          'datastore' : '/vmfs/volumes/b7-ds',
          'cluster' : 's2',
          'contrail_vm' : {
               'name' : 'sunilvm2',
               'mac' : '00:50:56:aa:aa:02',
               'host' : host3,
               'vmdk' : '/root/Ubuntu-precise-14.04-LTS.vmdk'
          }
    }
}

minimum_diskGB=32

env.ntp_server = '10.204.217.158'
# Folder where you have checked out the field-test git repo
env.ntp_server = 'ntp.juniper.net'
env.mail_to = 'sunilbasker@juniper.net'
env.mail_server = '10.204.216.49'
env.mail_port = '25'
env.log_scenario = 'Vcenter'
env.test_repo_dir='/homes/sunilbasker/test'

