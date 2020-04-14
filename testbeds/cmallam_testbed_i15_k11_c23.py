from fabric.api import env

host1 = 'root@10.204.217.127'
host2 = 'root@10.204.216.231'
host3 = 'root@10.204.217.8'

ext_routers = [('mx1', '10.204.217.190')]
router_asn = 64510
public_vn_rtgt = 19006
#public_vn_subnet = "10.204.219.80/29"

host_build = 'cmallam@10.204.217.127'


env.roledefs = {
    'all': [host1, host2, host3],
    'cfgm': [host1],
    'webui': [host1],
    'openstack': [host1],
    'control': [host1],
    'collector': [host1],
    'database': [host1],
    'compute': [host2, host3],
    'build': [host_build]
}

env.hostnames = {
    'all': ['nodei15', 'nodek11', 'nodec23']
}
#env.interface_rename = False
#
#control_data = {
#    host1 : { 'ip': '192.168.250.1/24', 'gw' : '192.168.250.254', 'device':'eth0' },
#    host2 : { 'ip': '192.168.250.2/24', 'gw' : '192.168.250.254', 'device':'eth0' },
#    host3 : { 'ip': '192.168.250.3/24', 'gw' : '192.168.250.254', 'device':'eth0' },
#}

env.openstack_admin_password = 'contrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
}
minimum_diskGB=32
env.test_repo_dir='/root/contrail-test-merge/'
env.mail_from='cmallam@juniper.net'
env.mail_to='cmallam@juniper.net'
multi_tenancy=True
env.interface_rename = False
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario='Three node sanity'
env.enable_lbaas = True
