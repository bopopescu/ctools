import os
from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.204.217.4'
host2 = 'root@10.204.217.5'
host3 = 'root@10.204.217.6'
host4 = 'root@10.204.217.128'
host5 = 'root@10.204.217.130'

#External routers if any
ext_routers = [('blr-mx2', '192.168.10.100')]
router_asn = 64512
public_vn_rtgt = 11314
public_vn_subnet = "10.204.219.48/29"


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
    'all': ['nodec19', 'nodec20', 'nodec21', 'nodei16', 'nodei18']
}
#Openstack admin password
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
env.log_scenario='Kubernets control data insterface With HA'

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

env.test_repo_dir='/root/contrail-test'
env.orchestrator='kubernetes'

env.kubernetes = {
'mode' : 'baremetal',
'master': host2,
'slaves': [host4, host5]
}

control_data = {
    host1 : { 'ip': '192.168.10.1/24', 'gw' : '192.168.10.100', 'device': 'enp1s0f1' },
    host2 : { 'ip': '192.168.10.2/24', 'gw' : '192.168.10.100', 'device': 'enp1s0f1' },
    host3 : { 'ip': '192.168.10.3/24', 'gw' : '192.168.10.100', 'device': 'enp1s0f1' },
    host4 : { 'ip': '192.168.10.5/24', 'gw' : '192.168.10.100', 'device': 'bond0' },
    host5 : { 'ip': '192.168.10.6/24', 'gw' : '192.168.10.100', 'device': 'bond0' },
}
