from fabric.api import env
import os


os_username = 'admin'
os_password = 'c0ntrail123'
os_tenant_name = 'admin'

host1 = 'root@10.204.217.52'
host2 = 'root@10.204.217.100'
host3 = 'root@10.204.217.101'

ext_routers = [('hooper', '10.204.217.240')]
router_asn = 64512
public_vn_rtgt = 2225
public_vn_subnet = "10.204.221.160/29"

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2, host3],
    'cfgm': [host1],
    'openstack': [host1],
    'webui': [host1],
    'control': [host1],
    'compute': [host2, host3],
    'collector': [host1],
    'database': [host1],
    'build': [host_build],
    'contrail-kubernetes': [host1]
}

env.physical_routers={
'hooper'     : {    'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'hooper',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.240',
             }
}

env.hostnames = {
    'all': ['nodeg12','nodec60', 'nodec61']
}


env.password = 'c0ntrail123'
env.openstack_admin_password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host_build: 'stack@123'
}
env.test = {
  'mail_to' : 'vvelpula@juniper.net',
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
    host3: 'ubuntu',
}
env.log_scenario='Kubernetes Single Yaml Sanity'
env.orchestrator='kubernetes'
env.kubernetes = {
   'mode' : 'baremetal',
   'main': host1,
   'subordinates': [host2, host3]
}

#env.cluster_id='clusterc19i16i18'
minimum_diskGB = 32
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
env.test_repo_dir = '/root/contrail-test'
env.mail_from = 'contrail-build@juniper.net'
env.mail_to = 'vvelpula@juniper.net'
multi_tenancy = True
env.enable_lbaas = True
do_parallel = True
#env.xmpp_auth_enable=True
#env.xmpp_dns_auth_enable=True
