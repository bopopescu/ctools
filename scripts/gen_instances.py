#!/usr/bin/python3
import yaml 
import os
import ipaddress
import random
import sys

if len(sys.argv) != 3:
    print('Incorrect usage')
    print('Usage : ./gen_instances.py input.yaml templates.yaml')
    exit()

# Open file all.yml
stream = open('all.yml', 'w') 

# Read test specific config file
#test_stream = open('input.yaml', 'r')  
test_stream = open(sys.argv[1], 'r')
for x in yaml.load_all(test_stream):
    test_dict = x 

# Store test specific variables
test_var_dict = dict(test_dict['test_var'])

# Store machines specific variables 
machines_dict = dict(test_dict['machine_info'])
machine_names = machines_dict.keys()
number_of_machines = len(machines_dict.keys())

# Store role info for instances
role_dict = dict(test_dict['role_def']) 

# Calculate number of bms
number_of_bms = 0
bms_names = []
bms_ips = []
for machine in machines_dict:
    if machines_dict[machine]['number_of_vms'] == 0:
        number_of_bms = number_of_bms + 1
        bms_names.append(machines_dict[machine]['name'])
        bms_ips.append(machines_dict[machine]['ip'])

# Calculate the number of hypervisors
number_of_hypervisors = 0 
hypervisor_names = [] 
hypervisor_ips = [] 
for machine in machines_dict:
    if machines_dict[machine]['number_of_vms'] > 0:
        number_of_hypervisors = number_of_hypervisors + 1 
        hypervisor_names.append(machines_dict[machine]['name'])
        hypervisor_ips.append(machines_dict[machine]['ip'])  

# Calculate the number of instances
number_of_instances = 0
for machine in machines_dict:
    number_of_instances = number_of_instances + machines_dict[machine]['number_of_vms']
number_of_instances = number_of_instances + number_of_bms

# Create the ip list
start_ip = test_var_dict['start_ip']
start_addr = ipaddress.IPv4Address(start_ip)   
ip_list = [] 
for ip in range(1,number_of_instances + 1):
    ip_list.append(str(start_addr+ip))   

# Generate unique mac address
mac_addr_list = []
def randomMAC():
        mac = [ 0x00,
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff) ]
        return ':'.join(map(lambda x: "%02x" % x, mac))  

# Read all block templates and store them
#template_stream = open('templates.yaml', 'r') 
template_stream = open(sys.argv[2], 'r')
for x in yaml.load_all(template_stream):
    deployment_dict = x['deployment_section']
    servermanager_dict = x['servermanager_section']
    providerconfig_dict = x['providerconfig_section']
    instance_template_dict = x['instances_section']
    host_template_dict = x['hosts_section']
    network_template_dict = host_template_dict['network']
    interfaces_template_dict = network_template_dict['interfaces']
    intf1_template = interfaces_template_dict['intf1']
    intf2_template = interfaces_template_dict['intf2'] 
    contrail_config_dict =  x['contrail_section']
    kolla_config_dict =   x['kolla_section']
    orchestrator_config_dict =   x['orchestrator_section']
    test_topo_dict =   x['test_topo_section']

# Create the instances block
instances_dict = {} 
instances_list_dict = {} 
instances_list = []

for machine in machines_dict:
    if machines_dict[machine]['number_of_vms'] > 0:
        for vm_num in range(1,machines_dict[machine]['number_of_vms'] + 1):
            instances_list.append(str(machines_dict[machine]['name'])+'-vm'+str(vm_num))
    else:
        for vm_num in range(1,2):
            #instances_list.append(str(machines_dict[machine]['name'])+'-vm'+str(vm_num))
            instances_list.append(str(machines_dict[machine]['name']))

## create all the instances
vrouter_role = ['vrouter','openstack_compute']
for instance_num in range(0,number_of_instances):
    instances_list_dict[instances_list[instance_num]] = dict(instance_template_dict)
    instances_list_dict[instances_list[instance_num]]['provider'] = 'bms'
    instances_list_dict[instances_list[instance_num]]['ip'] = ip_list[instance_num]
    if instances_list[instance_num] in role_dict.keys():
        instances_list_dict[instances_list[instance_num]]['roles'] = role_dict[instances_list[instance_num]]['roles']
    else:
        instances_list_dict[instances_list[instance_num]]['roles'] = dict.fromkeys(vrouter_role)
    del instances_list_dict[instances_list[instance_num]]['instance_name']
instances_dict = {'instances': instances_list_dict}   

hypervisors_list = [] 
for machine in machines_dict:
    if machines_dict[machine]['number_of_vms'] > 0:
            hypervisors_list.append(machines_dict[machine])     

## create hosts per hypervisor
def get_hosts_kvm(hyp_dict,bms_index):
    hosts_list_dict = {}
    instances_per_bms = hyp_dict['number_of_vms']
    for host_num in range(1,instances_per_bms+1):
        hosts_list_dict['host'+str(host_num)] = dict(host_template_dict)
        hosts_list_dict['host'+str(host_num)]['name'] = hyp_dict['name']+'-vm'+str(host_num)
        hosts_list_dict['host'+str(host_num)]['ip'] =  instances_dict['instances'][hyp_dict['name']+'-vm'+str(host_num)]['ip']
        hosts_list_dict['host'+str(host_num)]['ram'] =  1024
        hosts_list_dict['host'+str(host_num)]['vcpus'] = 4
        hosts_list_dict['host'+str(host_num)]['server'] = 'kvm_host'+str(host_num)
        hosts_list_dict['host'+str(host_num)]['network'] = dict(network_template_dict)
        hosts_list_dict['host'+str(host_num)]['network']['interfaces'] = dict(interfaces_template_dict)
        hosts_list_dict['host'+str(host_num)]['network']['interfaces']['intf1'] = dict(intf1_template)
        if 'bond_interface_name' in machines_dict[bms_index].keys():
            hosts_list_dict['host'+str(host_num)]['network']['interfaces']['intf1']['bridge'] = machines_dict[bms_index]['bond_interface_name']
        else:
            hosts_list_dict['host'+str(host_num)]['network']['interfaces']['intf1']['bridge'] = hyp_dict['interface1']
        random_mac = randomMAC() 
        mac_addr_list.append(random_mac)
        hosts_list_dict['host'+str(host_num)]['network']['interfaces']['intf1']['mac'] = random_mac
        if test_var_dict['multi_interface'] == True:
            hosts_list_dict['host'+str(host_num)]['network']['interfaces']['intf2'] = dict(intf2_template)
            hosts_list_dict['host'+str(host_num)]['network']['interfaces']['intf2']['bridge'] = hyp_dict['interface2']
            random_mac = randomMAC()
            mac_addr_list.append(random_mac)
            hosts_list_dict['host'+str(host_num)]['network']['interfaces']['intf2']['mac'] = random_mac
        else:
            del hosts_list_dict['host'+str(host_num)]['network']['interfaces']['intf2']
    return hosts_list_dict 

kvmhost_names = []
for kvm_num in range(1,number_of_hypervisors+1):
    kvmhost_names.append('kvm_host'+str(kvm_num))   

hypervisors_list_dict = {}
for kvmhost in kvmhost_names:
    temp = {}
    temp['ip'] = hypervisor_ips.pop(0) 
    temp['username'] = "root"
    temp['password'] = "c0ntrail123"
    hyp_dict = hypervisors_list.pop(0)
    for bms in machines_dict:
        if str(machines_dict[bms]['ip']) == str(hyp_dict['ip']):
           bms_index = bms
           break
    temp['vm_config'] = get_hosts_kvm(hyp_dict,bms_index)
    hypervisors_list_dict[kvmhost] = dict(temp)

default_dict = {}
default_dict['image_dest'] = test_var_dict['image_dest']
default_dict['disk_format'] =  test_var_dict['disk_format'] 
default_dict['vagrant_images'] = test_var_dict['vagrant_images'] 
default_dict['vagrant_plugin'] =  test_var_dict['vagrant_plugin'] 
default_dict['vagrant_box'] =  test_var_dict['vagrant_box'] 
default_dict['vagrant_box_name'] = test_var_dict['vagrant_box_name'] 

vm_info = {'default': default_dict,
           'hypervisors': hypervisors_list_dict} 
vm_info_dict = {'vm_info': vm_info}
bond_info_dict = {'bond_info': machines_dict}

deployment_dict['deployment']['orchestrator'] = test_var_dict['orchestrator']
deployment_dict['deployment']['type']['contrail']['branch'] = test_var_dict['contrail_branch']
deployment_dict['deployment']['type']['contrail']['registry'] = test_var_dict['contrail_registry']
deployment_dict['deployment']['type']['kolla']['branch'] = test_var_dict['kolla_branch']
deployment_dict['deployment']['type']['kolla']['registry'] = test_var_dict['kolla_registry']
deployment_dict['deployment']['sku'] = test_var_dict['sku']
deployment_dict['deployment']['version'] = test_var_dict['version']
deployment_dict['deployment']['os'] = test_var_dict['os']
servermanager_dict['server_manager']['ip'] = test_var_dict['server_manager'] 
orchestrator_config_dict['orchestrator_configuration']['internal_vip'] = test_var_dict['internal_vip']
orchestrator_config_dict['orchestrator_configuration']['external_vip'] = test_var_dict['external_vip']
kolla_config_dict['kolla_config']['kolla_globals']['kolla_internal_vip_address'] = test_var_dict['internal_vip']
kolla_config_dict['kolla_config']['kolla_globals']['kolla_external_vip_address'] = test_var_dict['external_vip']
kolla_config_dict['kolla_config']['kolla_globals']['contrail_api_interface_address'] = test_var_dict['contrail_api_interface_addr']
kolla_config_dict['kolla_config']['kolla_globals']['docker_registry'] = test_var_dict['contrail_registry']
contrail_config_dict['contrail_configuration']['CONTAINER_REGISTRY'] = test_var_dict['contrail_registry']
contrail_config_dict['contrail_configuration']['CONTRAIL_VERSION'] = test_var_dict['version']
contrail_config_dict['contrail_configuration']['CLOUD_ORCHESTRATOR'] = test_var_dict['orchestrator']
contrail_config_dict['contrail_configuration']['KEYSTONE_AUTH_HOST'] = test_var_dict['keystone_auth_host']
contrail_config_dict['contrail_configuration']['VROUTER_GATEWAY'] = test_var_dict['vrouter_gw']
 

yaml.dump(deployment_dict,stream,default_flow_style=False)
yaml.dump(servermanager_dict,stream,default_flow_style=False)
yaml.dump(providerconfig_dict,stream,default_flow_style=False) 
yaml.dump(contrail_config_dict,stream,default_flow_style=False) 
yaml.dump(kolla_config_dict,stream,default_flow_style=False)  
yaml.dump(orchestrator_config_dict,stream,default_flow_style=False)  
yaml.dump(test_topo_dict,stream,default_flow_style=False)  
yaml.dump(instances_dict,stream,default_flow_style=False)
yaml.dump(vm_info_dict,stream,default_flow_style=False)  
yaml.dump(bond_info_dict,stream,default_flow_style=False) 
if len(mac_addr_list) != len(set(mac_addr_list)):
   print('MAC addr is not uniquely generated')  
