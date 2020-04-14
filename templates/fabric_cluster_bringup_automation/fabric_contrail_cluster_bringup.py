"""
Author: Soumil Kulkarni
File Name: inp_to_yaml.py
Summary: Script to create a virtualized infrastructure for running daily sanity or recreating any bugs for testing purpose. (Contrail on Contrail)
"""
import sys
import json
import uuid
import os
import time
import subprocess

inp_file = sys.argv[1]
with open(inp_file) as json_data:
    parsed_json = json.load(json_data)

server_dict = parsed_json["params"]["servers"]
go_server_dict = parsed_json["params"]["go_server_details"]
cluster_details_dict = parsed_json["params"]["contrail_cluster_details"]
openstack_cluster_details_dict  = parsed_json["params"]["openstack_cluster_details"]
#server_uuid_dict = {}
#for ser in server_dict:
#	temp_uuid = str(uuid.uuid4())
#	server_uuid_dict[ser] = temp_uuid

def build_data_for_api_to_add_servers():
	resources_dict = {}
	resources_dict["resources"]= []
	for ser in server_dict:
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
	print json_dumps_of_resources_dict	
	
def build_combined_dict_for_provision():
	#print cluster_details_dict 	
	resources_dict = {}
	resources_dict["resources"]= []
	# Build Contrail Cluster Information part of the final dictionary	
	temp = {}
	temp["kind"] = "contrail_cluster"
	temp["data"] = {}
	temp["data"]["display_name"] = cluster_details_dict["cluster_name"]
	temp["data"]["provisioner_type"] = cluster_details_dict["provision_type"]
	temp["data"]["ntp_server"] = cluster_details_dict["ntp_server"]
	temp["data"]["encap_priority"] = cluster_details_dict["encap_priority"]
	temp["data"]["registry_private_insecure"] = cluster_details_dict["registry_private_insecure"]
	temp["data"]["container_registry"] = cluster_details_dict["container_registry"]
	temp["data"]["contrail_version"] = cluster_details_dict["contrail_version"]
	temp["data"]["high_availability"] = cluster_details_dict["high_availability"]
	temp["data"]["orchestrator"] = cluster_details_dict["orchestrator"]
	temp["data"]["provisioning_state"] = "NOSTATE"
	temp["data"]["uuid"] = cluster_details_dict["cluster_uuid"]
	temp["data"]["default_gateway"] = cluster_details_dict["default_gateway"]
	temp["data"]["contrail_configuration"] = {}
	temp["data"]["contrail_configuration"]["key_value_pair"] = []
	list_openstack_nodes = []
	list_controller_nodes = []
	list_control_nodes = []
	for ser in server_dict:
		if "openstack" in server_dict[ser]["roles"]:
			list_openstack_nodes.append(server_dict[ser]["management_ip"])
		if "contrail-control" in server_dict[ser]["roles"]:
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
	if "fq_name" in cluster_details_dict:
		temp["data"]["fq_name"] = cluster_details_dict["fq_name"]
	else:
		t_list = ["admin", "default"]
		t_list.append(cluster_details_dict["cluster_name"])
		temp["data"]["fq_name"] = t_list
	#temp["data"]["parent_uuid"] = "admin"
	#temp["data"]["parent_uuid"] = "project"
	temp["data"]["openstack_cluster_refs"] = []
	t_dict = {}
	t_dict["uuid"] = openstack_cluster_details_dict["cluster_uuid"]
	temp["data"]["openstack_cluster_refs"].append(t_dict)
	resources_dict["resources"].append(temp)
	
	# Build Openstack Cluster details information part of the final dictionary
	temp = {}
	temp["kind"] = "openstack_cluster"
	temp["data"] = {}
#	temp["data"]["display_name"] = openstack_cluster_details_dict["cluster_name"]
	temp["data"]["uuid"] = openstack_cluster_details_dict["cluster_uuid"]
	#temp["data"]["parent_type"] = "project"
	#temp["data"]["parent_uuid"] = "admin"
	if "openstack_registry" in openstack_cluster_details_dict:
		temp["data"]["openstack_registry"] = openstack_cluster_details_dict["openstack_registry"]
	else:
		temp["data"]["openstack_registry"] = "default"
	if "openstack_release" in openstack_cluster_details_dict:
		temp["data"]["openstack_release"] = openstack_cluster_details_dict["openstack_release"]
	else:
		temp["data"]["openstack_release"] = "ocata"
#	if "ntp_server" in openstack_cluster_details_dict:
#		temp["data"]["ntp_server"] = openstack_cluster_details_dict["ntp_server"]
#	else:
#		temp["data"]["ntp_server"] = "10.84.5.100"
#	if "fq_name" in openstack_cluster_details_dict:
#		temp["data"]["fq_name"] = openstack_cluster_details_dict["fq_name"]
#	else:
#		t_list = ["admin", "default"]
#		t_list.append(openstack_cluster_details_dict["cluster_name"])
#		temp["data"]["fq_name"] = t_list
	if "openstack_internal_vip" in openstack_cluster_details_dict:
		temp["data"]["openstack_internal_vip"] = openstack_cluster_details_dict["openstack_internal_vip"]
	if "openstack_external_vip" in openstack_cluster_details_dict:
		temp["data"]["openstack_external_vip"] = openstack_cluster_details_dict["openstack_external_vip"]
	if "kolla_globals" in openstack_cluster_details_dict:
		temp["data"]["kolla_globals"] = {}
		temp["data"]["kolla_globals"]["key_value_pair"] = []
		for i in openstack_cluster_details_dict["kolla_globals"]:
			temp_d = {}
			temp_d["key"] = i
			temp_d["value"] = openstack_cluster_details_dict["kolla_globals"][i]
			temp["data"]["kolla_globals"]["key_value_pair"].append(temp_d)
	resources_dict["resources"].append(temp)
	
	# Create Orchestrator Information part of the final Dictionary
	list_of_orchestrator_servers = []
	orch_used = cluster_details_dict["orchestrator"] 
	for ser in server_dict:
		if orch_used in server_dict[ser]["roles"]:
			list_of_orchestrator_servers.append(ser)

	#print list_of_orchestrator_servers
	for ser in list_of_orchestrator_servers:
		# Create openstack_control_node dict
		temp = {}
		temp["kind"] = "openstack_control_node"
		temp["data"] = {}
		temp["data"]["parent_type"] = "openstack_cluster"
		temp["data"]["parent_uuid"] = openstack_cluster_details_dict["cluster_uuid"]
		temp["data"]["node_refs"] = []
		serv_uuid = server_dict[ser]["server_uuid"]
		node_refs_dict = {}
		node_refs_dict["uuid"] = serv_uuid
		temp["data"]["node_refs"].append(node_refs_dict)
		resources_dict["resources"].append(temp)	
		# Create openstack_network_node  dict
		temp = {}
		temp["kind"] = "openstack_storage_node"
		temp["data"] = {}
                temp["data"]["parent_type"] = "openstack_cluster"
                temp["data"]["parent_uuid"] = openstack_cluster_details_dict["cluster_uuid"]
                temp["data"]["node_refs"] = []
                serv_uuid = server_dict[ser]["server_uuid"]
                node_refs_dict = {}
                node_refs_dict["uuid"] = serv_uuid
                temp["data"]["node_refs"].append(node_refs_dict)
                resources_dict["resources"].append(temp)
		# Create openstack_monitoring_node dict
		temp = {}
                temp["kind"] = "openstack_monitoring_node"	
		temp["data"] = {}
                temp["data"]["parent_type"] = "openstack_cluster"
                temp["data"]["parent_uuid"] = openstack_cluster_details_dict["cluster_uuid"]
                temp["data"]["node_refs"] = []
                serv_uuid = server_dict[ser]["server_uuid"]
                node_refs_dict = {}
                node_refs_dict["uuid"] = serv_uuid
                temp["data"]["node_refs"].append(node_refs_dict)
                resources_dict["resources"].append(temp)
		# Create openstack_network_node dict
		temp = {}
                temp["kind"] = "openstack_network_node"
                temp["data"] = {}
                temp["data"]["parent_type"] = "openstack_cluster"
                temp["data"]["parent_uuid"] = openstack_cluster_details_dict["cluster_uuid"]
                temp["data"]["node_refs"] = []
                serv_uuid = server_dict[ser]["server_uuid"]
                node_refs_dict = {}
                node_refs_dict["uuid"] = serv_uuid
                temp["data"]["node_refs"].append(node_refs_dict)
                resources_dict["resources"].append(temp)
	
	# Create Compute (vRouter) Information part of the final Dictionary
	list_of_compute_servers = []
        for ser in server_dict:
                if "compute" in server_dict[ser]["roles"]:
                        list_of_compute_servers.append(ser)
	for ser in list_of_compute_servers:
		# Create openstack_compute_node dict
		temp = {}
		temp["kind"] = "openstack_compute_node"
		temp["data"] = {}
		if "default_gateway" in server_dict[ser]:
			temp["data"]["default_gateway"] = server_dict[ser]["default_gateway"]
		else:
			temp["data"]["default_gateway"] = ""
		temp["data"]["parent_type"] = "openstack_cluster"
		temp["data"]["parent_uuid"] = openstack_cluster_details_dict["cluster_uuid"]
		temp["data"]["node_refs"] = []
		serv_uuid = server_dict[ser]["server_uuid"]
		node_refs_dict = {}
		node_refs_dict["uuid"] = serv_uuid
		temp["data"]["node_refs"].append(node_refs_dict)
		resources_dict["resources"].append(temp)	
		# Create contrail_vrouter_node dict
		temp = {}
                temp["kind"] = "contrail_vrouter_node"
                temp["data"] = {}
                if "default_gateway" in server_dict[ser]:
                        temp["data"]["default_gateway"] = server_dict[ser]["default_gateway"]
                else:
                        temp["data"]["default_gateway"] = ""
                temp["data"]["parent_type"] = "contrail_cluster"
                temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
                temp["data"]["node_refs"] = []
                serv_uuid = server_dict[ser]["server_uuid"]
                node_refs_dict = {}
                node_refs_dict["uuid"] = serv_uuid
                temp["data"]["node_refs"].append(node_refs_dict)
                resources_dict["resources"].append(temp)
	
	# Create Contrail Information (control, config, database, webui) part of the final Dictionary
	list_of_contrail_servers = []
	for ser in server_dict:
		if "contrail-control" in server_dict[ser]["roles"]:
			list_of_contrail_servers.append(ser)
	for ser in list_of_contrail_servers:
		# Create contrail_config_node dict
		temp = {}
		temp["kind"] = "contrail_config_node"
		temp["data"] = {}
		temp["data"]["parent_type"] = "contrail_cluster"
		temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
		temp["data"]["node_refs"] = []
		serv_uuid = server_dict[ser]["server_uuid"]
		node_refs_dict = {}
		node_refs_dict["uuid"] = serv_uuid
		temp["data"]["node_refs"].append(node_refs_dict)
		resources_dict["resources"].append(temp)
		# Create contrail_config_database_node dict
		temp = {}
                temp["kind"] = "contrail_config_database_node"
                temp["data"] = {}
                temp["data"]["parent_type"] = "contrail_cluster"
                temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
                temp["data"]["node_refs"] = []
                serv_uuid = server_dict[ser]["server_uuid"]
                node_refs_dict = {}
                node_refs_dict["uuid"] = serv_uuid
                temp["data"]["node_refs"].append(node_refs_dict)
                resources_dict["resources"].append(temp)
		# Create contrail_analytics_node dict
		temp = {}
                temp["kind"] = "contrail_analytics_node"
                temp["data"] = {}
                temp["data"]["parent_type"] = "contrail_cluster"
                temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
                temp["data"]["node_refs"] = []
                serv_uuid = server_dict[ser]["server_uuid"]
                node_refs_dict = {}
                node_refs_dict["uuid"] = serv_uuid
                temp["data"]["node_refs"].append(node_refs_dict)
                resources_dict["resources"].append(temp)
		# Create contrail_analytics_database_node dict
		temp = {}
                temp["kind"] = "contrail_analytics_database_node"
                temp["data"] = {}
                temp["data"]["parent_type"] = "contrail_cluster"
                temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
                temp["data"]["node_refs"] = []
                serv_uuid = server_dict[ser]["server_uuid"]
                node_refs_dict = {}
                node_refs_dict["uuid"] = serv_uuid
                temp["data"]["node_refs"].append(node_refs_dict)
                resources_dict["resources"].append(temp)
		# Create contrail_control_node dict
		temp = {}
                temp["kind"] = "contrail_control_node"
                temp["data"] = {}
                temp["data"]["parent_type"] = "contrail_cluster"
                temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
                temp["data"]["node_refs"] = []
                serv_uuid = server_dict[ser]["server_uuid"]
                node_refs_dict = {}
                node_refs_dict["uuid"] = serv_uuid
                temp["data"]["node_refs"].append(node_refs_dict)
                resources_dict["resources"].append(temp)
		# Create contrail_webui_node dict
		temp = {}
                temp["kind"] = "contrail_webui_node"
                temp["data"] = {}
                temp["data"]["parent_type"] = "contrail_cluster"
                temp["data"]["parent_uuid"] = cluster_details_dict["cluster_uuid"]
                temp["data"]["node_refs"] = []
                serv_uuid = server_dict[ser]["server_uuid"]
                node_refs_dict = {}
                node_refs_dict["uuid"] = serv_uuid
                temp["data"]["node_refs"].append(node_refs_dict)
                resources_dict["resources"].append(temp)
	
	resources_json = json.dumps(resources_dict)
	print resources_json
			

def get_x_auth_token():
	go_server_ip = go_server_dict["server_ip"]
	go_server_port = go_server_dict["server_port"]
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
	#print temp_token_last
	
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
	print final_token		

def add_servers():
        go_server_ip = go_server_dict["server_ip"]
        go_server_port = go_server_dict["server_port"]
        final_token="69c83200-314c-4d3d-a1c6-5e6065f45e2f"
        url = "'https://%s:%s/sync'" % (go_server_ip, go_server_port)
#        server_data=json_dumps_of_resources_dict
        a = subprocess.Popen(["curl %s -H 'Accept: */*' --compressed -H 'Connection: keep-alive' -H 'Content-Type: application/json' -H 'X-Requested-With: XMLHttpRequest' -H 'X-Auth-Token: %s' --data '%s' --insecure --include " % (url,final_token, sever_data)], stdout=subprocess.PIPE, shell=True).communicate()
        add_server_response = str(a)
        print add_server_response
   
def start_ansible_provisioning():
       go_server_ip = go_server_dict["server_ip"]
       go_server_port = go_server_dict["server_port"]
       final_token="69c83200-314c-4d3d-a1c6-5e6065f45e2f"
       url = "'https://%s:%s/sync'" % (go_server_ip, go_server_port)
#       provisioing_dict=resources_json
       a = subprocess.Popen(["curl %s -H 'Accept: */*' --compressed -H 'Connection: keep-alive' -H 'Content-Type: application/json' -H 'X-Requested-With: XMLHttpRequest' -H 'X-Auth-Token: %s' --data '%s' --insecure --include " % (url,final_token, prov_dict)], stdout=subprocess.PIPE, shell=True).communicate()
       result = str(a)
       print result

if __name__ == '__main__':
    globals()[sys.argv[2]]()



