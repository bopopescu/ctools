from fabric.api import env
import os

host1 = 'root@10.204.216.64'
host2 = 'root@10.204.216.65'
host3 = 'root@10.204.217.76'
host4 = 'root@10.204.216.150'
host5 = 'root@10.204.217.114'
host6 = 'root@10.204.217.115'

ext_routers = [('umesh','7.7.7.78')]
router_asn = 64512
public_vn_rtgt = 2223
public_vn_subnet = '10.204.221.176/28'

host_build = 'stack@10.204.216.49'


env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6],
    'cfgm': [host1, host2, host3],
    'openstack': [host1, host2, host3],
    'webui': [host2],
    'control': [host1, host2, host3],
    'compute': [host4, host5, host6],
    'collector': [host1, host2, host3],
    'database': [host1, host2, host3],
    'build': [host_build],
    'toragent': [host5, host6],
    'tsn': [host5, host6],
}

env.hostnames = {
    'all': ['nodec7', 'nodec8', 'nodeg36', 'nodei1', 'nodei2', 'nodei3']
}

env.openstack_admin_password = 'contrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',

    host_build: 'stack@123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    host6:'ubuntu',
}

control_data = {
    host1 : { 'ip': '192.168.192.6/24', 'gw' : '192.168.192.254', 'device':'eth1' },
    host2 : { 'ip': '192.168.192.5/24', 'gw' : '192.168.192.254', 'device':'eth1' },
    host3 : { 'ip': '192.168.192.4/24', 'gw' : '192.168.192.254', 'device':'eth1' },
    host4 : { 'ip': '192.168.192.1/24', 'gw' : '192.168.192.254', 'device':'eth3' },
    host5 : { 'ip': '192.168.192.2/24', 'gw' : '192.168.192.254', 'device':'eth3' },
    host6 : { 'ip': '192.168.192.3/24', 'gw' : '192.168.192.254', 'device':'eth3' },
}

env.ha = {
    'internal_vip' : '192.168.192.251',
}
env.cluster_id='clusterc7c8g36i1i2i3'
minimum_diskGB=32
env.test_repo_dir='/home/stack/multi_interface_parallel/ubuntu/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename = True
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.log_scenario='Multi-Interface Sanity[mgmt, ctrl=data]'
env.enable_lbaas = True
do_parallel = True


env.tor_agent = {host5:[{
                    'tor_ip':'192.168.191.1',
                    'tor_id':'1',
                    'tor_type':'ovs',
                    'tor_ovs_port':'9998',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'192.168.192.2',
                    'tor_tsn_name':'nodei2',
                    'tor_name':'bng-contrail-qfx51-10',
                    'tor_tunnel_ip':'99.99.99.98',
                    'tor_vendor_name':'Juniper',
                    'tor_http_server_port': '9010',
                       },
{
                    'tor_ip':'192.168.191.2',
                    'tor_id':'2',
                    'tor_type':'ovs',
                    'tor_ovs_port':'9999',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'192.168.192.2',
                    'tor_tsn_name':'nodei2',
                    'tor_name':'bng-contrail-qfx51-15',
                    'tor_tunnel_ip':'99.99.99.97',
                    'tor_vendor_name':'Juniper',
                    'tor_http_server_port': '9011',
                       }],
host6:[{
                    'tor_ip':'192.168.191.1',
                    'tor_id':'1',
                    'tor_type':'ovs',
                    'tor_ovs_port':'9998',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'192.168.192.3',
                    'tor_tsn_name':'nodei3',
                    'tor_name':'bng-contrail-qfx51-10',
                    'tor_tunnel_ip':'99.99.99.98',
                    'tor_vendor_name':'Juniper',
                    'tor_http_server_port': '9010',
                       },
{
                    'tor_ip':'192.168.191.2',
                    'tor_id':'2',
                    'tor_type':'ovs',
                    'tor_ovs_port':'9999',
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'192.168.192.3',
                    'tor_tsn_name':'nodei3',
                    'tor_name':'bng-contrail-qfx51-15',
                    'tor_tunnel_ip':'99.99.99.97',
                    'tor_vendor_name':'Juniper',
                    'tor_http_server_port': '9011',
                       }],
 }

env.tor_hosts={
'10.204.217.213': [{ 'tor_port': 'ge-0/0/42',
                    'host_port' : 'em1',
                    'mgmt_ip' : '10.204.217.153',
                    'username' : 'root',
                    'password' : 'c0ntrail123',
                  }],
'10.204.217.199': [{ 'tor_port': 'ge-0/0/42',
                    'host_port' : 'em1',
                    'mgmt_ip' : '10.204.217.161',
                    'username' : 'root',
                    'password' : 'c0ntrail123',
                  }]
}

env.physical_routers={
'umesh'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'umesh',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '10.204.217.191',
                     'tunnel_ip' : '7.7.7.78',
                     'ports' : [],
                     'type'  : 'router',
             },
'bng-contrail-qfx51-10'       : {
                     'vendor': 'juniper',
                     'model' : 'qfx5100',
                     'asn'   : '64512',
                     'name'  : 'bng-contrail-qfx51-10',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.213',
                     'tunnel_ip' : '99.99.99.98',
                     'ports' : ['ge-0/0/42'],
                     'type'  : 'tor',
},
'bng-contrail-qfx51-15' : {
                     'vendor': 'juniper',
                     'model' : 'qfx5100',
                     'asn'   : '64512',
                     'name'  : 'bng-contrail-qfx51-15',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.199',
                     'tunnel_ip' : '99.99.99.97',
                     'ports' : ['ge-0/0/42'],
                     'type'  : 'tor',
}
}

static_route  = {
    host1 : [
             { 'ip': '192.168.191.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.78', 'netmask' : '255.255.255.255', 'gw':'192.168.192.252', 'intf': 'eth1' },
             { 'ip': '99.99.99.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth1' }],
    host2 : [
             { 'ip': '192.168.191.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.78', 'netmask' : '255.255.255.255', 'gw':'192.168.192.252', 'intf': 'eth1' },
             { 'ip': '99.99.99.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth1' }],
    host3 : [{ 'ip': '192.168.191.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth1' },
             { 'ip': '7.7.7.78', 'netmask' : '255.255.255.255', 'gw':'192.168.192.252', 'intf': 'eth1' },
             { 'ip': '192.168.191.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth1' }],
    host4 : [{ 'ip': '192.168.191.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth3' },
             { 'ip': '7.7.7.78', 'netmask' : '255.255.255.255', 'gw':'192.168.192.252', 'intf': 'eth3' },
            { 'ip': '192.168.191.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth3' }],
    host5 : [{ 'ip': '192.168.191.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth3' },
             { 'ip': '7.7.7.78', 'netmask' : '255.255.255.255', 'gw':'192.168.192.252', 'intf': 'eth3' },
             { 'ip': '192.168.191.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth3' }],
    host6 : [{ 'ip': '192.168.191.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth3' },
             { 'ip': '7.7.7.78', 'netmask' : '255.255.255.255', 'gw':'192.168.192.252', 'intf': 'eth3' },
            { 'ip': '192.168.191.0', 'netmask' : '255.255.255.0', 'gw':'192.168.192.254', 'intf': 'eth3' }]
}

ha_setup = True
env.ca_cert_file='/homes/vjoshi/github/mine/tor/contrail-test-verify-on-setup/tools/tor/cacert.pem'
env.test_repo_dir='/root/contrail-test'
