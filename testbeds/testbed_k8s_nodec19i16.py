from fabric.api import env
import os


os_username = 'admin'
os_password = 'c0ntrail123'
os_tenant_name = 'admin'

host1 = 'root@10.204.217.4'
host2 = 'root@10.204.217.128'

ext_routers = [('blr-mx2', '10.204.216.245')]
router_asn = 64512
public_vn_rtgt = 11314
public_vn_subnet = '10.204.219.48/29'

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2],
    'cfgm': [host1],
    'openstack': [host1],
    'webui': [host1],
    'control': [host1],
    'compute': [host2],
    'collector': [host1],
    'database': [host1],
    'build': [host_build],
    'contrail-kubernetes': [host1]
}

env.physical_routers={
'blr-mx2'     : {    'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'blr-mx2',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.216.245',
             }
}

env.hostnames = {
    'all': ['nodec19','nodei16']
}


env.password = 'c0ntrail123'
env.openstack_admin_password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host_build: 'stack@123'
}
env.test = {
  'mail_to' : 'dl-contrail-sw@juniper.net',
  'webserver_host': '10.204.216.50',
  'webserver_user' : 'bhushana',
  'webserver_password' : 'bhu@123',
  'webserver_log_path' :  '/home/bhushana/Documents/technical/logs',
  'webserver_report_path': '/home/bhushana/Documents/technical/sanity',
  'webroot' : 'Docs/logs',
  'mail_server' :  '10.204.216.49',
  'mail_port' : '25',
  'mail_sender': 'contrailbuild@juniper.net'
}
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
}
env.log_scenario='Kubernetes Single Yaml Sanity'
env.orchestrator='kubernetes'
env.kubernetes = {
   'mode' : 'baremetal',
   'main': host1,
   'subordinates': [host2]
}

#env.cluster_id='clusterc19i16i18'
minimum_diskGB = 32
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
env.test_repo_dir = '/root/contrail-test'
env.mail_from = 'contrail-build@juniper.net'
env.mail_to = 'dl-contrail-sw@juniper.net'
multi_tenancy = True
env.enable_lbaas = True
do_parallel = True
#env.xmpp_auth_enable=True
#env.xmpp_dns_auth_enable=True
