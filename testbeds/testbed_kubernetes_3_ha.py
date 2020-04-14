import os
from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.204.217.52'
host2 = 'root@10.204.217.71'
host3 = 'root@10.204.217.98'
host4 = 'root@10.204.217.100'
host5 = 'root@10.204.217.101'

ext_routers = [('hooper', '10.204.217.254')]
router_asn = 64512
public_vn_rtgt = 2225
public_vn_subnet = "10.204.221.160/29"

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
}
env.hostnames = {
    'all': ['nodeg12', 'nodeg31', 'nodec58',
             'nodec60', 'nodec61']
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
    host_build: 'c0ntrail123',
}
#To enable multi-tenancy feature
multi_tenancy = False
minimum_diskGB=32
#To Enable prallel execution of task in multiple nodes
#do_parallel = True
#haproxy = True
env.log_scenario='Kubernets HA Sanity'
env.test = {
  'mail_to' : 'vvelpula@juniper.net',
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
env.test_repo_dir='/root/vjoshi/contrail-tools/contrail-test'
env.orchestrator='kubernetes'

env.kubernetes = {
'mode' : 'baremetal',
'master': host1,
'slaves': [host4, host5]
}
