from fabric.api import env
import os

os_username = 'admin'
os_password = 'c0ntrail123'
os_tenant_name = 'admin'

host1 = 'root@10.204.216.94'

ext_routers = [('yuvaraj', '10.204.217.190')]
router_asn = 64510
public_vn_rtgt = 19005
public_vn_subnet = "10.204.219.88/29"

#host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1],
    'contrail-controller': [host1],
    'openstack': [host1],
    'contrail-analytics': [host1],
    'contrail-analyticsdb': [host1],
    'contrail-compute': [host1],
}

if os.getenv('AUTH_PROTOCOL',None) == 'https':
    env.log_scenario = 'Multi-Interface HA Sanity[mgmt, ctrl=data, SSL]'
    env.keystone = {
        'auth_protocol': 'https'
    }
    env.cfgm = {
        'auth_protocol': 'https'
    }
else:
    env.log_scenario = 'Multi-Interface HA Sanity[mgmt, ctrl=data]'

if os.getenv('ENABLE_RBAC',None) == 'true':
    cloud_admin_role = 'admin'
    aaa_mode = 'rbac'

env.physical_routers={
'yuvaraj'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'yuvaraj',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.190',
             }
}

env.hostnames = {
    'all': ['nodem5']
}
env.openstack_admin_password = 'c0ntrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
}

env.ostypes = {
    host1: 'ubuntu',
}

env.kernel_upgrade=False
env.openstack = {
    'manage_amqp': "true",
}

env.keystone = {
     'admin_password': 'c0ntrail123',
}


#env.cluster_id='clusterm5m6m7m8m9m10'
minimum_diskGB = 32
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
#env.test_repo_dir = '/home/stack/regression/contrail-test'
env.mail_from = 'contrail-build@juniper.net'
env.mail_to = 'dl-contrail-sw@juniper.net'
multi_tenancy = True
env.interface_rename = True
env.log_scenario = 'SMLite Single Node Container Sanity'
env.enable_lbaas = True
do_parallel = True
#enable_ceilometer = True
#ceilometer_polling_interval = 60
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
#  'fip_pool_name': 'floating-ip-pool',
#  'public_virtual_network': 'public',
#  'public_tenant_name' : 'admin',
#  'fixture_cleanup' : 'yes',
#   'keypair_name': 'contrail_key',  
}
env.test_repo_dir='/root/contrail-test'
