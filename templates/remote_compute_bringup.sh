#Author: Soumil Kulkarni 
#Usage: ./remote_compute_bringup.sh <New Project Name> <os for vm> <IP of base cluster config node> 
#Example: ./remote_compute_bringup.sh RC_Project_1 ubuntu-14-04 10.87.66.138

source /etc/contrail/openstackrc
echo "The New Project Name is : " $1
echo "The Required OS for the Virtual Machines is :" $2
echo "Ip Address of the config node of the base cluster : " $3
os_name=$2
selected_config_node_ip=$3
a="$(openstack project create $1 -f json > /root/$1/uuid.json)"
openstack_project_uuid=$(python -c 'import json; fd=json.loads(open("uuid.json").read()); print fd["id"]')
dashed_project_uuid=$(python -c 'import uuid; fd=uuid.UUID("'${openstack_project_uuid}'"); print fd')
echo "Dashed UUID of the newly created Project is : " $dashed_project_uuid
rm /root/$1/uuid.json
keystone user-role-add --user admin --role admin --tenant $1

sed -i 's/project_uuid_val/'${dashed_project_uuid}'/' /root/$1/input.json
python /root/$1/change_testbed_params.py /root/$1/input.json $os_name parse_openstack_image_list_command
#python change_testbed_params.py template_Remote_Compute vRE_18_1 get_vmx_images
#python change_testbed_params.py template_Remote_Compute vPFE_18_1 get_vmx_images
python /root/$1/inp_to_yaml.py /root/$1/input.json check_and_create_required_flavor

#sed -i 's/image_val/'${os_name}'/' template_Remote_Compute
fip_uuid="$(python change_testbed_params.py /root/$1/input.json $selected_config_node_ip get_fip_uuid)"
sed -i 's/fip_uuid/'${fip_uuid}'/' /root/$1/input.json
#sed -i 's/fip_uuid/'${fip_uuid_val}'/' root/$1/Remote_Compute_Temp_Files/network.yaml
sed -i 's/project_uuid_val/'${dashed_project_uuid}'/' /root/$1/Remote_Compute_Temp_Files/network.yaml
sed -i 's/project_uuid_val/'${dashed_project_uuid}'/' /root/$1/Remote_Compute_Temp_Files/server.yaml
sed -i 's/fip_uuid_val/'${fip_uuid}'/' /root/$1/Remote_Compute_Temp_Files/server.yaml
#sed -i 's/project_name/'${1}'/' /root/$1/Remote_Compute_Temp_Files/network.yaml
#python inp_to_yaml.py template_Remote_Compute create_network_yaml > network.yaml
#python inp_to_yaml.py template_Remote_Compute create_server_yaml > server.yaml 

#sed -i 's/dashed_project_uuid/'${dashed_project_uuid}'/' network.yaml
#sed -i 's/dashed_project_uuid/'${dashed_project_uuid}'/' server.yaml

network_stack='remote_compute_network_stack'
final_network_stack_name=$network_stack$dashed_project_uuid
echo "Network Stack Name : " $final_network_stack_name
server_stack='remote_compute_server_stack'
final_server_stack_name=$server_stack$dashed_project_uuid
echo "Server Stack Name : " $final_server_stack_name


heat stack-create -f /root/$1/Remote_Compute_Temp_Files/network.yaml $final_network_stack_name
sleep 3
while true
do
#python helper_functions.py $final_network_stack_name get_stack_status > tmp.txt
python /root/$1/change_testbed_params.py /root/$1/input.json $final_network_stack_name get_stack_status >  /root/$1/tmp.txt
chmod 777 tmp.txt
net_res="$(cat /root/$1/tmp.txt)"
#echo net_res
if [ "$net_res" == 'success' ] || [ "$net_res" == 'failed' ] || [ "$net_res" == 'inprogress' ];
then
        if [ "$net_res" == 'success' ]
        then
                echo "Network Stack Created Successfully"
                break
        fi
        if [ "$net_res" == 'failed' ]
        then
                echo "Network Stack Creation Failed "
                break
        fi
        if [ "$net_res" == 'inprogress' ]
        then
                echo "Network Stack creation still in progress. Waiting for 5 more seconds"
                heat stack-list | grep $final_network_stack_name
                sleep 5
        fi
else
        echo "Network Stack Creation: get_stack_status function in helper_functions.py file did not return any thing"
        break
fi
done
rm tmp.txt

if [ "$net_res" == 'success' ]
then
        heat stack-create -f /root/$1/Remote_Compute_Temp_Files/server.yaml $final_server_stack_name
        sleep 10
        while true
        do
	#python helper_functions.py $final_server_stack_name get_stack_status > tmp.txt
	python /root/$1/change_testbed_params.py /root/$1/input.json $final_server_stack_name get_stack_status > /root/$1/tmp.txt
	ser_res="$(cat /root/$1/tmp.txt)"	
	if [ "$ser_res" == 'success' ] || [ "$ser_res" == 'failed' ] || [ "$ser_res" == 'inprogress' ];
        then
                if [ "$ser_res" == 'success' ]
                then
                        echo "Server Stack Created Successfully"
                        break
                fi
                if [ "$ser_res" == 'failed' ]
                then
                        echo "Server Stack Creation Failed"
                        heat stack-show $final_server_stack_name
                        exit 0
                fi
                if [ "$ser_res" == 'inprogress' ]
                then
                        echo "Server Stack Still in progress. Waiting for 20 more seconds"
                        heat stack-list | grep $final_server_stack_name
                        sleep 20
                fi
        else
                echo "Server Stack Creation: get_stack_status function in helper_functions.py file did not return any thing"
                break
        fi
        done
	echo "Final Server Stacks are "
	heat stack-list | grep $dashed_project_uuid
	sleep 90
	python /root/$1/inp_to_yaml.py /root/$1/input.json get_openstack_node_ip > /root/$1/openstack_node_ip
	openstack_node_ip="$(cat /root/$1/openstack_node_ip)"
	python /root/$1/inp_to_yaml.py /root/$1/input.json create_static_routes_for_remote_compute_nodes
	sleep 90
	echo "The Openstack Node where Contrail-ansible-deployer would run is: \n\n"$openstack_node_ip
	sshpass -p c0ntrail123 scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /root/$1/Remote_Compute_Temp_Files/instances.yaml root@$openstack_node_ip:/root/
	sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$openstack_node_ip 'yum -y install epel-release; yum -y install git ansible vim; cd; git clone http://github.com/Juniper/contrail-ansible-deployer; rm -f /root/contrail-ansible-deployer/config/instances.yaml; cp /root/instances.yaml /root/contrail-ansible-deployer/config/; cd /root/contrail-ansible-deployer; ansible-playbook -i inventory/ playbooks/configure_instances.yml; ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/install_contrail.yml; yum install -y gcc python-devel; pip install python-openstackclient; pip install python-ironicclient' 		
else
        echo "Network Stack Creation failed. So creation of the SERVER STACK is TERMINATED !!!!"
fi
echo "Done ----"s
