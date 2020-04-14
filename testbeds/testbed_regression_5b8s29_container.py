from fabric.api import env
import os


#Management ip addresses of hosts in the cluster
host1 ='root@10.87.66.144'
host2 ='root@10.87.66.145'
host3 ='root@10.87.66.146'
#host4 ='root@10.87.66.147'
host4 ='root@10.87.66.148'
host5 ='root@10.87.66.150'
host6 ='root@10.87.66.151'


#External routers if any
#for eg.
##ext_routers = [('5b8-mx-80-3', '7.7.7.77'), ('5b8-mx-80-4', '7.7.7.78')]
#ext_routers = []
ext_routers = [('5b8-mx80-3','172.17.90.243'), ('5b8-mx80-4','172.17.90.244')]                                                                                                                                                             

#Autonomous system number
router_asn = 64513
public_vn_rtgt = 5289
public_vn_subnet = '10.87.120.96/27'

#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.66.144'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1,host2,host3,host4,host5,host6],
    'webui': [host1],
    'openstack': [host1,host2,host3],
    'cfgm': [host1,host2,host3],
    'control': [host1,host2,host3],
    'collector': [host1,host2,host3],
    'database': [host1,host2,host3],
    'compute': [host4, host5, host6],
    'build': [host_build],
}

env.hostnames = {
    'all': ['5b8s29','5b8s30','5b8s31','5b8s32','5b8s33','5b8s35','5b8s36']
}
#Openstack admin password
env.openstack_admin_password = 'contrail123'

# Passwords of each host
# for passwordless login's no need to set env.passwords,
# instead populate env.key_filename in testbed.py with public key.
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

reimage_param = os.getenv('REIMAGE_PARAM', 'ubuntu-14.04.5')


# SSH Public key file path for passwordless logins
# if env.passwords is not specified.  
#env.key_filename = '/root/.ssh/id_rsa.pub'

#For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
    host6: 'ubuntu',
}
minimum_diskGB = 64

control_data = {
    host1 : { 'ip': '172.17.90.1/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host2 : { 'ip': '172.17.90.2/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host3 : { 'ip': '172.17.90.3/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host4 : { 'ip': '172.17.90.5/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host5 : { 'ip': '172.17.90.6/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host6 : { 'ip': '172.17.90.7/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
}

env.physical_routers={
'5b8-mx80-3'          : {
                     'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64513',
                     'name'  : '5b8-mx80-3',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'   : '10.87.66.243',
                     'tunnel_ip' : '3.3.3.3',
                     'ports' : [],
                     'type'  : 'router',
                 },
'5b8-mx80-4'          : {
                     'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64513',
                     'name'  : '5b8-mx80-4',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'   : '10.87.66.244',
                     'tunnel_ip' : '4.4.4.4',
                     'ports' : [],
                     'type'  : 'router',
},
'5b8-qfx3'       : {
                     'vendor': 'juniper',
                     'model' : 'qfx5100',
                     'asn'   : '64513',
                     'name'  : '5b8-qfx3',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '10.87.66.248',
                     'tunnel_ip' : '173.173.173.173',
                     'ports' : ['xe-0/0/48:3'],
                     'type'  : 'tor',
},
'5b8-qfx5'       : {
                     'vendor': 'juniper',
                     'model' : 'qfx5100',
                     'asn'   : '64513',
                     'name'  : '5b8-qfx5',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '10.87.66.250',
                     'tunnel_ip' : '185.185.185.185',
                     'ports' : ['xe-0/0/2'],
                     'type'  : 'tor',
},
}

# VIP
env.ha = {
    'external_vip' : '10.87.66.186',
    'internal_vip' : '172.17.90.186',
    'contrail_external_vip' : '10.87.66.186',
    'contrail_internal_vip' : '172.17.90.186',
}
env.openstack = {
    'amqp_host' : '172.17.90.186',
    'manage_amqp' : 'yes',
}
do_parallel = True
#env.mail_from='chhandak@juniper.net'
#env.mail_to='chhandak@juniper.net'
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.enable_lbaas = True
env.test_repo_dir='/root/contrail-test'
env.ca_cert_file='/root/cacert.pem'
env.mx_gw_test=True
env.image_web_server = '10.84.5.120'
env.ntp_server='66.129.255.62'
