from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

host1 = 'root@10.204.217.118'
host2 = 'root@10.204.217.119'
host3 = 'root@10.204.217.120'
host4 = 'root@10.204.217.121'
host5 = 'root@10.204.217.122'
host6 = 'root@10.204.217.131'
host7 = 'root@10.204.217.123'
host8 = 'root@10.204.217.124'

ext_routers = [('walsh', '7.7.7.77')]
router_asn = 64512
public_vn_rtgt = 10003
public_vn_subnet = "10.204.219.72/28"
host_build = "root@10.204.217.118"

env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6, host7, host8],
    'cfgm': [host1, host2, host3],
    'openstack': [host1, host2, host3],
    'webui': [host2],
    'control': [host1, host3],
    'compute': [host4, host5, host6, host7, host8],
    'tsn': [host4, host5, host7, host8],
    'toragent': [host4, host5, host7, host8],
    'collector': [host1, host3],
    'database': [host1, host2, host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['nodei6', 'nodei7', 'nodei8', 'nodei9', 'nodei10', 'nodei19', 'nodei11', 'nodei12']
}

# OPTIONAL vrouter limit parameter
# ==================================
env.vrouter_module_params = {
     host4:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host5:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host6:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host7:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
     host8:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
}

#OPTIONAL BONDING CONFIGURATION
#==============================
#Inferface Bonding
bond= {
    host4 : { 'name': 'bond0', 'member': ['p6p1','p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host5 : { 'name': 'bond0', 'member': ['p6p1','p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host6 : { 'name': 'bond0', 'member': ['p6p1','p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
}

control_data= {

    host1 : { 'ip': '192.168.22.1/24', 'gw' : '192.168.22.254', 'device':'p6p2' },
    host2 : { 'ip': '192.168.22.2/24', 'gw' : '192.168.22.254', 'device':'p6p2' },
    host3 : { 'ip': '192.168.22.3/24', 'gw' : '192.168.22.254', 'device':'p6p2' },
    host4 : { 'ip': '192.168.22.4/24', 'gw' : '192.168.22.254', 'device':'bond0' },
    host5 : { 'ip': '192.168.22.5/24', 'gw' : '192.168.22.254', 'device':'bond0' },
    host6 : { 'ip': '192.168.22.6/24', 'gw' : '192.168.22.254', 'device':'bond0' },
    host7 : { 'ip': '192.168.22.7/24', 'gw' : '192.168.22.254', 'device':'p6p1' },
    host8 : { 'ip': '192.168.22.8/24', 'gw' : '192.168.22.254', 'device':'p6p1' },
}

static_route  = {
    host1 : [{ 'ip': '52.52.52.52', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '192.168.11.0', 'netmask' : '255.255.255.0', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' }],
    host2 : [{ 'ip': '52.52.52.52', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '192.168.11.0', 'netmask' : '255.255.255.0', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' }],
    host3 : [{ 'ip': '52.52.52.52', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '192.168.11.0', 'netmask' : '255.255.255.0', 'gw':'192.168.22.254', 'intf': 'p6p2' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p2' }],
    host4 : [{ 'ip': '52.52.52.52', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '192.168.11.0', 'netmask' : '255.255.255.0', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' }],
    host5 : [{ 'ip': '52.52.52.52', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '192.168.11.0', 'netmask' : '255.255.255.0', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' }],
    host6 : [{ 'ip': '52.52.52.52', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '192.168.11.0', 'netmask' : '255.255.255.0', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'bond0' }],
    host7 : [{ 'ip': '52.52.52.52', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p1' },
             { 'ip': '192.168.11.0', 'netmask' : '255.255.255.0', 'gw':'192.168.22.254', 'intf': 'p6p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p1' }],
    host8 : [{ 'ip': '52.52.52.52', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p1' },
             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p1' },
             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p1' },
             { 'ip': '192.168.11.0', 'netmask' : '255.255.255.0', 'gw':'192.168.22.254', 'intf': 'p6p1' },
             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p1' },
             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'192.168.22.254', 'intf': 'p6p1' }],
}

env.tor_agent = {host4:
                     [{
                      'tor_ip':'192.168.11.1',
                      'tor_id':'1',
                      'tor_type':'ovs',
                      'tor_ovs_port':'4321',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'bng-contrail-qfx51-2',
                      'tor_tunnel_ip':'34.34.34.34',
                      'tor_http_server_port': '5678',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'192.168.11.2',
                      'tor_id':'2',
                      'tor_type':'ovs',
                      'tor_ovs_port':'4323',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'bng-contrail-qfx51-3',
                      'tor_tunnel_ip':'33.33.33.33',
                      'tor_http_server_port': '5676',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.5',
                      'tor_id':'5',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1005',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-5',
                      'tor_tunnel_ip':'2.2.2.5',
                      'tor_http_server_port': '2005',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.6',
                      'tor_id':'6',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1006',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-6',
                      'tor_tunnel_ip':'2.2.2.6',
                      'tor_http_server_port': '2006',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.7',
                      'tor_id':'7',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1007',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-7',
                      'tor_tunnel_ip':'2.2.2.7',
                      'tor_http_server_port': '2007',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.8',
                      'tor_id':'8',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1008',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-8',
                      'tor_tunnel_ip':'2.2.2.8',
                      'tor_http_server_port': '2008',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.9',
                      'tor_id':'9',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1009',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-9',
                      'tor_tunnel_ip':'2.2.2.9',
                      'tor_http_server_port': '2009',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.10',
                      'tor_id':'10',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1010',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-10',
                      'tor_tunnel_ip':'2.2.2.10',
                      'tor_http_server_port': '2010',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.11',
                      'tor_id':'11',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1011',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-11',
                      'tor_tunnel_ip':'2.2.2.11',
                      'tor_http_server_port': '2011',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.12',
                      'tor_id':'12',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1012',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-12',
                      'tor_tunnel_ip':'2.2.2.12',
                      'tor_http_server_port': '2012',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.13',
                      'tor_id':'13',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1013',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-13',
                      'tor_tunnel_ip':'2.2.2.13',
                      'tor_http_server_port': '2013',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.14',
                      'tor_id':'14',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1014',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-14',
                      'tor_tunnel_ip':'2.2.2.14',
                      'tor_http_server_port': '2014',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.15',
                      'tor_id':'15',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1015',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-15',
                      'tor_tunnel_ip':'2.2.2.15',
                      'tor_http_server_port': '2015',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.16',
                      'tor_id':'16',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1016',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-16',
                      'tor_tunnel_ip':'2.2.2.16',
                      'tor_http_server_port': '2016',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.17',
                      'tor_id':'17',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1017',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-17',
                      'tor_tunnel_ip':'2.2.2.17',
                      'tor_http_server_port': '2017',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.18',
                      'tor_id':'18',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1018',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.4',
                      'tor_tsn_name':'nodei9',
                      'tor_name':'dummy-18',
                      'tor_tunnel_ip':'2.2.2.18',
                      'tor_http_server_port': '2018',
                      'tor_vendor_name':'Juniper'
                      },
                      ],
                 host5:
                     [{
                      'tor_ip':'192.168.11.1',
                      'tor_id':'1',
                      'tor_type':'ovs',
                      'tor_ovs_port':'4321',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'bng-contrail-qfx51-2',
                      'tor_tunnel_ip':'34.34.34.34',
                      'tor_http_server_port': '5678',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'192.168.11.2',
                      'tor_id':'2',
                      'tor_type':'ovs',
                      'tor_ovs_port':'4323',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'bng-contrail-qfx51-3',
                      'tor_tunnel_ip':'33.33.33.33',
                      'tor_http_server_port': '5676',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.5',
                      'tor_id':'5',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1005',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-5',
                      'tor_tunnel_ip':'2.2.2.5',
                      'tor_http_server_port': '2005',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.6',
                      'tor_id':'6',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1006',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-6',
                      'tor_tunnel_ip':'2.2.2.6',
                      'tor_http_server_port': '2006',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.7',
                      'tor_id':'7',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1007',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-7',
                      'tor_tunnel_ip':'2.2.2.7',
                      'tor_http_server_port': '2007',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.8',
                      'tor_id':'8',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1008',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-8',
                      'tor_tunnel_ip':'2.2.2.8',
                      'tor_http_server_port': '2008',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.9',
                      'tor_id':'9',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1009',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-9',
                      'tor_tunnel_ip':'2.2.2.9',
                      'tor_http_server_port': '2009',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.10',
                      'tor_id':'10',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1010',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-10',
                      'tor_tunnel_ip':'2.2.2.10',
                      'tor_http_server_port': '2010',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.11',
                      'tor_id':'11',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1011',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-11',
                      'tor_tunnel_ip':'2.2.2.11',
                      'tor_http_server_port': '2011',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.12',
                      'tor_id':'12',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1012',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-12',
                      'tor_tunnel_ip':'2.2.2.12',
                      'tor_http_server_port': '2012',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.13',
                      'tor_id':'13',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1013',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-13',
                      'tor_tunnel_ip':'2.2.2.13',
                      'tor_http_server_port': '2013',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.14',
                      'tor_id':'14',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1014',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-14',
                      'tor_tunnel_ip':'2.2.2.14',
                      'tor_http_server_port': '2014',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.15',
                      'tor_id':'15',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1015',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-15',
                      'tor_tunnel_ip':'2.2.2.15',
                      'tor_http_server_port': '2015',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.16',
                      'tor_id':'16',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1016',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-16',
                      'tor_tunnel_ip':'2.2.2.16',
                      'tor_http_server_port': '2016',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.17',
                      'tor_id':'17',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1017',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-17',
                      'tor_tunnel_ip':'2.2.2.17',
                      'tor_http_server_port': '2017',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.18',
                      'tor_id':'18',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1018',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.5',
                      'tor_tsn_name':'nodei10',
                      'tor_name':'dummy-18',
                      'tor_tunnel_ip':'2.2.2.18',
                      'tor_http_server_port': '2018',
                      'tor_vendor_name':'Juniper'
                      },
                      ],
                 host7:
                     [
                      {
                      'tor_ip':'192.168.11.3',
                      'tor_id':'3',
                      'tor_type':'ovs',
                      'tor_ovs_port':'4324',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'bng-contrail-qfx51-4',
                      'tor_tunnel_ip':'32.32.32.32',
                      'tor_http_server_port': '5675',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'192.168.11.4',
                      'tor_id':'4',
                      'tor_type':'ovs',
                      'tor_ovs_port':'4325',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'bng-contrail-qfx51-5',
                      'tor_tunnel_ip':'31.31.31.31',
                      'tor_http_server_port': '5674',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.19',
                      'tor_id':'19',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1019',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-19',
                      'tor_tunnel_ip':'2.2.2.19',
                      'tor_http_server_port': '2019',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.20',
                      'tor_id':'20',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1020',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-20',
                      'tor_tunnel_ip':'2.2.2.20',
                      'tor_http_server_port': '2020',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.21',
                      'tor_id':'21',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1021',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-21',
                      'tor_tunnel_ip':'2.2.2.21',
                      'tor_http_server_port': '2021',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.22',
                      'tor_id':'22',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1022',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-22',
                      'tor_tunnel_ip':'2.2.2.22',
                      'tor_http_server_port': '2022',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.23',
                      'tor_id':'23',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1023',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-23',
                      'tor_tunnel_ip':'2.2.2.23',
                      'tor_http_server_port': '2023',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.24',
                      'tor_id':'24',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1024',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-24',
                      'tor_tunnel_ip':'2.2.2.24',
                      'tor_http_server_port': '2024',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.25',
                      'tor_id':'25',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1025',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-25',
                      'tor_tunnel_ip':'2.2.2.25',
                      'tor_http_server_port': '2025',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.26',
                      'tor_id':'26',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1026',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-26',
                      'tor_tunnel_ip':'2.2.2.26',
                      'tor_http_server_port': '2026',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.27',
                      'tor_id':'27',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1027',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-27',
                      'tor_tunnel_ip':'2.2.2.27',
                      'tor_http_server_port': '2027',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.28',
                      'tor_id':'28',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1028',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-28',
                      'tor_tunnel_ip':'2.2.2.28',
                      'tor_http_server_port': '2028',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.29',
                      'tor_id':'29',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1029',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-29',
                      'tor_tunnel_ip':'2.2.2.29',
                      'tor_http_server_port': '2029',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.30',
                      'tor_id':'30',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1030',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-30',
                      'tor_tunnel_ip':'2.2.2.30',
                      'tor_http_server_port': '2030',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.31',
                      'tor_id':'31',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1031',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-31',
                      'tor_tunnel_ip':'2.2.2.31',
                      'tor_http_server_port': '2031',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.32',
                      'tor_id':'32',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1032',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.7',
                      'tor_tsn_name':'nodei11',
                      'tor_name':'dummy-32',
                      'tor_tunnel_ip':'2.2.2.32',
                      'tor_http_server_port': '2032',
                      'tor_vendor_name':'Juniper'
                      },
                      ],
                  host8:
                     [
                      {
                      'tor_ip':'192.168.11.3',
                      'tor_id':'3',
                      'tor_type':'ovs',
                      'tor_ovs_port':'4324',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'bng-contrail-qfx51-4',
                      'tor_tunnel_ip':'32.32.32.32',
                      'tor_http_server_port': '5675',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'192.168.11.4',
                      'tor_id':'4',
                      'tor_type':'ovs',
                      'tor_ovs_port':'4325',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'bng-contrail-qfx51-5',
                      'tor_tunnel_ip':'31.31.31.31',
                      'tor_http_server_port': '5674',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.19',
                      'tor_id':'19',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1019',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-19',
                      'tor_tunnel_ip':'2.2.2.19',
                      'tor_http_server_port': '2019',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.20',
                      'tor_id':'20',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1020',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-20',
                      'tor_tunnel_ip':'2.2.2.20',
                      'tor_http_server_port': '2020',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.21',
                      'tor_id':'21',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1021',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-21',
                      'tor_tunnel_ip':'2.2.2.21',
                      'tor_http_server_port': '2021',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.22',
                      'tor_id':'22',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1022',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-22',
                      'tor_tunnel_ip':'2.2.2.22',
                      'tor_http_server_port': '2022',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.23',
                      'tor_id':'23',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1023',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-23',
                      'tor_tunnel_ip':'2.2.2.23',
                      'tor_http_server_port': '2023',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.24',
                      'tor_id':'24',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1024',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-24',
                      'tor_tunnel_ip':'2.2.2.24',
                      'tor_http_server_port': '2024',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.25',
                      'tor_id':'25',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1025',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-25',
                      'tor_tunnel_ip':'2.2.2.25',
                      'tor_http_server_port': '2025',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.26',
                      'tor_id':'26',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1026',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-26',
                      'tor_tunnel_ip':'2.2.2.26',
                      'tor_http_server_port': '2026',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.27',
                      'tor_id':'27',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1027',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-27',
                      'tor_tunnel_ip':'2.2.2.27',
                      'tor_http_server_port': '2027',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.28',
                      'tor_id':'28',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1028',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-28',
                      'tor_tunnel_ip':'2.2.2.28',
                      'tor_http_server_port': '2028',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.29',
                      'tor_id':'29',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1029',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-29',
                      'tor_tunnel_ip':'2.2.2.29',
                      'tor_http_server_port': '2029',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.30',
                      'tor_id':'30',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1030',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-30',
                      'tor_tunnel_ip':'2.2.2.30',
                      'tor_http_server_port': '2030',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.31',
                      'tor_id':'31',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1031',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-31',
                      'tor_tunnel_ip':'2.2.2.31',
                      'tor_http_server_port': '2031',
                      'tor_vendor_name':'Juniper'
                      },
                      {
                      'tor_ip':'1.1.1.32',
                      'tor_id':'32',
                      'tor_type':'ovs',
                      'tor_ovs_port':'1032',
                      'tor_ovs_protocol':'pssl',
                      'tor_tsn_ip':'192.168.22.8',
                      'tor_tsn_name':'nodei12',
                      'tor_name':'dummy-32',
                      'tor_tunnel_ip':'2.2.2.32',
                      'tor_http_server_port': '2032',
                      'tor_vendor_name':'Juniper'
                      },
                      ],
                }

env.ca_cert_file= '/root/cacert.pem'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
    host7: 'c0ntrail123',
    host8: 'c0ntrail123',

    host_build: 'c0ntrail123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    host6:'ubuntu',
    host7:'ubuntu',
    host8:'ubuntu',
}

# VIP
env.ha = {
    'internal_vip' : '192.168.22.210',
    'external_vip' : '10.204.217.210'
}

env.mail_from='chhandak@juniper.net'
env.mail_to='chhandak@juniper.net'
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.test_repo_dir='/root/contrail-test'
