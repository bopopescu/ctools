from fabric.api import env
 
host1 = 'root@10.204.221.3'
 

host_build = 'pbharat@10.204.216.4'
multi_tenancy = True
#env.interface_rename = True
ext_routers = []
router_asn = 64512
public_vn_rtgt = 10003
public_vn_subnet = "10.204.219.72/28"
 
 
env.roledefs = {

    'all': [host1],
    'cfgm': [host1],
    'openstack':[host1],
    'control': [host1],
    'compute': [host1],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],


}
 
env.hostnames ={
    'all': ['nodec50']
}
 
env.passwords = {
    host1: 'c0ntrail123',
    
    host_build: 'secret',
}
env.ostypes = {
   # host1: 'centos'
   host1: 'ubuntu'

}

#webui=True
#webui = True
#horizon = False
#ui_config = 'contrail'
#ui_browser = 'firefox'
 
env.test_repo_dir='/homes/pbharat/github/2187/contrail-test'
#env.mail_from='pbharat@juniper.net'
#env.mail_to='pbharat@juniper.net'
env.mail_to= 'dl-contrail-server-manager@juniper.net'
env.log_scenario='Single-Node Sanity'

env.test = {
    'mail_to': 'dl-contrail-server-manager@juniper.net'
    }
