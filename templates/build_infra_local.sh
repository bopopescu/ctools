source /etc/contrail/openstackrc 
echo $1 >> info.txt
a="$(openstack project create $1 -f json > uuid.json)"
openstack_project_uuid=$(python -c 'import json; fd=json.loads(open("uuid.json").read()); print fd["id"]')
dashed_project_uuid=$(python -c 'import uuid; fd=uuid.UUID("'${openstack_project_uuid}'"); print fd')
echo $dashed_project_uuid
ubuntu_image_name=$2
sleep 5
echo "The Contents of the input.json file before modification "
cat input.json

sed -i 's/project_uuid_val/'${dashed_project_uuid}'/' input.json
echo "input.json  --- Changed"

python change_testbed_params.py input.json $ubuntu_image_name parse_openstack_image_list_command
python change_testbed_params.py input.json vRE_17 get_vmx_images
python change_testbed_params.py input.json vPFE_17 get_vmx_images
sleep 5
sed -i 's/image_val/'${ubuntu_image_name}'/' input.json
echo "input.json  --- Changed"
echo "\n The Input.json looks something like this now"
cat input.json

mkdir /root/$dashed_project_uuid
python inp_to_yaml.py input.json check_and_create_required_flavor
python inp_to_yaml.py input.json create_network_yaml > /root/$dashed_project_uuid/final_network.yaml
python inp_to_yaml.py input.json create_server_yaml > /root/$dashed_project_uuid/final_server.yaml
python inp_to_yaml.py input.json produce_vmx_env_file > /root/$dashed_project_uuid/vin17.env
echo " The Servere and Network YAML files are now created at location '/root/$dashed_project_uuid'"

#wget http://10.84.5.120/images/soumilk/vm_images/vmx_files/vmx_compress.tar.gz
#cp vmx_compress.tar.gz /root/$dashed_project_uuid/
#rm vmx_compress.tar.gz
#tar -xvf /root/$dashed_project_uuid/vmx_compress.tar.gz -C /root/$dashed_project_uuid/

project_uuid=$(python -c 'import json; fd=json.loads(open("input.json").read()); print fd["inp_params"]["params"]["project_uuid"]')
network_stack='test_network_final'
final_network_stack_name=$network_stack$project_uuid
echo "Network Stack Name: $final_network_stack_name"
echo $final_network_stack_name >> info.txt
server_stack_name='test_server_final'
final_server_stack_name=$server_stack_name$project_uuid
echo "Server Stack Name: $final_server_stack_name"
echo $final_server_stack_name >> info.txt
vmx_stack_name='test_vmx_final'
final_vmx_stack_name=$vmx_stack_name$project_uuid
#echo $final_vmx_stack_name


# Lets create the Network Stack
heat stack-create -f /root/$dashed_project_uuid/final_network.yaml $final_network_stack_name
sleep 10
while true
do
python change_testbed_params.py input.json $final_network_stack_name get_stack_status > /root/$dashed_project_uuid/tmp.txt
chmod 777 /root/$dashed_project_uuid/tmp.txt
net_res="$(cat /root/$dashed_project_uuid/tmp.txt)"
if [ "$net_res" == 'success' ] || [ "$net_res" == 'failed' ] || [ "$net_res" == 'inprogress' ];
then
        if [ "$net_res" == 'success' ]
        then
                echo " Network Stack Created Successfully"
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
	heat stack-create -f /root/$dashed_project_uuid/final_server.yaml $final_server_stack_name
        sleep 20
        while true
        do
	python change_testbed_params.py input.json $final_server_stack_name get_stack_status > /root/$dashed_project_uuid/tmp.txt
        chmod 777 /root/$dashed_project_uuid/tmp.txt
        ser_res="$(cat /root/$dashed_project_uuid/tmp.txt)"
	if [ "$ser_res" == 'success' ] || [ "$ser_res" == 'failed' ] || [ "$ser_res" == 'inprogress' ];
        then
                #echo $final_server_stack_name
                #echo "$ser_res"
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
	vmx_dec="$(python inp_to_yaml.py input.json is_vmx_true)"
	if [ "$vmx_dec" == 'true' ]
	then
		wget http://10.84.5.120/images/soumilk/vm_images/vmx_files/vmx_compress.tar.gz
        	cp vmx_compress.tar.gz /root/$dashed_project_uuid/
        	rm vmx_compress.tar.gz
        	tar -xvf /root/$dashed_project_uuid/vmx_compress.tar.gz -C /root/$dashed_project_uuid/
		echo "vMX Stack Name: $final_vmx_stack_name"
		heat stack-create -f /root/$dashed_project_uuid/vmx_contrail.yaml -e /root/$dashed_project_uuid/vin17.env $final_vmx_stack_name
		sleep 20
		while true
		do 	
			python change_testbed_params.py input.json $final_vmx_stack_name get_stack_status > /root/$dashed_project_uuid/tmp.txt
			chmod 777 /root/$dashed_project_uuid/tmp.txt
			vmx_res="$(cat /root/$dashed_project_uuid/tmp.txt)"
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
	python inp_to_yaml.py input.json create_cluster_json > /root/$dashed_project_uuid/cluster.json
	echo "Cluster.json created "
	python inp_to_yaml.py input.json create_server_json > /root/$dashed_project_uuid/server.json
	echo "server.json created "
	python inp_to_yaml.py input.json get_sm_ip > /root/$dashed_project_uuid/server-manager-file
	echo "server-manager-ip file created that contains the server-manager ip"
	python inp_to_yaml.py input.json get_config_node_ip > /root/$dashed_project_uuid/config-node-ip
	echo "config-node-ip file created that contains the config node ip"
	python inp_to_yaml.py input.json create_testbedpy_file > /root/$dashed_project_uuid/testbed.py
	echo "Testbed.py created "
else
        echo "Network Stack Creation failed. So creation of the SERVER STACK is TERMINATED !!!!"
fi

#vmx_dec="$(python inp_to_yaml.py input.json is_vmx_true)"
#if [ "$vmx_dec" == 'true' ]
#then	
#	heat stack-create -f /root/$dashed_project_uuid/vmx_contrail.yaml -e /root/$dashed_project_uuid/vin17.env $final_vmx_stack_name
#else
#	echo "Not creating VMX Stack "
#fi

echo "---------   DONE   ---------"
