"""
"""
import sys
import json
from fabric.api import *
import paramiko
import os
import subprocess
import ast
import uuid
import random
import string
import time

if (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
    print '''
	THE CORRECT FORMAT OF USING THIS SCRIPT IS:
		python fabric_cluster_bringup.py <input_json_file> <function_to_perform>
	EXAMPLE :
		python fabric_cluster_bringup.py input.json get_x_auth_token
	'''
    sys.exit()

inp_file = sys.argv[1]
with open(inp_file) as json_data:
    parsed_json = json.load(json_data)

description = parsed_json["inp_params"]["description"]["msg"]
total_servers = parsed_json["inp_params"]["params"]["no_of_servers"]
total_networks = parsed_json["inp_params"]["params"]["no_of_networks"]

network_name_list = []
# parse all the data from the json file into a dict so that it an be used
# in the script

# Creating all The Dictionaries from the input json file that are required
# for all the functions to work properly in a scalable manner

server_dict = {}
network_dict = parsed_json["inp_params"]["networks"]
cluster_dict = {}
if "floating_ip_network" in parsed_json["inp_params"]:
   floating_ip_network_dict = parsed_json["inp_params"]["floating_ip_network"]
general_params_dict = parsed_json["inp_params"]["params"]
#testbed_py_dict = parsed_json["inp_params"]["testbed_py_params"]
testbed_py_dict = {}
all_cluster_dict = parsed_json["inp_params"]["cluster"]
provision_5_0_dict = {}


for clus in all_cluster_dict:
    server_dict[clus] = all_cluster_dict[clus]["servers"]
    cluster_dict[clus] = all_cluster_dict[clus]["cluster_json_params"]
    testbed_py_dict[clus] = all_cluster_dict[clus]["testbed_py_params"]
    provision_5_0_dict[clus] = all_cluster_dict[clus]["provison_5_0_config"]

for i in network_dict:
    network_name_list.append(network_dict[i]["name"])
    # A list to maintain all the network names

 
def build_server_data():
        a = subprocess.Popen('openstack server list -f json', shell=True, stdout=subprocess.PIPE)
        server_data= a.stdout.read()
        server_data= str(server_data)
        server_data=eval(server_data)
        for i in range(len(server_data)):
            server_data[i]["roles"] = []
            server_data[i]["name"] = server_data[i].pop("Name")
            server_data[i]["server_uuid"] = server_data[i].pop("ID")
            tmp = server_data[i]["Networks"].split(";")
            for item in tmp:
                if "public" in item:
                    server_data[i]["management_ip"] = str(item.split("=")[1])
                    server_data[i]["management_interface"] = "eth0"
                else:
                    server_data[i]["control_data_interface"] = {}
                    server_data[i]["control_data_interface"]["control_data_ip"] = str(item.split("=")[1])
                    server_data[i]["control_data_interface"]["control_data_interface"] = "eth1"
            for clus in server_dict:
                for j in server_dict[clus]:
                    if server_dict[clus][j]["name"] == server_data[i]["name"]:
                        for item in server_dict[clus][j]["roles"]:
                            server_data[i]["roles"].append(item.encode("utf-8"))
        return server_data

def build_data_for_api_to_add_servers():
    resources_dict = {}
    resources_dict["resources"]= []
    server_dict=build_server_data()
    for ser in range(len(server_dict)):
        # Server Data Dictionary
        temp_dict_server = {}
        temp_dict_server["kind"] = "node"
        temp_dict_server_data = {}
        temp_dict_server_data["type"] = "private"
        na_me = server_dict[ser]["name"].replace('_', '-')
        temp_dict_server_data["hostname"] = na_me
        temp_dict_server_data["ip_address"] = server_dict[ser]["management_ip"]
        temp_dict_server_data["interface_name"] = server_dict[ser]["management_interface"]
        temp_dict_server_data["uuid"] = server_dict[ser]["server_uuid"]
        if "control_data_interface" in server_dict[ser]:
            temp_dict_server_data["bms_info"] = {}
            temp_dict_server_data["bms_info"]["network_interface"] = "neutron"
            temp_dict_server_data["bms_info"]["driver"] = "pxe_ipmitool"
            temp_dict_server_data["isNode"] = "false"
        temp_dict_server_data["fq_name"] = []
        temp_dict_server_data["fq_name"].append("default-global-system-config")
        temp_dict_server_data["fq_name"].append(na_me + '-' + str(uuid.uuid4()))
        temp_dict_server["data"] = temp_dict_server_data
        resources_dict["resources"].append(temp_dict_server)
        # Management Management Interface Information
        temp_man_int = {}
        temp_man_int["kind"] = "port"
        temp_man_int_data = {}
        temp_man_int_data["parent_type"] = "node"
        temp_man_int_data["parent_uuid"] = server_dict[ser]["server_uuid"]
        temp_man_int_data["name"] = server_dict[ser]["management_interface"]
        temp_man_int_data["ip_address"] = server_dict[ser]["management_ip"]
        temp_man_int_data["pxe_enabled"] = "false"
        temp_man_int["data"] = temp_man_int_data
        resources_dict["resources"].append(temp_man_int)
        # Control Data Interface Information
        if "control_data_interface" in server_dict[ser]:
            temp_control_data_int = {}
            temp_control_data_int["kind"] = "port"
            temp_control_data_int_data = {}
            temp_control_data_int_data["parent_type"] = "node"
            temp_control_data_int_data["parent_uuid"] = server_dict[ser]["server_uuid"]
            temp_control_data_int_data["name"] = server_dict[ser]["control_data_interface"]["control_data_interface"]
            temp_control_data_int_data["ip_address"] = server_dict[ser]["control_data_interface"]["control_data_ip"]
            temp_control_data_int_data["pxe_enabled"] = "false"
            temp_control_data_int["data"] = temp_control_data_int_data
            resources_dict["resources"].append(temp_control_data_int)
    json_dumps_of_resources_dict = json.dumps(resources_dict)
#    print json_dumps_of_resources_dict
    return json_dumps_of_resources_dict

def build_combined_dict_for_provision():
    resources_dict = {}
    resources_dict["resources"]= []
    server_dict = build_server_data()
    cluster_details_dict = cluster_dict[clus]
    openstack_cluster_details_dict = cluster_dict[clus]["parameters"]["provision"]["openstack"]

    # Build Openstack Cluster details information part of the final dictionary
    temp = {}
    temp["kind"] = "openstack_cluster"
    temp["data"] = {}
    openstack_cluster_details_dict["cluster_uuid"] = ""
    openstack_cluster_details_dict["cluster_uuid"] = str(uuid.uuid4())
    temp["data"]["uuid"] = openstack_cluster_details_dict["cluster_uuid"]
    if "openstack_registry" in openstack_cluster_details_dict:
        temp["data"]["openstack_registry"] = openstack_cluster_details_dict["openstack_registry"]
    else:
        temp["data"]["openstack_registry"] = "default"
    if "openstack_release" in openstack_cluster_details_dict:
        temp["data"]["openstack_release"] = openstack_cluster_details_dict["openstack_release"]
    else:
        temp["data"]["openstack_release"] = "ocata"
    if "internal_vip" in openstack_cluster_details_dict:
        temp["data"]["openstack_internal_vip"] = openstack_cluster_details_dict["internal_vip"]
    if "external_vip" in openstack_cluster_details_dict:
        temp["data"]["openstack_external_vip"] = openstack_cluster_details_dict["external_vip"]
    if "kolla_globals" in openstack_cluster_details_dict:
        temp["data"]["kolla_globals"] = {}
        temp["data"]["kolla_globals"]["key_value_pair"] = []
        for i in openstack_cluster_details_dict["kolla_globals"]:
            temp_d = {}
            temp_d["key"] = i
            temp_d["value"] = openstack_cluster_details_dict["kolla_globals"][i]
            temp["data"]["kolla_globals"]["key_value_pair"].append(temp_d)
    if "kolla_passwords" in openstack_cluster_details_dict:
        temp["data"]["kolla_passwords"] = {}
        temp["data"]["kolla_passwords"]["key_value_pair"] = []
        for i in openstack_cluster_details_dict["kolla_passwords"]:
            temp_d = {}
            temp_d["key"] = i
            temp_d["value"] = openstack_cluster_details_dict["kolla_passwords"][i]
            temp["data"]["kolla_passwords"]["key_value_pair"].append(temp_d)
    if "customize" in openstack_cluster_details_dict:
        temp["data"]["customize"] = openstack_cluster_details_dict["customize"]
    else:
        temp["data"]["customize"] = "nova.conf: |\n        [libvirt]\n        virt_type=qemu\n        cpu_mode=none"
    fq_name_list = []
    fq_name_list.append("default-global-system-config")
    fq_name_list.append(cluster_details_dict["cluster_name"] + '-' + str(uuid.uuid4()))
    temp["data"]["fq_name"] = fq_name_list
    resources_dict["resources"].append(temp)

    # Build Contrail Cluster Information part of the final dictionary   
    temp = {}
    temp["kind"] = "contrail_cluster"
    temp["data"] = {}
    temp["data"]["display_name"] = cluster_details_dict["cluster_name"]
#    temp["data"]["provisioner_type"] = cluster_details_dict["provisioning_type"]
    temp["data"]["ntp_server"] = provision_5_0_dict[clus]["provider_config"]["ntp_server"]
    temp["data"]["domain_suffix"] = provision_5_0_dict[clus]["provider_config"]["domain_suffix"]
    temp["data"]["encap_priority"] = cluster_details_dict["encap_priority"]
    temp["data"]["registry_private_insecure"] = cluster_details_dict["registry_private_insecure"]
    temp["data"]["container_registry"] = provision_5_0_dict[clus]["deployment_config"]["deployments"]["contrail"]["registry"]
    temp["data"]["contrail_version"] = provision_5_0_dict[clus]["deployment_config"]["version"]
    temp["data"]["high_availability"] = cluster_details_dict["high_availability"]
    temp["data"]["orchestrator"] = provision_5_0_dict[clus]["deployment_config"]["orchestrator"]
    temp["data"]["provisioning_state"] = "NOSTATE"
    temp["data"]["uuid"] = cluster_details_dict["cluster_uuid"]
    temp["data"]["default_gateway"] = cluster_details_dict["default_gateway"]
    temp["data"]["contrail_configuration"] = {}
    temp["data"]["contrail_configuration"]["key_value_pair"] = []
    list_openstack_nodes = []
    list_controller_nodes = []
    list_control_nodes = []
    for ser in range(len(server_dict)):
        if "openstack" in server_dict[ser]["roles"]:
#            list_openstack_nodes.append(server_dict[ser]["management_ip"])
            if "control_data_interface" in server_dict[ser]:
                list_openstack_nodes.append(server_dict[ser]["control_data_interface"]["control_data_ip"])
        if "control" in server_dict[ser]["roles"]:
            list_controller_nodes.append(server_dict[ser]["management_ip"])
            if "control_data_interface" in server_dict[ser]:
                list_control_nodes.append(server_dict[ser]["control_data_interface"]["control_data_ip"])
    temp_openstack = {}
    temp_openstack["key"] = "OPENSTACK_NODES"
    temp_openstack["value"] = ",".join(list_openstack_nodes)
    temp["data"]["contrail_configuration"]["key_value_pair"].append(temp_openstack)
    temp_controller = {}
    temp_controller["key"] = "CONTROLLER_NODES"
    temp_controller["value"] = ",".join(list_controller_nodes)
    temp["data"]["contrail_configuration"]["key_value_pair"].append(temp_controller)
    if "control_data_interface" in server_dict[ser]:
        temp_control = {}
        temp_control["key"] = "CONTROL_NODES"
        temp_control["value"] = ",".join(list_control_nodes)
        temp["data"]["contrail_configuration"]["key_value_pair"].append(temp_control)
        temp["data"]["OPENSTACK_NODES"] = ",".join(list_openstack_nodes)
        temp["data"]["CONTROLLER_NODES"] = ",".join(list_controller_nodes)
        temp["data"]["CONTROL_NODES"] = ",".join(list_control_nodes)
    fq_name_list = []
    fq_name_list.append("default-global-system-config")
    fq_name_list.append(cluster_details_dict["cluster_name"] + '-' + str(uuid.uuid4()))
    temp["data"]["fq_name"] = fq_name_list
    temp["data"]["openstack_cluster_refs"] = []
    t_dict = {}
    t_dict["uuid"] = openstack_cluster_details_dict["cluster_uuid"]
    temp["data"]["openstack_cluster_refs"].append(t_dict)
    resources_dict["resources"].append(temp)

    # Create Orchestrator Information part of the final Dictionary
    list_of_orchestrator_servers = []
    orch_used = provision_5_0_dict[clus]["deployment_config"]["orchestrator"]
    for ser in range(len(server_dict)):
        if orch_used in server_dict[ser]["roles"]:
            list_of_orchestrator_servers.append(ser)

    #print list_of_orchestrator_servers
    for ser in list_of_orchestrator_servers:
        # Create openstack_control_node dict
        temp = {}
        temp["kind"] = "openstack_control_node"
        temp["data"] = {}
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "openstack-cluster"
        temp["data"]["parent_uuid"] = openstack_cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)
        # Create openstack_network_node  dict
        temp = {}
        temp["kind"] = "openstack_storage_node"
        temp["data"] = {}
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "openstack-cluster"
        temp["data"]["parent_uuid"] = openstack_cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)
        # Create openstack_monitoring_node dict
        temp = {}
        temp["kind"] = "openstack_monitoring_node"
        temp["data"] = {}
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "openstack-cluster"
        temp["data"]["parent_uuid"] = openstack_cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)
        # Create openstack_network_node dict
        temp = {}
        temp["kind"] = "openstack_network_node"
        temp["data"] = {}
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "openstack-cluster"
        temp["data"]["parent_uuid"] = openstack_cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)

    # Create Compute (vRouter) Information part of the final Dictionary
    list_of_compute_servers = []
    for ser in range(len(server_dict)):
        if "openstack_compute" in server_dict[ser]["roles"]:
            list_of_compute_servers.append(ser)
    for ser in list_of_compute_servers:
        # Create openstack_compute_node dict
        temp = {}
        temp["kind"] = "openstack_compute_node"
        temp["data"] = {}
        if "default_gateway" in cluster_details_dict:
            temp["data"]["default_gateway"] = cluster_details_dict["default_gateway"]
        else:
            temp["data"]["default_gateway"] = ""
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "openstack-cluster"
        temp["data"]["parent_uuid"] = openstack_cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)
        # Create contrail_vrouter_node dict
        temp = {}
        temp["kind"] = "contrail_vrouter_node"
        temp["data"] = {}
        if "default_gateway" in cluster_details_dict:
                temp["data"]["default_gateway"] = cluster_details_dict["default_gateway"]
        else:
                temp["data"]["default_gateway"] = ""
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "contrail-cluster"
        temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)

    # Create Contrail Service (service) Information part of the final Dictionary
    list_of_service_servers = []
    for ser in range(len(server_dict)):
        if "service" in server_dict[ser]["roles"]:
            list_of_service_servers.append(ser)
    for ser in list_of_service_servers:
        # Create contrail_service_node dict
        temp = {}
        temp["kind"] = "contrail_service_node"
        temp["data"] = {}
        if "default_gateway" in cluster_details_dict:
            temp["data"]["default_gateway"] = cluster_details_dict["default_gateway"]
        else:
            temp["data"]["default_gateway"] = ""
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "contrail-cluster"
        temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)

    # Create Contrail Information (control, config, database, webui) part of the final Dictionary
    list_of_contrail_servers = []
    for ser in range(len(server_dict)):
        if "control" in server_dict[ser]["roles"]:
            list_of_contrail_servers.append(ser)
    for ser in list_of_contrail_servers:
        # Create contrail_config_node dict
        temp = {}
        temp["kind"] = "contrail_config_node"
        temp["data"] = {}
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "contrail-cluster"
        temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)
        # Create contrail_config_database_node dict
        temp = {}
        temp["kind"] = "contrail_config_database_node"
        temp["data"] = {}
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "contrail-cluster"
        temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)
        # Create contrail_analytics_node dict
        temp = {}
        temp["kind"] = "contrail_analytics_node"
        temp["data"] = {}
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "contrail-cluster"
        temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)
        # Create contrail_analytics_database_node dict
        temp = {}
        temp["kind"] = "contrail_analytics_database_node"
        temp["data"] = {}
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "contrail-cluster"
        temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)
        # Create contrail_control_node dict
        temp = {}
        temp["kind"] = "contrail_control_node"
        temp["data"] = {}
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "contrail-cluster"
        temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)
        # Create contrail_webui_node dict
        temp = {}
        temp["kind"] = "contrail_webui_node"
        temp["data"] = {}
        temp["data"]["uuid"] = str(uuid.uuid4())
        temp["data"]["name"] = temp["data"]["uuid"]
        temp["data"]["parent_type"] = "contrail-cluster"
        temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
        temp["data"]["node_refs"] = []
        serv_uuid = server_dict[ser]["server_uuid"]
        node_refs_dict = {}
        node_refs_dict["uuid"] = serv_uuid
        temp["data"]["node_refs"].append(node_refs_dict)
        temp["operation"] = "CREATE"
        resources_dict["resources"].append(temp)

    resources_json = json.dumps(resources_dict)
#    print resources_json
    return resources_json

def get_contrail_command_node_ip():
        server_data = build_server_data()
        for i in range(len(server_data)):
            if "contrail_command" in server_data[i]["roles"]:
                contrail_command_node_ip = server_data[i]["management_ip"]
                print server_data[i]["management_ip"]

def get_x_auth_token(go_server_ip):
#        go_server_ip = get_contrail_command_node_ip()
        go_server_port = "9091"
	url = "'https://%s:%s/keystone/v3/auth/tokens'" % (go_server_ip, go_server_port)
	data = '{"auth":{"identity":{"methods":["password"],"password":{"user":{"name":"admin","domain":{"id":"default"},"password":"contrail123"}}}}}'
	#print url
	#print data
	a = subprocess.Popen(["curl %s -H 'Accept: */*' --compressed -H 'Connection: keep-alive' -H 'Content-Type: application/json' -H 'X-Requested-With: XMLHttpRequest' --data '%s'  --insecure --include " % (url, data)], stdout=subprocess.PIPE, shell=True).communicate()  	
	temp_token = ""
	ab = str(a)
	abc = ab.split(',')
	#print abc
	for temp in abc:
		if "X-Subject-Token" in temp:
			temp_token = temp
			temp_token1 = temp_token.split("X-Subject-Token:")
			temp_token12 = temp_token1[1]
			#print temp_token12
			temp_token13 = temp_token12.split("\\")
			temp_token14 = temp_token13[0]
			temp_token_last = temp_token14.replace(' ', '')
#	print temp_token_last
	
	url = "'https://%s:%s/keystone/v3/auth/projects'" % (go_server_ip, go_server_port)
	a = subprocess.Popen(["curl %s -H 'Accept: */*' --compressed -H 'Connection: keep-alive' -H 'Content-Type: application/json' -H 'X-Requested-With: XMLHttpRequest' -H 'X-Auth-Token:%s' --insecure --include " % (url, temp_token_last)], stdout=subprocess.PIPE, shell=True).communicate()
	# Generate the final X-AUTH_TOKEN
	url = "'https://%s:%s/keystone/v3/auth/tokens'" % (go_server_ip, go_server_port)
	data = '{"auth":{"identity":{"methods":["token"],"token":{"id":"%s"}},"scope":{"project":{"id":"admin"}}}}' %temp_token_last 
	a = subprocess.Popen(["curl %s -H 'Accept: */*' --compressed -H 'Connection: keep-alive' -H 'Content-Type: application/json' -H 'X-Requested-With: XMLHttpRequest' --data '%s' --insecure --include " % (url, data)], stdout=subprocess.PIPE, shell=True).communicate()
	final_token = ""
	ab = str(a)
	abc = ab.split(',')
	#print abc
	for temp in abc:
		if "X-Subject-Token" in temp:
			temp_token = temp
                        temp_token1 = temp_token.split("X-Subject-Token:")
                        temp_token12 = temp_token1[1]
                        #print temp_token12
                        temp_token13 = temp_token12.split("\\")
                        temp_token14 = temp_token13[0]
                        temp_token_last = temp_token14.replace(' ', '')
			final_token = temp_token_last
#        return final_token
	print final_token

def add_servers(go_server_ip,final_token):
        go_server_port = "9091"
        url = "'https://%s:%s/sync'" % (go_server_ip, go_server_port)
        server_data=str(build_data_for_api_to_add_servers())
        a = subprocess.Popen(["curl %s -H 'Accept: */*' --compressed -H 'Connection: keep-alive' -H 'Content-Type: application/json' -H 'X-Requested-With: XMLHttpRequest' -H 'X-Auth-Token: %s' --data '%s' --insecure --include " % (url,final_token, server_data)], stdout=subprocess.PIPE, shell=True).communicate()
        add_server_response = str(a)
        if "201 Created" in add_server_response:
            print "Passed"
        else:
            print "Failed to add servers ..\n",add_server_response

def start_ansible_provisioning(go_server_ip,final_token):
       go_server_port = "9091"
       url = "'https://%s:%s/sync'" % (go_server_ip, go_server_port)
       prov_dict=str(build_combined_dict_for_provision())
       a = subprocess.Popen(["curl %s -H 'Accept: */*' --compressed -H 'Connection: keep-alive' -H 'Content-Type: application/json' -H 'X-Requested-With: XMLHttpRequest' -H 'X-Auth-Token: %s' --data '%s' --insecure --include " % (url,final_token, prov_dict)], stdout=subprocess.PIPE, shell=True).communicate()
       prov_response = str(a)
       if "201 Created" in prov_response:
           print "Passed"
       else:
           print "Failed to start provisioning via contrail command ..\n",prov_response

def get_provisioning_status(go_server_ip,final_token):
        go_server_port = "9091"
        cluster_details_dict = cluster_dict[clus]
        url = "'https://%s:%s/contrail-cluster/%s'" % (go_server_ip, go_server_port, cluster_details_dict["cluster_uuid"])
        a = subprocess.Popen(["curl -X GET %s -H 'Accept: */*' --compressed -H 'Connection: keep-alive' -H 'Content-Type: application/json' -H 'X-Requested-With: XMLHttpRequest'  -H 'x-auth-token: %s'  --insecure --include " % (url, final_token)], stdout=subprocess.PIPE, shell=True).communicate()
        tmp = str(a)
        if "200 OK" in tmp:
            for item in tmp.split(","):
                if "provisioning_state" in item:
                    val = item.split(":")
                    break
            print val[-1]
        elif "401 Unauthorized" in tmp:
            print "CREATED"

if __name__ == '__main__':
    if len(sys.argv) <=3:
        globals()[sys.argv[2]]()
    elif len(sys.argv) <=4:
        globals()[sys.argv[2]](sys.argv[3])
    elif len(sys.argv) <=5:
        globals()[sys.argv[2]](sys.argv[3],sys.argv[4])
