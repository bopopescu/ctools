from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.204.221.26'

#External routers if any
#for eg.
#ext_routers = [('mx1', '10.204.216.253')]
ext_routers = [('blr-mx1', '10.204.216.253')]
router_asn = 64512
public_vn_rtgt = 10003
public_vn_subnet = "10.204.219.184/29"


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
    'all': ['nodec63']
}

#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'
#Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'stack@123',
}


env.ostypes = {
    host1:'ubuntu',
}

env.physical_routers={
'blr-mx1'     : {    'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'blr-mx1',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '10.204.216.253',
             }
}

#To disable installing contrail interface rename package
env.interface_rename = True
minimum_diskGB=32
#To enable multi-tenancy feature
multi_tenancy = True

env.xmpp_auth_enable=True
env.xmpp_dns_auth_enable=True
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
env.test_repo_dir='/home/stack/github_ubuntu_single_node/havana/contrail-test'
env.mail_to='ritam@juniper.net'
env.log_scenario='Container Single Node Sanity'
env.enable_lbaas = True

#enable ceilometer
enable_ceilometer = True
ceilometer_polling_interval = 60

