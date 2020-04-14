from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.204.217.112'

#External routers if any
#for eg.
ext_routers = [('mx2', '10.204.216.245')]
#ext_routers = []
router_asn = 64512
public_vn_rtgt = 11000
public_vn_subnet = "10.204.220.208/29"


#Host from which the fab commands are triggered to install and provision
host_build = 'stack@10.204.216.49'

#Role definition of the hosts.
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

env.hostnames = {
    'all': ['nodeh8']
}
env.physical_routers={
'blr-mx2'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'blr-mx2',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.216.245',
             }
}

env.ostypes = {
    host1:'ubuntu',
}

#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'
#Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',

    host_build: 'contrail123',
}

#To disable installing contrail interface rename package
env.interface_rename = True
minimum_diskGB=32

#To enable multi-tenancy feature
multi_tenancy = True

#To Enable prallel execution of task in multiple nodes
#do_parallel = True
#haproxy = True
env.test_repo_dir='/home/stack/smgr_github_ubuntu_single_node/contrail-test'
env.mail_to='dl-contrail-sw@juniper.net'
env.log_scenario='Server Manager Single-Node Sanity'
env.enable_lbaas = True
env.xmpp_auth_enable=True
env.xmpp_dns_auth_enable=True

#enable ceilometer
enable_ceilometer = True
ceilometer_polling_interval = 60
