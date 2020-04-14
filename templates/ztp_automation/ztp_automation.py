"""
Author: Soumil Kulkarni
File Name: ztp_automation.py
Summary: All the helper functions for automation of the ZTP prcess
Date: Wed Oct 24, 2018
"""
import sys
import json
import paramiko
import subprocess

inp_file = sys.argv[1]
with open(inp_file, 'rw') as json_data:
    parsed_json = json.load(json_data)

#print parsed_json
"""
a = subprocess.Popen('ifconfig -a | grep 90:e2:ba:c2:f8:80', shell=True, stdout=subprocess.PIPE)
a_tmp = a.stdout.read()
print str(a_tmp)
a_list =  a_tmp.split(" ")
print a_list[0]
"""

def get_interface_name_to_attach_to_bridge():
    a = subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE)
    a_tmp = a.stdout.read()
    hostname = str(a_tmp)
    hostname = hostname.replace('\n', '')
    ret_dict = {hostname: {}}
    for i in parsed_json['baremetal_details']:
        if parsed_json['baremetal_details'][i]['name'] == hostname:
            for j in parsed_json['baremetal_details'][i]['bridge_interface']:
                mac_attached_to_br = parsed_json['baremetal_details'][i]['bridge_interface'][j]['mac_attached_to']
                a = subprocess.Popen('ifconfig -a | grep %s' %mac_attached_to_br , shell=True, stdout=subprocess.PIPE)
                a_tmp = a.stdout.read()
                a_list =  a_tmp.split(" ")
                interface_name = a_list[0]
		ret_dict[hostname][j] =  interface_name
                #parsed_json['baremetal_details'][i]['bridge_interface'][j]['interface_attached_to'] = interface_name
    return ret_dict

def get_hostname_of_bms():
    a = subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE)
    a_tmp = a.stdout.read()
    #print "Hostname of the selected BMS is : %s" %str(a_tmp)
    return str(a_tmp)

def create_bridge_interfaces():
    interface_bridge_mapping = get_interface_name_to_attach_to_bridge()
    hostname_of_curr_bms = get_hostname_of_bms().strip()
    main_str = ""
    for i in parsed_json['baremetal_details']:
        if parsed_json['baremetal_details'][i]['name'] == hostname_of_curr_bms:
            for j in parsed_json['baremetal_details'][i]['bridge_interface']:
                br_name = parsed_json['baremetal_details'][i]['bridge_interface'][j]['name']
                #br_interface_attached_to = parsed_json['baremetal_details'][
                #    i]['bridge_interface'][j]['interface_attached_to']
                br_interface_attached_to = interface_bridge_mapping[hostname_of_curr_bms][j]
                br_interface_address = parsed_json['baremetal_details'][i]['bridge_interface'][j]['ip']
                br_interface_netmask = parsed_json['baremetal_details'][i]['bridge_interface'][j]['netmask']
                str1 = """
auto %s
iface %s inet static
  bridge_ports   %s
  address %s
  netmask  %s

					""" % (br_name, br_name, br_interface_attached_to, br_interface_address, br_interface_netmask)
                main_str += str1
                #a = subprocess.Popen('echo %s >> /etc/network/interfaces' % str1, shell=True, stdout=subprocess.PIPE)
                #a_tmp = a.stdout.read()
                #print "%s config added to /etc/network/interfaces file" %br_name
    print main_str


if __name__ == '__main__':
    globals()[sys.argv[2]]()
