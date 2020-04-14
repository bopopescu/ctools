from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'admin'

host1 = 'root@10.204.217.206'
host2 = 'root@10.204.217.122'
host3 = 'root@10.204.217.93'
host4 = 'root@10.204.217.94'
host5 = 'root@10.204.217.95'
host6 = 'root@10.204.217.96'

ext_routers = [('yuvaraj', '22.22.22.2')]
router_asn = 64510
public_vn_rtgt = 19005
public_vn_subnet = "10.204.219.88/29"

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6],
    'contrail-compute': [host1, host2],
    'openstack': [host3],
    'contrail-controller': [host4],
    'contrail-analytics': [host5, host6],
    'contrail-analyticsdb': [host4, host5, host6],
    'build': [host_build],
}
env.physical_routers={
'yuvaraj'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'yuvaraj',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.190',
             }
}

env.hostnames = {
    'all': ['nodel1', 'nodei10', 'nodec53', 'nodec54', 'nodec55', 'nodec56']
}

control_data = {

    host1: {'ip': '22.22.22.1/24', 'gw': '22.22.22.2', 'device': 'p514p2'},
    host2: {'ip': '22.22.22.10/24', 'gw': '22.22.22.2', 'device': 'p6p2'},
    host3: {'ip': '22.22.22.53/24', 'gw': '22.22.22.2', 'device': 'p1p2'},
    host4: {'ip': '22.22.22.54/24', 'gw': '22.22.22.2', 'device': 'p1p2'},
    host5: {'ip': '22.22.22.55/24', 'gw': '22.22.22.2', 'device': 'p1p2'},
    host6: {'ip': '22.22.22.56/24', 'gw': '22.22.22.2', 'device': 'p1p2'},
}

env.password = 'c0ntrail123'
env.openstack_admin_password = 'contrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',

    host_build: 'stack@123',
}

env.kernel_upgrade=False
env.openstack = {
    'manage_amqp': "true"
}

env.keystone = {
    'admin_password': 'contrail123'
}


env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
    host6: 'ubuntu',
}
#use_devicemanager_for_md5 = True
env.cluster_id='clusterc53c54c55c56l1i10'
minimum_diskGB = 32
env.encap_priority="VXLAN,MPLSoUDP,MPLSoGRE"
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
env.test_repo_dir = '/home/stack/regression/contrail-test'
env.mail_from = 'contrail-build@juniper.net'
env.mail_to = 'dl-contrail-sw@juniper.net'
multi_tenancy = True
env.interface_rename = True
env.log_scenario = 'MultiNode MulltiIntf SMLite Container Sanity'
env.enable_lbaas = True
do_parallel = True
