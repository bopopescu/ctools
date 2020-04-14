from fabric.api import env
 
host1 = 'root@10.204.221.33'
host2 = 'root@10.204.221.34'
host3 = 'root@10.204.221.35'
host4 = 'root@10.204.221.36'
host5 = 'root@10.204.221.37' 

host_build = 'pbharat@10.204.217.4'
#multi_tenancy = True
#env.interface_rename = True
#webui = True 
#ext_routers = [('mx1', '10.204.216.253')]
ext_routers = []
router_asn = 64512
public_vn_rtgt = 10003
public_vn_subnet = "10.204.219.72/28"
 
 
env.roledefs = {

    'all': [host1, host2, host3, host4, host5],
    'cfgm': [host1, host3],
    'openstack':[host2],
    'control':[host2, host3],
    'compute': [host4, host5],
    'collector': [host1],
    'webui': [host1],
    'database': [host1, host2, host3],
    'build': [host_build],


}
 
env.hostnames ={
    'all': ['nodec42', 'nodec44', 'nodec45', 'nodec46', 'nodec47']
}
env.ostypes = {
     host1 : 'ubuntu',
     host2 : 'ubuntu',
     host3 : 'ubuntu',
     host4 : 'ubuntu',
     host5 : 'ubuntu',

}
 
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host_build: 'secret',
}
 
env.test_repo_dir='/homes/pbharat/github/contrail-test'
#env.mail_from='pbharat@juniper.net'
env.mail_to='dl-contrail-server-manager@juniper.net'
env.test = {
    'mail_to': 'dl-contrail-server-manager@juniper.net'
    }

