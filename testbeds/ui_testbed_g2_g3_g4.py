from fabric.api import env

host1 = 'root@10.204.217.42'
host2 = 'root@10.204.217.43'
host3 = 'root@10.204.217.44'
host4 = 'root@10.204.217.47'
ext_routers = []
router_asn = 64512

host_build = 'stack@10.204.216.49'


env.roledefs = {
    'all': [host1, host2, host3, host4],
    'cfgm': [host1],
    'webui': [host1, host2, host3],
    'openstack': [host2],
    'control': [host1, host2, host3],
    'collector': [host1, host2, host3],
    'database': [host1],
    'compute': [host1, host2, host3, host4],
    'build': [host_build]
}

env.hostnames = {
    'all': ['nodeg2', 'nodeg3', 'nodeg4', 'nodeg7']
}

env.openstack_admin_password = 'contrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host_build: 'stack@123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
}
minimum_diskGB=32
multi_tenancy=True
env.interface_rename = False
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.enable_lbaas = True
