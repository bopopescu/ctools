from fabric.api import env                                           

#Management ip addresses of hosts in the cluster
host1 = 'root@172.16.70.2'                      
host2 = 'root@172.16.70.3'                      
host3 = 'root@172.16.70.4'                      
host4 = 'root@172.16.70.7'                      
host5 = 'root@172.16.70.8'                      
host6 = 'root@172.16.70.9'                      
host7 = 'root@172.16.70.10'                     
host8 = 'root@172.16.70.11'                     
host9 = 'root@172.16.70.12'                     

#External routers if any
#ext_routers = [('montreal', '10.87.140.185')]
ext_routers = [('sydney', '172.16.80.100'), ('tasman', '172.16.80.200')]

#Autonomous system number
router_asn = 64512       

#Host from which the fab commands are triggered to install and provision
host_build = 'root@172.16.70.2'                                         

#Role definition of the hosts.
env.roledefs = {              
    'all': [host1, host2, host3,host4,host5,host6,host7,host8,host9],
    'cfgm': [host1,host2,host3],                                     
    'openstack': [host1,host2,host3],                                            
    'control': [host1,host2,host3],                                  
    'compute': [host4, host5,host6,host7,host8,host9],               
    'collector': [host1,host2,host3],                                
    'webui': [host1,host2,host3],                                                
    'database': [host1,host2,host3],                                 
    'build': [host_build],                                           
}                                                                    

env.hostnames = {
    'all': ['csol1-node2','csol1-node3','csol1-node4','csol1-node7','csol1-node8','csol1-node9','csol1-node10','csol1-node11','csol1-node12']
}                                                                                                                                            

#Openstack admin password
env.openstack_admin_password = 'c0ntrail123'

env.password = 'c0ntrail123'
#Passwords of each host     
env.passwords = {           
    host1: 'c0ntrail123',   
    host2: 'c0ntrail123',   
    host3: 'c0ntrail123',   
    host4: 'c0ntrail123',   
    host5: 'c0ntrail123',   
    host6: 'c0ntrail123',   
    host7: 'c0ntrail123',   
    host8: 'c0ntrail123',   
    host9: 'c0ntrail123',   
    host_build: 'c0ntrail123',
}                             

#For reimage purpose
env.ostypes = {     
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
    host6: 'ubuntu',
    host7: 'ubuntu',
    host8: 'ubuntu',
    host9: 'ubuntu',
}                   

#OPTIONAL BONDING CONFIGURATION
#==============================
#Inferface Bonding             
#OPTIONAL BONDING CONFIGURATION
#==============================
#Inferface Bonding             
bond= {                        
    host1 : { 'name': 'bond0', 'member': ['eth2','eth3'], 'mode':'802.3ad' }, 
	host2 : { 'name': 'bond0', 'member': ['eth2','eth3'], 'mode':'802.3ad' }, 
	host3 : { 'name': 'bond0', 'member': ['eth2','eth3'], 'mode':'802.3ad' }, 
	host4 : { 'name': 'bond0', 'member': ['eth2','eth3'], 'mode':'802.3ad' }, 
	host5 : { 'name': 'bond0', 'member': ['eth2','eth3'], 'mode':'802.3ad' }, 
	host6 : { 'name': 'bond0', 'member': ['eth2','eth3'], 'mode':'802.3ad' }, 
	host7 : { 'name': 'bond0', 'member': ['eth2','eth3'], 'mode':'802.3ad' }, 
	host8 : { 'name': 'bond0', 'member': ['eth2','eth3'], 'mode':'802.3ad' }, 
	host9 : { 'name': 'bond0', 'member': ['eth2','eth3'], 'mode':'802.3ad' }, 
	}
#OPTIONAL SEPARATION OF MANAGEMENT AND CONTROL + DATA
#====================================================
#Control Interface                                   
#control = {                                         
#    host1 : { 'ip': '10.87.140.197/22', 'gw' : '10.87.159.254', 'device':'eth0' },
#    host2 : { 'ip': '10.87.140.198/22', 'gw' : '10.87.159.254', 'device':'eth0' },
#    host3 : { 'ip': '10.87.140.199/22', 'gw' : '10.87.159.254', 'device':'eth0' },
#}                                                                                 

#Data Interface
control_data = {
   host1 : { 'ip': '172.16.80.2/24',  'gw' : '172.16.80.253', 'device':'bond0' },
   host2 : { 'ip': '172.16.80.3/24',  'gw' : '172.16.80.253', 'device':'bond0' },
   host3 : { 'ip': '172.16.80.4/24',  'gw' : '172.16.80.253', 'device':'bond0' },
   host4 : { 'ip': '172.16.80.7/24',  'gw' : '172.16.80.253', 'device':'bond0' },
   host5 : { 'ip': '172.16.80.8/24',  'gw' : '172.16.80.253', 'device':'bond0' },
   host6 : { 'ip': '172.16.80.9/24',  'gw' : '172.16.80.253', 'device':'bond0' },
   host7 : { 'ip': '172.16.80.10/24', 'gw' : '172.16.80.253', 'device':'bond0' },
   host8 : { 'ip': '172.16.80.11/24', 'gw' : '172.16.80.253', 'device':'bond0' },
   host9 : { 'ip': '172.16.80.12/24', 'gw' : '172.16.80.253', 'device':'bond0' },
}

#To disable installing contrail interface rename package
env.interface_rename = False

#To use existing service_token
#service_token = 'your_token'

#Specify keystone IP
#keystone_ip = '172.16.70.2'

#Specify Keystone admin user if not same as  admin
#keystone_admin_user = 'nonadmin'

#Specify Keystone admin password if not same as env.openstack_admin_password
#keystone_admin_password = 'contrail123'

#Specify Region Name
#region_name = 'RegionName'

#To enable multi-tenancy feature
#multi_tenancy = True

#To enable haproxy feature
#haproxy = True

#To Enable prallel execution of task in multiple nodes
#do_parallel = True

# To configure the encapsulation priority. Default: MPLSoGRE
#env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"

#Ceph related

# HA Config

env.ha = {
    'internal_vip' : '172.16.80.25',
    'external_vip' : '172.16.70.25',

}
