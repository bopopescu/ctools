from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

host1 = 'root@10.204.217.139'
host2 = 'root@10.204.217.140'
host3 = 'root@10.204.217.142'
host4 = 'root@10.204.217.144'
host5 = 'root@10.204.217.147'
host6 = 'root@10.204.217.148'
host7 = 'root@10.204.217.149'
host8 = 'root@10.204.217.150'
#host9 = 'root@10.204.217.210'
#host10 = 'root@10.204.217.217'
#host11 = 'root@10.204.217.218'
#host12 = 'root@10.204.217.220'
#host13 = 'root@10.204.217.247'
#host14 = 'root@10.204.217.248'
#host15 = 'root@10.204.217.249'
host16 = 'root@10.204.217.118'
host17 = 'root@10.204.217.119'
host18 = 'root@10.204.217.120'
host21 = 'root@10.204.217.123'
host22 = 'root@10.204.217.124'

ext_routers = [('ishant', '192.168.1.200'), ('dhawan', '192.168.1.199')]
router_asn = 64501
public_vn_rtgt = 19005
public_vn_subnet = "10.204.220.64/26"

host_build = 'vjoshi@10.204.216.37'

env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6,host7, host8 ,host16,host17,host18,host21,host22],
    'cfgm': [host1, host2, host3],
    'openstack': [host4, host5, host6],
    'webui': [host1, host2, host3],
    'control': [host1, host2, host3],
    'compute': [host7, host8, host16,host17,host18,host21,host22],
    'collector': [host1, host2, host3],
    'database': [host1, host2, host3],
    'build': [host_build],
    'monitor': [host2],
}

env.hostnames = {
    'all': ['nodei27', 'nodei28', 'nodei30', 'nodei32', 'nodei35', 'nodei36', 'nodei37', 'nodei38', 'nodei6','nodei7','nodei8','nodei11','nodei12']
}

env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
    host7: 'c0ntrail123',
    host8: 'c0ntrail123',
#    host9: 'c0ntrail123',
#    host10: 'c0ntrail123',
#    host11: 'c0ntrail123',
#    host12: 'c0ntrail123',
#    host13: 'c0ntrail123',
#    host14: 'c0ntrail123',
#    host15: 'c0ntrail123',
    host16: 'c0ntrail123',
    host17: 'c0ntrail123',
    host18: 'c0ntrail123',
    host21: 'c0ntrail123',
    host22: 'c0ntrail123',

    host_build: 'c0ntrail123'
}


env.mail_from='contrail-build@juniper.net'
env.mail_to='vjoshi@juniper.net'
multi_tenancy=True
env.interface_rename=True
do_parallel=True
env.enable_lbaas = True

env.ha = {
    'internal_vip' : '192.168.1.100',
    'contrail_internal_vip' : '192.168.1.101',
    'external_vip' : '10.204.217.87',
    'contrail_external_vip' : '10.204.217.178',
    'internal_virtual_router_id' :  222,
    'external_virtual_router_id' :  223,
    'contrail_internal_virtual_router_id' :  224,
    'contrail_external_virtual_router_id' :  225,
}

control_data = {
    host1 : { 'ip': '192.168.1.2/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
    host2 : { 'ip': '192.168.1.3/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
    host3 : { 'ip': '192.168.1.24/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
    host4 : { 'ip': '192.168.1.4/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
    host5 : { 'ip': '192.168.1.5/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
    host6 : { 'ip': '192.168.1.6/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
    host7 : { 'ip': '192.168.1.7/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
    host8 : { 'ip': '192.168.1.8/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
#    host9 : { 'ip': '192.168.1.9/24', 'gw' : '192.168.1.254', 'device':'em2' },
#    host10 : { 'ip': '192.168.1.10/24', 'gw' : '192.168.1.254', 'device':'em2' },
#    host11 : { 'ip': '192.168.1.11/24', 'gw' : '192.168.1.254', 'device':'em2' },
#    host12 : { 'ip': '192.168.1.12/24', 'gw' : '192.168.1.254', 'device':'em2' },
#    host13 : { 'ip': '192.168.1.13/24', 'gw' : '192.168.1.254', 'device':'em2' },
#    host14 : { 'ip': '192.168.1.14/24', 'gw' : '192.168.1.254', 'device':'em2' },
#    host15 : { 'ip': '192.168.1.15/24', 'gw' : '192.168.1.254', 'device':'em2' },
    host16 : { 'ip': '192.168.1.16/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
    host17 : { 'ip': '192.168.1.17/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
    host18 : { 'ip': '192.168.1.18/24', 'gw' : '192.168.1.254', 'device':'p6p2' },
#    host19 : { 'ip': '192.168.1.19/24', 'gw' : '192.168.1.254', 'device':'p6p1' },
#    host20 : { 'ip': '192.168.1.20/24', 'gw' : '192.168.1.254', 'device':'p6p1' },
    host21 : { 'ip': '192.168.1.21/24', 'gw' : '192.168.1.254', 'device':'p6p1' },
    host22 : { 'ip': '192.168.1.22/24', 'gw' : '192.168.1.254', 'device':'p6p1' },
#    host23 : { 'ip': '192.168.1.23/24', 'gw' : '192.168.1.254', 'device':'p6p1' },
}

#env.test_repo_dir='/root/contrail-test'
env.test_repo_dir='/root/sandipd/contrail-test'
