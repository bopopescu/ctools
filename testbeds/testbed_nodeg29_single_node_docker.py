from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

host1 = 'root@10.204.217.69'

ext_routers = []
#ext_routers = [('blr-mx2', '10.204.216.245')]
router_asn = 64512
public_vn_rtgt = 19005
public_vn_subnet = "10.204.219.96/29"

host_build = 'kalok@10.204.216.3'

env.roledefs = {
    'all': [host1],
    'cfgm': [host1],
    'control': [host1],
    'compute': [host1],
    'collector': [host1],
    'openstack': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
     'all': ['nodeg29']
}

env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'secret',
}
env.ostypes = { 
    host1: 'ubuntu',
    }

# OPTIONAL COMPUTE HYPERVISOR CHOICE:
#======================================
# Compute Hypervisor
env.hypervisor = {
    host1: 'docker'
}
#  Specify the hypervisor to be provisioned in the compute node.(Default=libvirt)

#To disable installing contrail interface rename package
env.interface_rename = True
minimum_diskGB=32
#To enable multi-tenancy feature
multi_tenancy = True


env.test_repo_dir='/homes/ganeshahv/git-hub/contrail-test'
#env.test_repo_dir='/homes/ganeshahv/commit_queue/Feb-02/contrail-test'
#env.mail_from='ganeshahv@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
env.log_scenario='Docker Single-Node Sanity'
#To enable haproxy feature
#haproxy = True

