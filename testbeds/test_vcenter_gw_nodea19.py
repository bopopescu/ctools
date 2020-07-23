from fabric.api import env
import os


host1 = 'root@10.204.216.7'
host2 = 'root@10.204.216.10'
host3 = 'root@10.204.217.121'
host4 = 'root@10.204.217.45'

ext_routers = [('blr-mx1', '10.204.216.253')]
router_asn = 64510
public_vn_rtgt = 19006
public_vn_subnet = "10.204.219.80/29"

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [ host1, host2, host3, host4],
    'cfgm': [host1],
    'openstack': [host4],
    'webui': [host1],
    'control': [host1],
    'collector': [host1],
    'database': [host1],
    'compute': [host2,host3],
    'build': [host_build]
}

if os.getenv('AUTH_PROTOCOL',None) == 'https':
    env.keystone = {
        'auth_protocol': 'https'
    }   
    env.cfgm = {
        'auth_protocol': 'https'
    }   

env.hostnames = {
    'all': ['nodea11', 'nodea14','nodei9', 'nodeg5']
}

env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host_build: 'stack@123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
}

}

env.orchestrator = 'openstack'
env.other_orchestrators={
'orch1'             :{
                         'name'         : 'vcenter',
                         'type'         : 'vcenter',
                         'vcenter_server': 'vcenter10',
                         'gateway_vrouters' : ['nodei9'],
                        }
 }    

#env.subordinate_orchestrator = 'vcenter'
control_data = {
    host1 : { 'ip': '192.168.250.4/24', 'gw' : '192.168.250.254', 'device':'em1' },
    host2 : { 'ip': '192.168.250.5/24', 'gw' : '192.168.250.254', 'device':'em1' },
    host3 : { 'ip': '192.168.250.19/24', 'gw' : '192.168.250.254', 'device':'p6p2' },
    host4 : { 'ip': '192.168.250.6/24', 'gw' : '192.168.250.254', 'device':'p1p2' },
}

env.physical_routers={
'nodei9'     : {       
                     'name'  : 'nodei9',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.121',
                     'ports' : ['p6p1'],
                     'type'  : 'vcenter_gateway',
             },
}

env.compute_as_gateway_mode = {
   host3 : 'server',
}

env.vcenter_servers = {
    'vcenter10': {
        'server':'10.204.217.189',
        'port': '443',
        'username': 'administrator@vsphere.local',
        'password': 'Contrail123!',
        'auth': 'https',
        'datacenters':{
        'a11a29':{
            'dv_switches': {
                'Distributed_Switch':{
                    'dv_switch_version': '5.5.0', 
                'clusters': ['a11a29_blr'],
             },
     },
   },
  },
 },
}

esxi_hosts = {
    'nodel5' : {
        'ip' : '10.204.217.212',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'cluster' : 'a11a29_blr',
        'datastore' : '/vmfs/volumes/l5-ds',
        'vcenter_server': 'vcenter10',
        'skip_reimage'  : 'true' 
        },
    'nodel6' : {
        'ip' : '10.204.217.215',
        'username' : 'root',
        'password' : 'c0ntrail123',
       'cluster' : 'a11a29_blr',
        'vcenter_server': 'vcenter10',
        'datastore' : '/vmfs/volumes/l6-ds',
        'skip_reimage'  : 'true' 
    },

}

env.test = {
  'mail_to' : 'dl-contrail-sw@juniper.net',
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

env.cluster_id='cluster_vrouter_gw'
minimum_diskGB=32
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename = False
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario='Vcenter Gateway'
env.enable_lbaas = True
do_parallel = True
env.ntp_server = 'ntp.juniper.net'

#enable ceilometer
enable_ceilometer = True
ceilometer_polling_interval = 60
env.test_repo_dir='/root/contrail-test-ci'
