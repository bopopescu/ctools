import os
from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.204.217.108'
host2 = 'root@10.204.217.52'
host3 = 'root@10.204.217.71'
host4 = 'root@10.204.217.98'
host5 = 'root@10.204.217.100'
#host6 = 'root@10.204.217.101'

#External routers if any
#for eg. 
#ext_routers = [('mx1', '10.204.216.253')]
ext_routers = [('hooper', '77.77.1.100')]
router_asn = 64512
public_vn_rtgt = 12005
public_vn_subnet = "10.204.219.136/29"


#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.204.217.187'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3, host4, host5],
    'cfgm': [host1, host2, host3],
    'control': [host1, host2, host3],
    'compute': [host4, host5],
    'collector': [host1, host2, host3],
    'webui': [host1],
    'database': [host1, host2, host3],
    'build': [host_build],
    'contrail-kubernetes': [host1, host2, host3],
#    'contrail-lb' : [host6]
}

env.hostnames = {
#    'all': ['nodeh4', 'nodeg12', 'nodeg31', 'nodec58', 'nodec60', 'nodec61']
    'all': ['nodeh4', 'nodeg12', 'nodeg31', 'nodec58', 'nodec60']
}

#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'
#Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
#    host6: 'c0ntrail123',

    host_build: 'c0ntrail123',
}

#To enable multi-tenancy feature
multi_tenancy = False
minimum_diskGB=32
#To Enable prallel execution of task in multiple nodes
#do_parallel = True
#haproxy = True
env.log_scenario='Kubernets ontrol data insterface HA setup'

env.test = {
  'mail_to' : 'pulkitt@juniper.net',
  'webserver_host': '10.204.216.50',
  'webserver_user' : 'bhushana',
  'webserver_password' : 'c0ntrail!23',
  'webserver_log_path' :  '/home/bhushana/Documents/technical/logs',
  'webserver_report_path': '/home/bhushana/Documents/technical/sanity',
  'webroot' : 'Docs/logs',
  'mail_server' :  '10.204.216.49',
  'mail_port' : '25',
  'mail_sender': 'contrailbuild@juniper.net',
}
#image_name = os.getenv('IMAGE_NAME', 'centos-7.3-1611.qcow2.gz')

env.test_repo_dir='/root/pulkitt/contrail-tools/contrail-test'
env.orchestrator='kubernetes'


env.kubernetes = {
'mode' : 'baremetal',
'master': host1,
'slaves': [host2, host3, host4, host5]
}

control_data = {
    host1 : { 'ip': '77.77.1.10/24', 'gw' : '77.77.1.254', 'device': 'enp3s0f1' },
    host2 : { 'ip': '77.77.1.20/24', 'gw' : '77.77.1.254', 'device': 'enp1s0f1' },
    host3 : { 'ip': '77.77.1.30/24', 'gw' : '77.77.1.254', 'device': 'enp1s0f1' },
    host4 : { 'ip': '77.77.1.11/24', 'gw' : '77.77.1.254', 'device': 'enp2s0f1' },
    host5 : { 'ip': '77.77.1.21/24', 'gw' : '77.77.1.254', 'device': 'bond0' },
#    host6 : { 'ip': '77.77.1.31/24', 'gw' : '77.77.1.254', 'device': 'enp2s0f1' },
}

# 10.204.217.101 is the lb node nodec60
#env.ha = {
#    'contrail_external_vip' : '10.204.217.101'
#}
