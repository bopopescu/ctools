from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'
#multi_tenancy = True
webui = True
horizon = False
ui_config = 'contrail'
ui_browser = 'firefox'

host1 = 'root@10.204.221.24'
host2 = 'root@10.204.221.25'
host3 = 'root@10.204.221.26'
host4 = 'root@10.204.221.27'
host5 = 'root@10.204.221.28'

ext_routers = []
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = "10.84.41.0/24"

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2, host3, host4, host5],
    'contrail-controller': [host2],
    'openstack': [host1],
    'contrail-analytics': [host1],
    'contrail-analyticsdb': [host1, host2, host3],
    'contrail-compute': [host4, host5],
    'build': [host_build],
}

env.hostnames = {
    'all': ['nodeg34', 'nodec51', 'nodec63', 'nodec48', 'nodec49']
}

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

#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.kernel_upgrade=False

env.openstack = {
    'manage_amqp': "true"
}

env.keystone = {
    'admin_password': 'contrail123'
}

minimum_diskGB=32
env.mail_from='musharani@juniper.net'
env.mail_to='musharani@juniper.net'
env.log_scenario ='Multi Node Webui Sanity'
