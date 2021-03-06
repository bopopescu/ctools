from fabric.api import env

host1 = 'root@10.204.217.217'

ext_routers = [('blr-mx1', '10.204.216.253')]
router_asn = 64004
public_vn_rtgt = 10003
public_vn_subnet = "10.204.219.40/29"

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1],
    'compute': [host1],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

analytics_aaa_mode = 'no-auth'

env.hostnames = {
    'all': ['nodel7']
}

env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'contrail123',
}
minimum_diskGB=32
env.test_repo_dir='/home/stack/centos_github_sanity/contrail-test'
env.mail_from='ankitja@juniper.net'

env.interface_rename=True 
env.encap_priority="'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario='Single Node Sanity'
env.enable_lbaas = True

env.physical_routers={
'blr-mx1'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'blr-mx1',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '10.204.216.253',
             }
}

env.test = {
'mail_to' : 'ankitja@juniper.net',
}

#enable ceilometer
enable_ceilometer = True
ceilometer_polling_interval = 60
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
