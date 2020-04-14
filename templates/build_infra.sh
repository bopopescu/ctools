source /etc/contrail/openstackrc 
echo $1 >> /root/$1/info.txt
a="$(openstack project create $1 -f json > /root/$1/uuid.json)"
openstack_project_uuid=$(python -c 'import json; fd=json.loads(open("/root/'$1'/uuid.json").read()); print fd["id"]')
dashed_project_uuid=$(python -c 'import uuid; fd=uuid.UUID("'${openstack_project_uuid}'"); print fd')
echo $dashed_project_uuid
ubuntu_image_name=$2
selected_config_node_ip=$3
sleep 5
echo "The Contents of the input.json file before modification "
cat /root/$1/input.json

sed -i 's/project_uuid_val/'${dashed_project_uuid}'/' /root/$1/input.json
python /root/$1/change_testbed_params.py /root/$1/input.json $ubuntu_image_name parse_openstack_image_list_command
#python /root/$1/change_testbed_params.py /root/$1/input.json vRE_17 get_vmx_images
#python /root/$1/change_testbed_params.py /root/$1/input.json vPFE_17 get_vmx_images
python /root/$1/change_testbed_params.py /root/$1/input.json vRE_18_1 get_vmx_images
python /root/$1/change_testbed_params.py /root/$1/input.json vPFE_18_1 get_vmx_images
sleep 5

sed -i 's/image_val/'${ubuntu_image_name}'/' /root/$1/input.json
fip_uuid="$(python /root/$1/change_testbed_params.py /root/$1/input.json $selected_config_node_ip get_fip_uuid)"
echo "The FIP Networm UUID for this project is: $fip_uuid"
sed -i 's/fip_uuid/'${fip_uuid}'/' /root/$1/input.json
echo "/root/$1/input.json  --- Changed"
echo "The New imput.json :- \n"
cat /root/$1/input.json

echo "Change Premissions on cloud_init.sh file"
chmod 777 /root/$1/cloud_init.sh

echo "Lets See if the Server Manager OS is already added to openstack"
python /root/$1/inp_to_yaml.py /root/$1/input.json add_sm_os_to_openstack
echo "Server Manager OS added"

#Adding the recommended flavor for the VM on the base cluster
python /root/$1/inp_to_yaml.py /root/$1/input.json check_and_create_required_flavor 
python /root/$1/inp_to_yaml.py /root/$1/input.json create_network_yaml > /root/$1/final_network.yaml
python /root/$1/inp_to_yaml.py /root/$1/input.json create_server_yaml > /root/$1/final_server.yaml
#python /root/$1/inp_to_yaml.py /root/$1/input.json produce_vmx_env_file > /root/$1/vin17.env
echo " The Servere and Network YAML files are now created at location '/root/$1'"

project_uuid=$(python -c 'import json; fd=json.loads(open("/root/'$1'/input.json").read()); print fd["inp_params"]["params"]["project_uuid"]')
network_stack='test_network_final'
final_network_stack_name=$network_stack$project_uuid
echo $final_network_stack_name
echo $final_network_stack_name >> /root/$1/info.txt
server_stack_name='test_server_final'
final_server_stack_name=$server_stack_name$project_uuid
echo $final_server_stack_name
echo $final_server_stack_name >> /root/$1/info.txt
vmx_stack_name='test_vmx_final'
final_vmx_stack_name=$vmx_stack_name$project_uuid
echo $final_vmx_stack_name
echo $final_vmx_stack_name >> /root/$1/info.txt

#Lets Create the Network Stack
heat stack-create -f /root/$1/final_network.yaml $final_network_stack_name
sleep 10
while true
do
python /root/$1/change_testbed_params.py /root/$1/input.json $final_network_stack_name get_stack_status > /root/$1/tmp.txt
chmod 777 /root/$1/tmp.txt
net_res="$(cat /root/$1/tmp.txt)"
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
                echo "Network Stack creation still in progress. Waiting for 20 more seconds"
                heat stack-list | grep $final_network_stack_name
                sleep 20
        fi
else
        echo "Network Stack Creation: get_stack_status function in change_testbed_params.py file did not return any thing"
        break
fi
done


if [ "$net_res" == 'success' ]
then
	heat stack-create -f /root/$1/final_server.yaml $final_server_stack_name
	sleep 20
        while true
        do
	python /root/$1/change_testbed_params.py /root/$1/input.json $final_server_stack_name get_stack_status > /root/$1/tmp.txt
        chmod 777 /root/$1/tmp.txt
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
                        echo "Server Stack Still in progress. Waiting for 30 more seconds"
                        heat stack-list | grep $final_server_stack_name
                        sleep 30
                fi
        else
                echo "Server Stack Creation: get_stack_status function in change_testbed_params.py file did not return any thing"
                break
        fi
        done
	vmx_dec="$(python /root/$1/inp_to_yaml.py /root/$1/input.json is_vmx_true)"
	if [ "$vmx_dec" == 'true' ]
	then
		sshpass -p "c0ntrail123" scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r root@10.84.24.64:/cs-shared/soumilk/remote_compute/Remote_compute_Automation/new_topology-try-2017-12-11/New_working_VMX/Tanvir_VMX/VMX_Bundle_Automation .
		mv VMX_Bundle_Automation /root/$1/
		sed -i 's/_project_name_/'$1'/' /root/$1/VMX_Bundle_Automation/vmx_contrail.env
		fixed_n_name='final_test_network_1_'$dashed_project_uuid
		sed -i 's/fixed_network_name/'${fixed_n_name}'/' /root/$1/VMX_Bundle_Automation/vmx_contrail.env
		var_n_name='final_test_network_2_'$dashed_project_uuid
		sed -i 's/variable_network_name/'${var_n_name}'/' /root/$1/VMX_Bundle_Automation/vmx_contrail.env
		gateway_ip="$(python /root/$1/change_testbed_params.py /root/$1/input.json $selected_config_node_ip get_gateway_ip)"
		sed -i 's/__gateway_ip__/'${gateway_ip}'/' /root/$1/VMX_Bundle_Automation/vmx_contrail.env	
		echo "vMX Stack Name: $final_vmx_stack_name"
		heat stack-create -f /root/$1/VMX_Bundle_Automation/vmx_contrail.yaml -e /root/$1/VMX_Bundle_Automation/vmx_contrail.env  $final_vmx_stack_name
		sleep 20
		while true
		do
			python /root/$1/change_testbed_params.py /root/$1/input.json $final_vmx_stack_name get_stack_status > /root/$1/tmp.txt
			chmod 777 /root/$1/tmp.txt
			vmx_res="$(cat /root/$1/tmp.txt)"
			if [ "$vmx_res" == 'success' ] || [ "$vmx_res" == 'failed' ] || [ "$vmx_res" == 'inprogress' ];
			then
				if [ "$vmx_res" == 'success' ]
				then
					echo "VMX Stack Created Successfully"
					break
				fi
				if [ "$vmx_res" == 'failed' ]
				then
					echo "VMX Stack Creation Failed"
				fi
				if [ "$vmx_res" == 'inprogress' ]
				then
					echo "VMX Stack Creation still in progress. Waiting for 30 more seconds"
					heat stack-list | grep $final_vmx_stack_name
					sleep 30
				fi
			else
				echo "VMX Stack Creation: get_stack_status function in change_testbed_params.py file did not return any thing"
				break
		fi
		done
	else
		echo "Not creating VMX Stack "
	fi
		
	echo " Final List of all Heat Stacks "
	heat stack-list 
	python /root/$1/inp_to_yaml.py /root/$1/input.json create_cluster_json > /root/$1/cluster.json
	echo "cluster.json now Created"
	python /root/$1/inp_to_yaml.py /root/$1/input.json create_server_json > /root/$1/server.json
	echo "server.json now Created"
	python /root/$1/inp_to_yaml.py /root/$1/input.json get_sm_ip > /root/$1/server-manager-file
	echo "server-manager-file now created that conatins server manager IP"
	python /root/$1/inp_to_yaml.py /root/$1/input.json get_config_node_ip > /root/$1/config-node-ip
	echo "config-node-ip file now created that contains config node IP"
	python /root/$1/inp_to_yaml.py /root/$1/input.json create_testbedpy_file > /root/$1/testbed.py
	echo "Testbed.py file created that will be used for running the tests on the overlay cluster"
	echo " -----   DONE  -----"

else
        echo "Network Stack Creation failed. So creation of the SERVER STACK is TERMINATED !!!!"
fi


