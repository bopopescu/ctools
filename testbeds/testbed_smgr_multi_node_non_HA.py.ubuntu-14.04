from fabric.api import env
 
host1 = 'root@10.204.217.61'
host2 = 'root@10.204.217.73'
host3 = 'root@10.204.217.98'
host4 = 'root@10.204.217.23'
host5 = 'root@10.204.217.57' 


ext_routers = [('mx2', '10.204.216.245')]
#ext_routers = []
router_asn = 64512
public_vn_rtgt = 11000
public_vn_subnet = "10.204.220.216/29"

 
#Host from which the fab commands are triggered to install and provision
host_build = 'stack@10.204.216.49'
 
env.roledefs = {

    'all': [host1, host2, host3, host4, host5],
    'cfgm': [host1, host3],
    'openstack': [host2],
    'control': [host2, host3],
    'compute': [host4, host5],
    'collector': [host1],
    'webui': [host1],
    'database': [host1, host2, host3],
    'build': [host_build],


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
 
env.hostnames ={
    'all': ['nodeg21', 'nodeg33', 'nodec58', 'nodec38', 'nodeg17']
}

env.ostypes = {
     host1 : 'ubuntu',
     host2 : 'ubuntu',
     host3 : 'ubuntu',
     host4 : 'ubuntu',
     host5 : 'ubuntu',
}
 
#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'


env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host_build: 'stack@123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
}


#To disable installing contrail interface rename package
env.interface_rename = False

#To enable multi-tenancy feature
multi_tenancy = True

#To Enable prallel execution of task in multiple nodes
#do_parallel = True
#haproxy = True
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.enable_lbaas = True
do_parallel = True
enable_ceilometer = True
ceilometer_polling_interval = 60
minimum_diskGB=32
env.test_repo_dir='/home/stack/smgr_github_ubuntu_multi_node/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
env.log_scenario='Server Manager Multi-Node Sanity'
