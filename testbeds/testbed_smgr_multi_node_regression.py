from fabric.api import env
 
host1 = 'root@10.204.217.159'


ext_routers = [('mx2', '10.204.216.245')]
#ext_routers = []
router_asn = 64512
public_vn_rtgt = 11000
public_vn_subnet = "10.204.220.216/29"

 
#Host from which the fab commands are triggered to install and provision
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
 
env.hostnames ={
    'all': ['nodej3']
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
     host1 : 'ubuntu',
}
 
#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'


env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'contrail123',
}

#To disable installing contrail interface rename package
#env.interface_rename = False

#To enable multi-tenancy feature
multi_tenancy = True

#To Enable prallel execution of task in multiple nodes
#do_parallel = True
#haproxy = True
env.test_repo_dir='/home/stack/smgr_github_ubuntu_multi_node/contrail-test'
env.mail_to='ritam@juniper.net'
env.log_scenario='Server Manager Multi-Node Regression'

env.test = {
'mail_to': 'ritam@juniper.net',
}

