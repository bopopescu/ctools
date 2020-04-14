from fabric.api import env

os_username = 'admin'
os_password = 'n1keenA'
os_tenant_name = 'demo'

host1 = 'root@10.87.140.127'
host2 = 'root@10.87.140.187'

ext_routers = [('montreal', '10.87.140.140')]
router_asn = 64510

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2],
    'cfgm': [host1],
    'openstack': [host1],
    'webui': [host1],
    'control': [host1 ],
    'compute': [host2],
    'collector': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
    'all': ['esbu-vse2100-8','cmbu-vxa2010-25']
}

control_data = {
   host1 : { 'ip': '5.0.0.1/24', 'gw' : '5.0.0.254', 'device':'eth5' },
   host2 : { 'ip': '5.0.0.2/24', 'gw' : '5.0.0.254', 'device':'eth1' },
}

env.passwords = {
    host1: 'n1keenA',
    host2: 'n1keenA',
    host_build: 'stack@123',
}

minimum_diskGB=32

#env.test_repo_dir='/home/stack/centos_multi_node_github_sanity/contrail-test'
env.mail_from="vageesant@juniper.net"
env.mail_to="vageesant@juniper.net"
multi_tenancy=True
env.interface_rename = True 
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario = 'Multi-Interface Sanity[mgmt, ctrl=data]'
