#!/usr/bin/env bash
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

openstack role add --project $1 --user $OS_USERNAME admin
export OS_TENANT_NAME=$1

sed -i 's/project_uuid_val/'${dashed_project_uuid}'/' /root/$1/input.json
echo "input.json  --- Changed"

python /root/$1/change_testbed_params.py /root/$1/input.json $ubuntu_image_name parse_openstack_image_list_command
python /root/$1/inp_to_yaml.py /root/$1/input.json check_and_create_required_flavor
python /root/$1/change_testbed_params.py /root/$1/input.json vRE_18_1 get_vmx_images
python /root/$1/change_testbed_params.py /root/$1/input.json vPFE_18_1 get_vmx_images
sleep 5
sed -i 's/image_val/'${ubuntu_image_name}'/' /root/$1/input.json
fip_uuid="$(python change_testbed_params.py input.json $selected_config_node_ip get_fip_uuid)"
project_hash="$(python change_testbed_params.py input.json $1 get_project_hash )"
sed -i 's/_project_hash_/'${project_hash}'/' input.json
sed -i 's/fip_uuid/'${fip_uuid}'/' input.json
echo "input.json  --- Changed"
echo "\n The Input.json looks something like this now"
cat /root/$1/input.json

#mkdir /root/$dashed_project_uuid
python /root/$1/inp_to_yaml.py /root/$1/input.json check_and_create_required_flavor
python /root/$1/inp_to_yaml.py /root/$1/input.json create_network_yaml > /root/$1/final_network.yaml
python /root/$1/inp_to_yaml.py /root/$1/input.json create_server_yaml > /root/$1/final_server.yaml
echo " The Server and Network YAML files are now created at location '/root/$dashed_project_uuid'"

network_stack='test_network_final'
final_network_stack_name=$network_stack$dashed_project_uuid
echo "Network Stack Name: $final_network_stack_name"
echo $final_network_stack_name >> /root/$1/info.txt
server_stack_name='test_server_final'
final_server_stack_name=$server_stack_name$dashed_project_uuid
echo "Server Stack Name: $final_server_stack_name"
echo $final_server_stack_name >> /root/$1/info.txt
vmx_stack_name='test_vmx_final'
final_vmx_stack_name=$vmx_stack_name$dashed_project_uuid
echo $final_vmx_stack_name
echo $final_vmx_stack_name >> /root/$1/info.txt

#rm /root/.ssh/known_hosts
# Lets create the Network Stack
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
	heat stack-create -f /root/$1/final_server.yaml $final_server_stack_name
        sleep 20
        while true
        do
	python /root/$1/change_testbed_params.py /root/$1/input.json $final_server_stack_name get_stack_status > /root/$1/tmp.txt
        chmod 777 /root/$1/tmp.txt
        ser_res="$(cat /root/$1//tmp.txt)"
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
		#public_network_uuid="$(python /root/$1/change_testbed_params.py /root/$1/input.json $selected_config_node_ip get_fip_uuid)"
		sed -i 's/__public_network_uuid__/'${fip_uuid}'/' /root/$1/VMX_Bundle_Automation/vmx_contrail.env
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
        contrail_version="$(echo $VERSION)"
        sed -i 's/__VERSION__/'${contrail_version}'/' /root/$1/input.json
        deployer="$(python /root/$1/inp_to_yaml.py /root/$1/input.json get_deployer)"
	python /root/$1/inp_to_yaml.py /root/$1/input.json create_yaml_file_for_5_0_provisioning  > /root/$1/all.yml
	echo "Yaml with all the provision and test parameters is created and named as all.yml"
	sed -i 's/__VERSION__/'${contrail_version}'/' /root/$1/all.yml
	if [ -n "$BRANCH" ]; then
	    contrail_branch="$(echo $BRANCH)"
	    sed -i 's/__BRANCH__/'${contrail_branch}'/' /root/$1/all.yml
	else
	    sed -i 's/__BRANCH__/master/' /root/$1/all.yml
	fi
        echo "The All.yml which will be used for running sanity and provisioning looks something like this:\n"
        cat /root/$1/all.yml
        if [[ $deployer == *"contrail_command"* ]]; then
            config_node_ip=$(python /root/$1/fabric_cluster_bringup_automation/fabric_cluster_bringup.py /root/$1/input.json get_contrail_command_node_ip)
        else
            python /root/$1/inp_to_yaml.py /root/$1/input.json get_config_node_ip > /root/$1/config_node_ip
            config_node_ip="$(cat /root/$1/config_node_ip)"
        fi
    echo "Adding sleep of 300 seconds as WA for node not being reachable during provision - will remove this as part of cleanup"
    sleep 300
	((count=60))
	while [[ $count -ne 0 ]] ; do
            sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$config_node_ip 'uname -a'
            rc=$?
            if [[ $rc -eq 0 ]]; then
                break
            fi
            echo "The Config Node, $config_node_ip is not yet reachable"
	    ((count = count - 1))
            sleep 5
	done
	if [[ $count -eq 0 ]]
	then
	    echo "The Config Node $config_node_ip is Not reachable"
            exit 1
	else
	    echo "The config node ip where the ansible repo is going to cloned is: "$config_node_ip
	    sshpass -p c0ntrail123 scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r /root/$1/ansible root@$config_node_ip:/root/ansible
            OS_INFO=`sshpass -p 'c0ntrail123' ssh -o 'StrictHostKeyChecking no' -o 'UserKnownHostsFile /dev/null' root@$config_node_ip 'cat /etc/*elease | grep "PRETTY_NAME"'`
            if ([[ $OS_INFO == *"CentOS"* ]] && [[ $deployer == *'contrail_command'* ]]); then
                sshpass -p c0ntrail123 scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r /root/$1/fabric_cluster_bringup_automation root@$config_node_ip:/root/fabric_cluster_bringup_automation
                sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$config_node_ip "cd /root/fabric_cluster_bringup_automation ; ./install_contrail_command.sh $config_node_ip $contrail_version"
                sleep 10
                final_token=$(python /root/$1/fabric_cluster_bringup_automation/fabric_cluster_bringup.py /root/$1/input.json get_x_auth_token $config_node_ip)
                echo "Final token generated : $final_token"
                sleep 10
                resp=$(python /root/$1/fabric_cluster_bringup_automation/fabric_cluster_bringup.py /root/$1/input.json add_servers $config_node_ip $final_token)
                if [ "$resp" == 'Passed' ]
                then
                    echo "Sucessfully added servers .. "
                else 
                    echo $resp; exit         
                fi
                sleep 15
                prov_resp=$(python /root/$1/fabric_cluster_bringup_automation/fabric_cluster_bringup.py /root/$1/input.json start_ansible_provisioning $config_node_ip $final_token)
                if [ "$prov_resp" == 'Passed' ]
                then
                    echo "Started provisioning via contrail command .. "
                else
                    echo $prov_resp; exit
                fi
                status_resp="NO_STATE"
                while [ "$status_resp" != 'CREATED' ]; do
                    status_resp=$(python /root/$1/fabric_cluster_bringup_automation/fabric_cluster_bringup.py /root/$1/input.json get_provisioning_status $config_node_ip $final_token)
                    echo $status_resp 
                    sleep 120
                done
                if [ "$status_resp" == 'CREATED' ]
                then
                    echo "Provisioning completed successfully via contrail command .. "
                else
                    echo "Provisioning Failed"; exit
                fi
                sshpass -p c0ntrail123 scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /root/$1/all.yml root@$config_node_ip:/root/ansible/inventory/group_vars/
                sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$config_node_ip 'cd /root/ansible/ ; ansible-playbook -i inventory/ playbooks/run_sanity.yml'
            elif ([[ $OS_INFO == *"CentOS"* ]] && [[ $deployer == None ]]); then
	              sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$config_node_ip 'yum install -y git ansible-2.4.2.0 epel-release vim'
	              sshpass -p c0ntrail123 scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /root/$1/all.yml root@$config_node_ip:/root/ansible/inventory/group_vars/
	              sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$config_node_ip 'cd /root/ansible/ ; ansible-playbook -i inventory/ playbooks/all.yml'
            elif [[ $OS_INFO == *"OpenShift"* ]]; then
                sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$config_node_ip 'yum update -y && yum install -y sshpass git python-pip epel-release vim && pip install ansible==2.5.2'
                sshpass -p c0ntrail123 scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /root/$1/all.yml root@$config_node_ip:/root/ansible/inventory/group_vars/
                sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$config_node_ip 'cd /root/ansible/ ; ansible-playbook -i inventory/ playbooks/all.yml'
            elif [[ $OS_INFO == *"Ubuntu"* ]]; then
                sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$config_node_ip 'apt-get clean && apt-get update && apt-get install -y software-properties-common && apt-add-repository -y ppa:ansible/ansible && apt-get update && apt-get install -y sshpass git python-pip python-minimal python-apt && pip install ansible'
                sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$config_node_ip 'pip install junos-eznc jxmlease && ansible-galaxy install Juniper.junos'
                sshpass -p c0ntrail123 scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /root/$1/all.yml root@$config_node_ip:/root/ansible/inventory/group_vars/
	        sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$config_node_ip 'cd /root/ansible/ ; ansible-playbook -i inventory/ playbooks/all.yml -e 'ansible_python_interpreter=/usr/bin/python3' -v '
            fi
	fi
else
        echo "Network Stack Creation failed. So creation of the SERVER STACK is TERMINATED !!!!"
fi
echo "Cloning the contrail-deployments repo and transferring the all.yaml file generated above."
echo "DONE !!!!!!!!!!!!"

