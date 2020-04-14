from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.87.121.34'
host2 = 'root@10.87.121.35'
host3 = 'root@10.87.121.36'


#External routers if any
#for eg.
ext_routers = [('5b6-mx80-3', '10.87.65.253')]


router_asn = 64512       
public_vn_rtgt = 10003    
public_vn_subnet = '10.87.117.240/28'


#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.65.144'


#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3],
    'cfgm': [host1],
    'control': [host1],
    'compute': [host2, host3],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.kubernetes = {
'mode' : 'baremetal',
'master': host1,
'slaves': [host2, host3]
}

#Hostnames
# Deprecated 'all' key from release 3.0; Consider specifying the hostname for each host seperately as below
#env.hostnames = {
#    'all': ['a0s1', 'a0s2', 'a0s3','a0s4', 'a0s5', 'a0s6', 'a0s7', 'a0s8', 'a0s9', 'a0s10','backup_node']
#}
env.hostnames = {
    host1: '5b7s18',
    host2: '5b7s19',
    host3: '5b7s20',
}

#Openstack admin password
#env.openstack_admin_password = 'contrail123'

# Passwords of each host
# for passwordless login's no need to set env.passwords,
# instead populate env.key_filename in testbed.py with public key.
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

# SSH Public key file path for passwordless logins
# if env.passwords is not specified.
#env.key_filename = '/root/.ssh/id_rsa.pub'

#For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
}

env.orchestrator='kubernetes'


env.test = {
   'mail_to': 'chhandak@juniper.net',
   'mail_server': '10.84.24.64',
   'mail_port': '4000',
   'image_web_server': '10.84.5.120',
   'log_scenario': 'Kubernetes Sanity',
}

env.mail_from='chhandak@juniper.net'
env.mail_to='chhandak@juniper.net'
env.mail_server='10.84.24.64'
env.mail_port='4000'
env.mx_gw_test=True
env.testbed_location='US'
env.image_web_server = '10.84.5.120'
env.log_scenario='Kubernetes Sanity'
env.ntp_server = '10.84.5.100'


