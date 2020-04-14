import yaml
import sys
contrail_controller_ips = ""
openstack_ips = ""
control_node_ips = ""
with open("contrail_test_input.yaml") as f:
    list_doc = yaml.load(f)

for host, value in list_doc['instances'].items():
    with open("/home/stack/"+host) as h: 
        ips=h.read()
        ips = ips.split('\n')
        for ip in ips:
            if '10.0.0.' in ip:
                control_data_ip=ip
            if '10.1.0.' in ip:
                api_ip=ip

        value['ip'] = api_ip

        if 'compute' in host or 'dpdk' in host:
            value['ip'] = control_data_ip 

        for i in range(3):
            if ("overcloud-contrailcontroller-" + str(i)) == host:
                contrail_controller_ips = api_ip if not contrail_controller_ips else contrail_controller_ips + ',' + api_ip
                control_node_ips = control_data_ip if not control_node_ips else control_node_ips + ',' + control_data_ip 
        for i in range(3):
            if ("overcloud-controller-" + str(i)) == host:
                openstack_ips = api_ip if not openstack_ips else openstack_ips + ',' + api_ip

with open("/home/stack/server_list") as h: 
    hosts=h.read()

hosts=hosts.split('\n')
for host in hosts: 
    host_s = host.split(' ') 
    if 'overcloud-contrailcontroller-0' in host_s:
        for item in host_s:
            if '192.168.24' in item:
                cfgm0_ip = item 
                list_doc['orchestrator_configuration']['contrail_api_interface_address'] = item
        break

if sys.argv[1] == 'kernel':       
    with open("/home/stack/server_list") as h:
        hosts=h.read()

    hosts=hosts.split('\n')
    for host in hosts:
        host_s = host.split(' ')
        if 'overcloud-novacompute-0' in host_s:
            for item in host_s:
                if '192.168.24' in item:
                    cmpt0_ip = item
            break

    with open("/home/stack/server_list") as h:
        hosts=h.read()

    hosts=hosts.split('\n')
    for host in hosts:
        host_s = host.split(' ')
        if 'overcloud-novacompute-1' in host_s:
            for item in host_s:
                if '192.168.24' in item:
                    cmpt1_ip = item
            break

if sys.argv[1] == 'dpdk':     
    with open("/home/stack/server_list") as h:
        hosts=h.read()

    hosts=hosts.split('\n')
    for host in hosts:
        host_s = host.split(' ')
        if 'overcloud-contraildpdk-0' in host_s:
            for item in host_s:
                if '192.168.24' in item:
                    cmpt0_ip = item
            break

    with open("/home/stack/server_list") as h:
        hosts=h.read()

    hosts=hosts.split('\n')
    for host in hosts:
        host_s = host.split(' ')
        if 'overcloud-contraildpdk-1' in host_s:
            for item in host_s:
                if '192.168.24' in item:
                    cmpt1_ip = item
            break

list_doc['test_configuration']['cfgm0_host_string'] = "heat-admin@" + cfgm0_ip
list_doc['test_configuration']['cmpt0_host_string'] = "heat-admin@" + cmpt0_ip
list_doc['test_configuration']['cmpt1_host_string'] = "heat-admin@" + cmpt1_ip
list_doc['contrail_configuration']['CONTROLLER_NODES'] = contrail_controller_ips 
list_doc['contrail_configuration']['CONTROL_NODES'] = control_node_ips 
list_doc['contrail_configuration']['OPENSTACK_NODES'] = openstack_ips 

with open("/home/stack/keystone") as h:
    keystone=h.read()

    passwd=keystone.split('\n')[0]
    ip1=keystone.split('\n')[1].split(':')[0].split(' ')[-1]
    ip2=keystone.split('\n')[2].split(':')[0].split(' ')[-1]

    ext_vip = ip1 if '10.2.0.' in ip1 else ip2
    int_vip = ip1 if '10.1.0.' in ip1 else ip2

list_doc['contrail_configuration']['KEYSTONE_AUTH_ADMIN_PASSWORD'] = passwd 
list_doc['contrail_configuration']['KEYSTONE_AUTH_HOST'] = ext_vip 
list_doc['orchestrator_configuration']['external_vip'] = ext_vip 
list_doc['orchestrator_configuration']['internal_vip'] = int_vip 
list_doc['orchestrator_configuration']['keystone']['password'] = passwd 
list_doc['test_configuration']['stack_password'] = passwd

with open("contrail_test_input.yaml", "w") as f:
    yaml.dump(list_doc, f)
