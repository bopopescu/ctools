from fabric.api import env
 
host1 = 'root@10.204.217.62'
host2 = 'root@10.204.217.63'


#ext_routers = [('mx2', '10.204.216.245')]
ext_routers = []
router_asn = 64512
public_vn_rtgt = 11000
public_vn_subnet = "10.204.220.216/29"

 
#Host from which the fab commands are triggered to install and provision
host_build = 'stack@10.204.216.49'
 
env.roledefs = {

    'all': [host1, host2],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1],
    'compute': [host2],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
    'storage-main': [host1],
    'storage-compute': [ host2],

}
 
env.hostnames ={
    'all': ['nodeg22', 'nodeg23']
}

env.ostypes = {
     host1 : 'ubuntu',
     host2 : 'ubuntu',
}
 
#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'


env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',

    host_build: 'contrail123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
}


#To disable installing contrail interface rename package
#env.interface_rename = False

#To enable multi-tenancy feature
multi_tenancy = True

#To Enable prallel execution of task in multiple nodes
#do_parallel = True
#haproxy = True
env.test_repo_dir='/home/stack/smgr_github_ci/contrail-test'
env.mail_to='dl-contrail-server-manager@juniper.net'
env.log_scenario='Server Manager CI Sanity'


                                                                   
storage_node_config = {
    host2 : { 'disks' : ['/dev/sdb'] , 'journal' : ['/dev/sdb'] },
}

storage_replica_size = 2

minimum_diskGB = 32

env.test = {
'mail_to': 'dl-contrail-server-manager@juniper.net',
}
