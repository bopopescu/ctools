from fabric.api import env                                                           
import os                                                                            


#Management ip addresses of hosts in the cluster
host1 ='root@10.87.66.157'                      
host2 ='root@10.87.66.158'                      
host3 ='root@10.87.66.159'                      
host4 ='root@10.87.66.160'                      
host5 ='root@10.87.66.161'                      
host6 ='root@10.87.66.162'                      
host7 ='root@10.87.66.163'                      
host8 ='root@10.87.66.164'                      
host9 ='root@10.87.66.165'                      
host10 ='root@10.87.66.166'                     
host11 ='root@10.87.66.167'                     
host12 ='root@10.87.66.168'                     
host13 ='root@10.87.66.147'                     
host14 ='root@10.87.66.148'
host15 ='root@10.87.66.150'                            
host17 ='root@10.87.66.152'                     
#host18 ='root@10.87.66.153'                    
host19 ='root@10.87.66.154'                     
host20 ='root@10.87.66.169'  

kvm_host1 = 'root@10.87.66.144'
kvm_host2 = 'root@10.87.66.145'
kvm_host3 = 'root@10.87.66.146'

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
host_build = 'root@10.87.66.157'                                        

#Role definition of the hosts.
env.roledefs = {              
    'all': [host1,host2,host3,host4,host13, host14,host17, host19],
    'webui': [host2,host2,host3],                                                                                                                     
    'openstack': [host1],                                                                                                     
    'cfgm': [host2,host3,host4],                                                                                                         
    'control': [host2,host3,host4],                                                                                                      
    'collector': [host2,host3,host4],                                                                                                    
    'database': [host2,host3,host4],                                                                                                     
    'compute': [host13, host14,host17, host19],                                                                          
    #'vgw': [host13],                                                                                                                      
    'tsn': [host17, host19],                                                                                                              
    'toragent': [host17, host19],                                                                                                         
    'build': [host_build],                                                                                                                
}                                                                                                                                         

env.hostnames = {
    'all': ['5b8s29-vm1','5b8s29-vm2','5b8s29-vm3','5b8s29-vm4', '5b8s32','5b8s33','5b8s35','5b8s36','5b8s37','5b8s38','5b8s39']                                                                                                                                                                                                                      
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
    host7: 'c0ntrail123',                                         
    host8: 'c0ntrail123',                                         
    host9: 'c0ntrail123',                                         
    host10: 'c0ntrail123',                                        
    host11: 'c0ntrail123',                                        
    host12: 'c0ntrail123',                                        
    host13: 'c0ntrail123',                                        
    host14: 'c0ntrail123',                                        
    host15: 'c0ntrail123',                                        
    host16: 'c0ntrail123',                                        
    host17: 'c0ntrail123',                                        
#    host18: 'c0ntrail123',                                       
    host19: 'c0ntrail123',
    host20: 'c0ntrail123',  	
    host_build: 'c0ntrail123',                                    
}                                                                 

reimage_param = os.getenv('REIMAGE_PARAM', 'ubuntu-14.04.2')

vm_node_details = {
    'default': {   
                'image_dest' : '/mnt/disk1/images/',
                'ram' : '65536',                    
                'vcpus' : '32',                     
                'disk_format' : 'qcow2',            
                'image_source' : 'http://10.84.5.120/cs-shared/images/node_vm_images/%s-256G.img.gz' % (reimage_param),
                },                                                                                                     
    host1 : {                                                                                                          
                'name' : '5b8s29-vm1',                                                                                 
                'server': kvm_host1,                                                                                   
                'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:02'},                                            
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:02'}                                             
                            ],                                                                                         
            },                                                                                                         
    host2 : {                                                                                                          
                'name' : '5b8s29-vm2',                                                                                 
                'server': kvm_host1,                                                                                   
                'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:03'},                                            
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:03'}                                             
                            ],                                                                                         
            },                                                                                                         
    host3 : {                                                                                                          
                'name' : '5b8s29-vm3',                                                                                 
                'server': kvm_host1,                                                                                   
                'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:04'},                                            
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:04'}                                             
                            ],                                                                                         
            },                                                                                                         
    host4 : {                                                                                                          
                'name' : '5b8s29-vm4',                                                                                 
                'server': kvm_host1,                                                                                   
                'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:05'},                                            
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:05'}                                             
                            ],                                                                                         
            },                                                                                                         
    host5 : {   'name' : '5b8s30-vm1',                                                                                 
                'server': kvm_host2,                                                                                   
                'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:06'},                                            
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:06'}                                             
                            ]                                                                                          
            },                                                                                                         
    host6 : {   'name' : '5b8s30-vm2',                                                                                 
                'server': kvm_host2,                                                                                   
                'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:07'},                                            
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:07'}                                             
                            ]                                                                                          
            },                                                                                                         
    host7 : {   'name' : '5b8s30-vm3',                                                                                 
                'server': kvm_host2,                                                                                   
                'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:08'},                                            
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:08'}                                             
                            ]                                                                                          
            },                                                                                                         
    host8 : {   'name' : '5b8s30-vm4',                                                                                 
                'server': kvm_host2,                                                                                   
                'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:09'},                                            
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:09'}                                             
                            ]                                                                                          
            },                                                                                                         
    host9 : {   'name' : '5b8s31-vm1',                                                                                 
                'server': kvm_host3,                                                                                   
                'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:0A'},                                            
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:0A'}                                             
                            ]                                                                                          
            },                                                                                                         
    host10 : {   'name' : '5b8s31-vm2',                                                                                
                 'server': kvm_host3,                                                                                  
                 'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:0B'},                                           
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:0B'}                                             
                             ]                                                                                         
            },                                                                                                         
    host11 : {   'name' : '5b8s31-vm3',                                                                                
                 'server': kvm_host3,                                                                                  
                 'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:0C'},                                           
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:0C'}                                             
                            ]                                                                                          
            },                                                                                                         
    host12 : {   'name' : '5b8s31-vm4',                                                                                
                 'server': kvm_host3,                                                                                  
                 'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:0D'},                                           
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:0D'}                                             
                            ]                                                                                          
            },
	host20 : {   'name' : '5b8s29-vm5',                                                                                
                 'server': kvm_host1,                                                                                  
                 'network' : [{'bridge' : 'br0', 'mac':'52:53:55:01:00:0E'},                                           
                             {'bridge' : 'br1', 'mac':'52:53:55:02:00:0E'}                                             
                            ]                                                                                          
            }               			
}                                                                                                                      

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
    host7: 'ubuntu',
    host8: 'ubuntu',
    host9: 'ubuntu',
    host10: 'ubuntu',
    host11: 'ubuntu',
    host12: 'ubuntu',
    host13: 'ubuntu',
    host14: 'ubuntu',
    host15: 'ubuntu',
    host16: 'ubuntu',
    host17: 'ubuntu',
#    host18: 'ubuntu',
    host19: 'ubuntu',
	host20: 'ubuntu', 
}                     
#env.orchestrator = 'openstack' #other values are 'vcenter', 'none' default:openstack

#ntp server the servers should point to
#env.ntp_server = 'ntp.juniper.net'    

# OPTIONAL COMPUTE HYPERVISOR CHOICE:
#======================================
# Compute Hypervisor                   
#env.hypervisor = {                    
#    host5: 'docker',                  
#    host6: 'libvirt',                 
#    host10: 'docker',                 
#}                                     
#  Specify the hypervisor to be provisioned in the compute node.(Default=libvirt)

# INFORMATION FOR DB BACKUP/RESTORE ..
#=======================================================
#Optional,Backup Host configuration if it is not available then it will put in localhost
#backup_node = 'root@2.2.2.2'                                                           

# Optional, Local/Remote location of backup_data path
# if it is not passed then it will use default path  
#backup_db_path= ['/home/','/root/']G                
#cassandra backup can be defined either "full" or "custom"
#full -> take complete snapshot of cassandra DB           
#custom -> take snapshot except defined in skip_keyspace  
#cassandra_backup='custom'  [ MUST OPTION]                
#skip_keyspace=["ContrailAnalytics"]  IF cassandra_backup is selected as custom
#service token need to define to do  restore of backup data                    
#service_token = '53468cf7552bbdc3b94f'                                        


#OPTIONAL ANALYTICS CONFIGURATION
#================================
# database_dir is the directory where cassandra data is stored
#                                                             
# If it is not passed, we will use cassandra's default        
# /var/lib/cassandra/data                                     
#                                                             
#database_dir = '<separate-partition>/cassandra'              
#                                                             
# analytics_data_dir is the directory where cassandra data for analytics
# is stored. This is used to seperate cassandra's main data storage [internal
# use and config data] with analytics data. That way critical cassandra's    
# system data and config data are not overrun by analytis data               
#                                                                            
# If it is not passed, we will use cassandra's default                       
# /var/lib/cassandra/data                                                    
#                                                                            
#analytics_data_dir = '<separate-partition>/analytics_data'                  
#                                                                            
# ssd_data_dir is the directory where cassandra can store fast retrievable   
# temporary files (commit_logs). Giving cassandra an ssd disk for this       
# purpose improves cassandra performance                                     
#                                                                            
# If it is not passed, we will use cassandra's default                       
# /var/lib/cassandra/commit_logs                                             
#                                                                            
#ssd_data_dir = '<seperate-partition>/commit_logs_data'                      

#following variables allow analytics data to have different TTL in cassandra database
#analytics_config_audit_ttl controls TTL for config audit logs                       
#analytics_statistics_ttl controls TTL for stats/control_data                        
#following parameter allows to specify minimum amount of disk space in the analytics 
#database partition, if configured amount of space is not present, it will fail provisioning
minimum_diskGB = 64                                                                         

#OPTIONAL BONDING CONFIGURATION
#==============================
#Inferface Bonding             
##bond= {                      
##    b7s31 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
##    b7s32 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
##    b7s33 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
##    b7s34 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
##    b7s35 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
##    b7s36 : { 'name': 'bond0', 'member': ['p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },        
##    b7s37 : { 'name': 'bond0', 'member': ['p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },        
##}                                                                                                              
##                                                                                                               
##env.sriov = {                                                                                                  
##     host9 :[ {'interface' : 'p514p2', 'VF' : 25, 'physnets' : ['physnet1']}],                                 
##     host10 :[ {'interface' : 'p514p2', 'VF' : 25, 'physnets' : ['physnet1']}],                                
##}                                                                                                              
##                                                                                                               
###OPTIONAL SEPARATION OF MANAGEMENT AND CONTROL + DATA and OPTIONAL VLAN INFORMATION                            
###==================================================================================                            
control_data = {                                                                                                 
    host1 : { 'ip': '172.17.90.1/24', 'gw' : '172.17.90.254', 'device':'eth1' },                                 
    host2 : { 'ip': '172.17.90.2/24', 'gw' : '172.17.90.254', 'device':'eth1' },                                 
    host3 : { 'ip': '172.17.90.3/24', 'gw' : '172.17.90.254', 'device':'eth1' },                                 
    host4 : { 'ip': '172.17.90.4/24', 'gw' : '172.17.90.254', 'device':'eth1' },                                 
    #host5 : { 'ip': '172.17.90.5/24', 'gw' : '172.17.90.254', 'device':'eth1' },                                 
    #host6 : { 'ip': '172.17.90.6/24', 'gw' : '172.17.90.254', 'device':'eth1' },                                 
    #host7 : { 'ip': '172.17.90.7/24', 'gw' : '172.17.90.254', 'device':'eth1' },                                 
    #host8 : { 'ip': '172.17.90.8/24', 'gw' : '172.17.90.254', 'device':'eth1' },                                 
    #host9 : { 'ip': '172.17.90.9/24', 'gw' : '172.17.90.254', 'device':'eth1' },                                 
    #host10 : { 'ip': '172.17.90.10/24', 'gw' : '172.17.90.254', 'device':'eth1' },                               
    #host11 : { 'ip': '172.17.90.11/24', 'gw' : '172.17.90.254', 'device':'eth1' },                               
    #host12 : { 'ip': '172.17.90.12/24', 'gw' : '172.17.90.254', 'device':'eth1' },                               
    host13 : { 'ip': '172.17.90.13/24', 'gw' : '172.17.90.254', 'device':'p514p1' },                             
    host14 : { 'ip': '172.17.90.14/24', 'gw' : '172.17.90.254', 'device':'p514p1' },                             
    #host15 : { 'ip': '172.17.90.15/24', 'gw' : '172.17.90.254', 'device':'p514p1' },                             
    #host16 : { 'ip': '172.17.90.16/24', 'gw' : '172.17.90.254', 'device':'p514p1' },                             
    host17 : { 'ip': '172.17.90.17/24', 'gw' : '172.17.90.254', 'device':'p514p1' },                             
    host19 : { 'ip': '172.17.90.19/24', 'gw' : '172.17.90.254', 'device':'p514p1' },
    host20 : { 'ip': '172.17.90.20/24', 'gw' : '172.17.90.254', 'device':'eth1' },	
}                                                                                                                
###OPTIONAL STATIC ROUTE CONFIGURATION                                                                           
###===================================                                                                           
static_route  = {                                                                                                
    host17 : [{ 'ip': '173.173.173.173', 'netmask' : '255.255.255.255', 'gw':'172.17.90.249', 'intf': 'p514p1' },
             { 'ip': '185.185.185.185', 'netmask' : '255.255.255.255', 'gw':'172.17.90.249', 'intf': 'p514p1' }],
    host19 : [{ 'ip': '173.173.173.173', 'netmask' : '255.255.255.255', 'gw':'172.17.90.249', 'intf': 'p514p1' },
             { 'ip': '185.185.185.185', 'netmask' : '255.255.255.255', 'gw':'172.17.90.249', 'intf': 'p514p1' }],
}                                                                                                                
###OPTIONAL STATIC ROUTE CONFIGURATION                                                                           
###===================================                                                                           
##static_route  = {                                                                                              
##    host1 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },     
##             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
##             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],  
##    host2 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },     
##             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
##             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],  
##    host3 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },     
##             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
##             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },   
##             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],  
##    host4 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'vhost0' },     
##             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' }],  
##    host5 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'vhost0' },     
##             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' }],  
##    host6 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'vhost0' },     
##             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' }],  
##    host7 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'vhost0' },     
##             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' }],  
##    host8 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'vhost0' },     
##             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' }],  
##    host9 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'vhost0' },     
##             { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },      
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' }],  
##    host10 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'vhost0' },    
##             { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' },   
##             { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'vhost0' }],  
                                                                                                                 
    #host4 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
    #         { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],   
    #host5 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
    #         { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],   
    #host6 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
    #         { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],   
    #host7 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
    #         { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],   
    #host8 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
    #         { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],   
    #host9 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },      
    #         { 'ip': '7.7.7.77', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '8.8.8.88', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },       
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],   
    #host10 : [{ 'ip': '172.18.90.0', 'netmask' : '255.255.255.0', 'gw':'172.17.90.254', 'intf': 'p514p1' },     
    #         { 'ip': '34.34.34.34', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '33.33.33.33', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '32.32.32.32', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' },    
    #         { 'ip': '31.31.31.31', 'netmask' : '255.255.255.255', 'gw':'172.17.90.254', 'intf': 'p514p1' }],   
#}                                                                                                               

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
    #'external_vip' : '10.87.66.185',
    #'internal_vip' : '172.17.90.185',
    'contrail_external_vip' : '10.87.66.186',
    'contrail_internal_vip' : '172.17.90.186',
	'contrail_internal_virtual_router_id' :  240, #Default = 100                                                           
    'contrail_external_virtual_router_id' :  241, #Default = 100
}                                             
env.openstack = {                             
    'amqp_host' : '172.17.90.1',            
    'manage_amqp' : 'yes',                    
}                                             
##                                            
### OPTIONAL vrouter limit parameter          
### ==================================        
##env.vrouter_module_params = {               
##     host4:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
##     host5:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
##     host6:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
##     host8:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
##     host9:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
##     host10:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},
##}                                                                                           
##                                                                                            
# OPTIONAL vrouter limit parameter                                                            
# ==================================                                                          
env.vrouter_module_params = {                                                                 
     host13:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},  
     host14:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},  
     host15:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},  
     host16:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},  
     host17:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},  
     host19:{'mpls_labels':'200000', 'nexthops':'512000', 'vrfs':'65536', 'macs':'1000000'},  
}                                                                                             

env.tor_agent = {host17:[{
                    'tor_ip':'172.17.90.248',
                    'tor_agent_id':'1',      
                    'tor_type':'ovs',        
                    'tor_ovs_port':'4321',   
                    'tor_ovs_protocol':'pssl',
                    'tor_tsn_ip':'172.17.90.17',
                    'tor_tsn_name':'5b8s37',    
                    'tor_name':'5b8-qfx3',      
                    'tor_tunnel_ip':'173.173.173.173',
                    'tor_vendor_name':'Juniper',      
                    'tor_product_name':'QFX5100',     
                    'tor_agent_http_server_port': '1233',
                    'tor_agent_ovs_ka': '10000',         
                       },                                
                       {                                 
                    'tor_ip':'172.17.90.250',            
                    'tor_agent_id':'2',                  
                    'tor_type':'ovs',                    
                    'tor_ovs_port':'4322',               
                    'tor_ovs_protocol':'pssl',           
                    'tor_tsn_ip':'172.17.90.17',         
                    'tor_tsn_name':'5b8s37',             
                    'tor_name':'5b8-qfx5',               
                    'tor_tunnel_ip':'185.185.185.185',   
                    'tor_vendor_name':'Juniper',         
                    'tor_product_name':'QFX5100',        
                    'tor_agent_http_server_port': '1234',
                    'tor_agent_ovs_ka': '10000',         
                       },                                
                       ],                                
                                                         
                 host19:[{                               
                    'tor_ip':'172.17.90.248',            
                    'tor_agent_id':'1',                  
                    'tor_type':'ovs',                    
                    'tor_ovs_port':'4321',               
                    'tor_ovs_protocol':'pssl',           
                    'tor_tsn_ip':'172.17.90.19',         
                    'tor_tsn_name':'5b8s39',             
                    'tor_name':'5b8-qfx3',               
                    'tor_tunnel_ip':'173.173.173.173',   
                    'tor_vendor_name':'Juniper',         
                    'tor_product_name':'QFX5100',        
                    'tor_agent_http_server_port': '1233',
                    'tor_agent_ovs_ka': '10000',         
                       },                                
                       {                                 
                    'tor_ip':'172.17.90.250',            
                    'tor_agent_id':'2',                  
                    'tor_type':'ovs',                    
                    'tor_ovs_port':'4322',               
                    'tor_ovs_protocol':'pssl',           
                    'tor_tsn_ip':'172.17.90.19',         
                    'tor_tsn_name':'5b8s39',             
                    'tor_name':'5b8-qfx5',               
                    'tor_tunnel_ip':'185.185.185.185',   
                    'tor_vendor_name':'Juniper',         
                    'tor_product_name':'QFX5100',        
                    'tor_agent_http_server_port': '1234',
                    'tor_agent_ovs_ka': '10000',         
                       },                                
                       ]                                 
                }                                        
##                 host6:[{                              
##                    'tor_ip':'172.18.90.3',            
##                    'tor_agent_id':'3',                
##                    'tor_type':'ovs',                  
##                    'tor_ovs_port':'4323',             
##                    'tor_ovs_protocol':'pssl',         
##                    'tor_tsn_ip':'172.17.90.6',        
##                    'tor_tsn_name':'5b7s6',            
##                    'tor_name':'5b7-qfx4',             
##                    'tor_tunnel_ip':'32.32.32.32',     
##                    'tor_vendor_name':'Juniper',       
##                    'tor_product_name':'QFX5100',      
##                    'tor_agent_http_server_port': '1231',
##                    'tor_agent_ovs_ka': '10000',         
##                       },                                
##                       {                                 
##                    'tor_ip':'172.18.90.4',              
##                    'tor_agent_id':'4',                  
##                    'tor_type':'ovs',                    
##                    'tor_ovs_port':'4324',               
##                    'tor_ovs_protocol':'pssl',           
##                    'tor_tsn_ip':'172.17.90.6',          
##                    'tor_tsn_name':'5b7s6',              
##                    'tor_name':'5b7-qfx5',               
##                    'tor_tunnel_ip':'31.31.31.31',       
##                    'tor_vendor_name':'Juniper',         
##                    'tor_product_name':'QFX5100',        
##                    'tor_agent_http_server_port': '1230',
##                    'tor_agent_ovs_ka': '10000',         
##                       },                                
##                       ],                                
##                                                         
##                 host7:[{                                
##                    'tor_ip':'172.18.90.3',              
##                    'tor_agent_id':'3',                  
##                    'tor_type':'ovs',                    
##                    'tor_ovs_port':'4323',               
##                    'tor_ovs_protocol':'pssl',           
##                    'tor_tsn_ip':'172.17.90.7',          
##                    'tor_tsn_name':'5b7s7',              
##                    'tor_name':'5b7-qfx4',               
##                    'tor_tunnel_ip':'32.32.32.32',       
##                    'tor_vendor_name':'Juniper',         
##                    'tor_product_name':'QFX5100',        
##                    'tor_agent_http_server_port': '1231',
##                    'tor_agent_ovs_ka': '10000',         
##                       },                                
##                       {                                 
##                    'tor_ip':'172.18.90.4',              
##                    'tor_agent_id':'4',                  
##                    'tor_type':'ovs',                    
##                    'tor_ovs_port':'4324',               
##                    'tor_ovs_protocol':'pssl',           
##                    'tor_tsn_ip':'172.17.90.7',          
##                    'tor_tsn_name':'5b7s7',              
##                    'tor_name':'5b7-qfx5',               
##                    'tor_tunnel_ip':'31.31.31.31',       
##                    'tor_vendor_name':'Juniper',         
##                    'tor_product_name':'QFX5100',        
##                    'tor_agent_http_server_port': '1230',
##                    'tor_agent_ovs_ka': '10000',         
##                       },                                
##                       ]                                 
##                }                                        
##                                                         
##                                                         
env.tor_hosts={                                            
'10.87.66.248': [{'tor_port': 'xe-0/0/48:3',               
                    'host_port' : 'p513p1',                
                    'mgmt_ip' : '10.87.66.155',            
                    'username' : 'root',                   
                    'password' : 'c0ntrail123',            
                  }],                                      
'10.87.66.250': [{'tor_port': 'xe-0/0/2',                  
                    'host_port' : 'p513p2',                
                    'mgmt_ip' : '10.87.66.155',            
                    'username' : 'root',                   
                    'password' : 'c0ntrail123',            
                  }]                                       
}                                                          
##                                                         
##env.physical_routers={                                   
##'5b7-mx80-2'          : {                                
##                     'vendor': 'juniper',                
##                     'model' : 'mx',                     
##                     'asn'   : '64513',                  
##                     'name'  : '5b7-mx80-2',             
##                     'ssh_username' : 'root',            
##                     'ssh_password' : 'Embe1mpls',       
##                     'mgmt_ip'   : '172.18.90.77',       
##                     'tunnel_ip' : '7.7.7.77',           
##                     'ports' : [],                       
##                     'type'  : 'router',                 
##                 },                                      
##'5b7-qfx2'       : {                                     
##                     'vendor': 'juniper',                
##                     'model' : 'qfx5100',                
##                     'asn'   : '64513',                  
##                     'name'  : '5b7-qfx2',               
##                     'ssh_username' : 'root',            
##                     'ssh_password' : 'Embe1mpls',       
##                     'mgmt_ip'  : '172.18.90.1',         
##                     'tunnel_ip' : '34.34.34.34',        
##                     'ports' : ['xe-0/0/46'],            
##                     'type'  : 'tor',                    
##},
##'5b7-qfx3'       : {
##                     'vendor': 'juniper',
##                     'model' : 'qfx5100',
##                     'asn'   : '64513',
##                     'name'  : '5b7-qfx3',
##                     'ssh_username' : 'root',
##                     'ssh_password' : 'Embe1mpls',
##                     'mgmt_ip'  : '172.18.90.2',
##                     'tunnel_ip' : '33.33.33.33',
##                     'ports' : ['xe-0/0/46'],
##                     'type'  : 'tor',
##},
##}
##
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

env.vgw = {host13: {'vgw1': {'vn': 'default-domain:admin:public1:public1', 'ipam-subnets': ['10.87.66.96/29', '10.87.66.128/29']}}}

