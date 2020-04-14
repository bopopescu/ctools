from fabric.api import env
 
host1 = 'root@10.204.221.24'
host2 = 'root@10.204.221.27'
host3 = 'root@10.204.221.28'
host4 = 'root@10.204.221.25'
host5 = 'root@10.204.221.26' 

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
    'cfgm': [host1, host2, host3],
    'openstack':[host1, host2, host3],
    'control':[host1, host2, host3],
    'compute': [host4, host5],
    'collector': [host1, host2, host3],
    'webui': [host1, host2, host3],
    'database': [host1, host2, host3],
    'build': [host_build],


}
env.hostnames ={
    'all': ['nodeg34', 'nodec48', 'nodec49', 'nodec51', 'nodec63']
}
env.ostypes = {
     host1 : 'ubuntu',
     host2 : 'ubuntu',
     host3 : 'ubuntu',
     host4 : 'ubuntu',
     host5 : 'ubuntu',

}

os_username = 'admin'
os_password = 'c0ntrail123'
os_tenant_name = 'demo'

# VIP
env.ha = {
    'internal_vip' : '192.168.100.10',
    'external_vip' : '10.204.221.17',
}

# To Enable parallel execution of task in multiple nodes
do_parallel = False


control_data = {
    host1 : { 'ip': '192.168.100.5/24', 'gw' : '192.168.100.254', 'device':'p1p2' },
    host2 : { 'ip': '192.168.100.6/24', 'gw' : '192.168.100.254', 'device':'p1p2' },
    host3 : { 'ip': '192.168.100.7/24', 'gw' : '192.168.100.254', 'device':'p1p2' },
    host4 : { 'ip': '192.168.100.8/24', 'gw' : '192.168.100.254', 'device':'p1p2' },
    host5 : { 'ip': '192.168.100.9/24', 'gw' : '192.168.100.254', 'device':'p1p2' },
}

env.openstack_admin_password = 'contrail123'
env.password = 'c0ntrail123'
 
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host_build: 'secret',
}

 
env.cluster_id='cluster_bk'
minimum_diskGB=32
env.test_repo_dir='/homes/pbharat/github/contrail-test'
#env.mail_from='pbharat@juniper.net'
env.mail_to='dl-contrail-server-manager@juniper.net'
env.subject='Multi node sanity'

env.test = {
    'mail_to': 'dl-contrail-server-manager@juniper.net'
    }
