from fabric.api import env
 
# Contrail Config Nodes
host1 = 'heat-admin@CONFIG1'
 
# Compute Nodes
host2 = 'heat-admin@compute1'
host3 = 'heat-admin@compute2'

# Openstack Nodes
host4 = 'heat-admin@openstack1'
 
#Contrail-Analytics
host5 = 'heat-admin@analytics1'

#contrail-analytics-database
host6 = 'heat-admin@analytics-db1'

# TWO HYPERVIOSR 140 and 139 needs to add 139
hypervisor_host = 'root@10.87.67.44'
hypervisor_host_stack = 'stack@10.87.67.44'
undercloud_host = 'root@10.87.67.231'
undercloud_host_stack = 'stack@10.87.67.231'

#External routers if any
#for eg.
ext_routers = []
rh_username = 'aranjan.redhat'
rh_password = 'H3Ub9pth3x'
rh_pool_id = '8a85f9895cce2f3a015ccf0eb79749f8' 
#Autonomous system number
router_asn = 64512
 
#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.84.5.31'
 
#Role definition of the hosts.
env.roledefs = {
	'all': [host1, host2, host3, host4 , host5 , host6],
	'openstack': [host4],
	'cfgm': [host1],
	'control': [host1],
	'compute': [host2, host3],
	'collector': [host5],
	'database': [host6],
        'undercloud' : [undercloud_host],
        'rh_hypervisor' : [ hypervisor_host ],
	'build': [host_build],
}
 
#Hostnames
env.hostnames = {
	host1: 'contrail-controller.localdomain',
	host2: 'compute.localdomain',
        host3: 'compute2.localdomain',
	host4: 'controller.localdomain',
        host5: 'contrail-analytics.localdomain',
        host6: 'contrail-analytics-database.localdomain',
        undercloud_host: 'uc-newtonX.example.com',
        undercloud_host_stack:'undercloud.example.com',

}
 
env.passwords = {
	host1: 'SSH-KEY-SHARED',
	host2: 'SSH-KEY-SHARED',
	host3: 'SSH-KEY-SHARED',
	host4: 'SSH-KEY-SHARED',
	host5: 'SSH-KEY-SHARED',
	host6: 'SSH-KEY-SHARED',
        undercloud_host: 'c0ntrail123',
        hypervisor_host: 'c0ntrail123',
        hypervisor_host_stack: 'c0ntrail123',
        undercloud_host_stack: 'c0ntrail123',
}
 
 
#Openstack admin password. Retrieve OVERCLOUD_ADMIN_PASSWORD from /home/stack/tripleo-overcloud-passwords in undercloud node
env.openstack_admin_password = 'PASSWORD_ADMIN'
 
env.ostypes = {
	host1: 'redhat',
	host2: 'redhat',
	host3: 'redhat',
	host4: 'redhat',
	host5: 'redhat',
	host6: 'redhat',
}
 
minimum_diskGB = 5
 
#OPTIONAL BONDING CONFIGURATION
#==============================
 
#OPTIONAL SEPARATION OF MANAGEMENT AND CONTROL + DATA and OPTIONAL VLAN INFORMATION
#==================================================================================
control_data = {
	host1  : { 'ip': '10.0.0.40/24', 'gw' : '10.0.0.1', 'device':'eth2' },
	host2  : { 'ip': '10.0.0.41/24', 'gw' : '10.0.0.1', 'device':'eth2' },
	host3  : { 'ip': '10.0.0.42/24', 'gw' : '10.0.0.1', 'device':'eth2' },
	host7  : { 'ip': '10.0.0.30/24', 'gw' : '10.0.0.1', 'device':'vhost0' },
        # needs to add hos 8 9 and 20 update IP ADDRESS
        host8  : { 'ip': '10.0.0.31/24', 'gw' : '10.0.0.1', 'device':'vhost0' },
        host9  : { 'ip': '10.0.0.32/24', 'gw' : '10.0.0.1', 'device':'vhost0' },
        host20  : { 'ip': '10.0.0.33/24', 'gw' : '10.0.0.1', 'device':'vhost0' },
	host10  : { 'ip': '10.0.0.20/24', 'gw' : '10.0.0.1', 'device':'eth2' },
        host11  : { 'ip': '10.0.0.21/24', 'gw' : '10.0.0.1', 'device':'eth2' },
        host12  : { 'ip': '10.0.0.22/24', 'gw' : '10.0.0.1', 'device':'eth2' },
#	host13  : { 'ip': '10.0.0.22/24', 'gw' : '10.0.0.1', 'device':'eth2' },
        host14  : { 'ip': '10.0.0.50/24', 'gw' : '10.0.0.1', 'device':'eth2' },
        host15  : { 'ip': '10.0.0.51/24', 'gw' : '10.0.0.1', 'device':'eth2' },
        host16  : { 'ip': '10.0.0.52/24', 'gw' : '10.0.0.1', 'device':'eth2' },
        host17  : { 'ip': '10.0.0.60/24', 'gw' : '10.0.0.1', 'device':'eth2' },
        host18  : { 'ip': '10.0.0.61/24', 'gw' : '10.0.0.1', 'device':'eth2' },
        host19  : { 'ip': '10.0.0.62/24', 'gw' : '10.0.0.1', 'device':'eth2' },

}
 
env.interface_rename = False
 
env.keystone = {
	'keystone_ip' 	: 'IP_KEYSTONE',            # Keystone external VIP
	'auth_protocol'   : 'http',              	#Default is http
	'auth_port'   	: '35357',             	#Default is 35357
	'admin_token' 	: 'TOKEN_ADMIN',  #OVERCLOUD_ADMIN_TOKEN
	'admin_user'  	: 'admin',             	#Default is admin
	'admin_password'  : 'overcloud_admin_pass',   #OVERCLOUD_ADMIN_PASSWORD

	'nova_password'   : 'PASSWORD_NOVA', #OVERCLOUD_NOVA_PASSWORD
	'neutron_password': 'PASSWORD_NEUTRON', #OVERCLOUD_NEUTRON_PASSWORD
	'service_tenant'  : 'service',           	# Service tenant name of services like nova
	'admin_tenant'	: 'admin',             	# Admin tenant name of keystone admin user
	'region_name' 	: 'regionOne',         	#Default is RegionOne
	'insecure'    	: 'True',              	#Default = False
	'manage_neutron'  : 'yes',                    #Default = 'yes' , Does configure neutron user/role in keystone required.
       'manage_neutron_server'  : 'no',          # Avoid installing neutron-server in contrail controller nodes
}
 
env.ha = {
    #'contrail_internal_vip'   : 'IP_KEYSTONE',   	#Internal Virtual IP of the contrail HA Nodes.
    #'contrail_external_vip'   : '10.87.67.11',   	#External Virtual IP of the contrail HA Nodes.
}
 

env.openstack = {
 	'service_token' : 'TOKEN_ADMIN', # OVERCLOUD_ADMIN_TOKEN
# 	'amqp_hosts' : '10.87.67.20',  # IP of AMQP Server in first openstack node
 	'manage_amqp' : 'no',             	# Manage seperate AMQP for openstack services in openstack nodes.
     'osapi_compute_workers' : 40,         # Default 40, For low memory system reduce the osapi compute workers thread.
 	'conductor_workers' : 40,         	# Default 40, For low memory system reduce the conductor workers thread.
}

#Config node related config knobs
#amqp_hosts : List of customer deployed AMQP servers to be used by config services.
#amqp_port : Port of the customer deployed AMQP servers.
env.cfgm = {
##    'amqp_hosts' : ['10.0.0.20', ],
    'amqp_port' : '5672',
    'amqp_password' : 'PASSWORD_RABBITMQ' # OVERCLOUD_RABBITMQ_PASSWORD
}

env.osp = {
    'osp_version' : '11',
    'rh_username' : 'aranjan.redhat',
    'rh_password' : 'H3Ub9pth3x',
    'rh_pool_id' : '8a85f9895cce2f3a015ccf0eb79749f8',
    'NtpServer' : '10.84.5.100',
    'DnsServers' : '10.84.5.100',
    'ExternalNetCidr' : '10.87.67.128/25',
    'ExternalAllocationPools' : "[{'start': '10.87.67.212', 'end': '10.87.67.226'}]",
    'VrouterPhysicalInterface' : 'eno1',
    'PublicVirtualInterface' : 'eth1',
    'ExternalInterfaceDefaultRoute' : '10.87.67.254',
    'ControlPlaneIp' : 'enp129s0f0',
    'ExternalIP' : 'eno1',
}
env.test = {
    'webserver_user' : 'bhushana',
    'webserver_password' : 'bhu@123',
    'webserver_report_path': '/home/bhushana/Documents/technical/sanity',
    'webroot' : 'Docs/logs',
    'mail_sender': 'contrailbuild@juniper.net',
    'webserver_log_path' :  '/home/bhushana/Documents/technical/logs',
    'webserver_host': '10.204.216.50',
    'mail_from' : 'shajuvk@juniper.net',
    'mail_to' : 'shajuvk@juniper.net',
    'mail_server' : '10.84.24.64',
    'mail_port' : '4000',
    'enable_lbaas' : True,
    'enable_ceilometer' : True,
    'ceilometer_polling_interval' : '60',
    'image_web_server' : '10.84.5.120',
    'testbed_location' : 'US',
    'ntp_server' : '10.84.5.100',
}
