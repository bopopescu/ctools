#!/usr/bin/bash

UNDERCLOUD_STACK_USER=stack
UNDERCLOUD_STACK_HOME=/home/stack
UNDERCLOUD_PASSWORD=contrail123
UNDERCLOUD_IP=$1
VERSION=$2

sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP "(
sed -i '/  ContrailImageTag: /a \  ContrailImageTag: $VERSION' tripleo-heat-templates/environments/contrail/contrail-services.yaml
sed -i '0,/  ContrailImageTag: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
)"

source stackrc
ipmi_password=ADMIN
ipmi_user=ADMIN

for node in $(openstack baremetal node list -c UUID -f value) ; do openstack baremetal node delete $node ; done

while IFS= read -r line; do      mac=`echo $line|awk '{print $1}'`;   name=`echo $line|awk '{print $2}'`;   kvm_ip=`echo $line|awk '{print $3}'`;   profile=`echo $line|awk '{print $4}'`;   ipmi_port=`echo $line|awk '{print $5}'`;   uuid=`openstack baremetal node create --driver pxe_ipmitool --property cpus=16 --property memory_mb=32768 --property local_gb=300 --property cpu_arch=x86_64 --driver-info ipmi_username=${ipmi_user}  --driver-info ipmi_address=${kvm_ip} --driver-info ipmi_password=${ipmi_password} --driver-info ipmi_port=${ipmi_port} --name=${name} --property capabilities=profile:${profile},boot_option:local -c uuid -f value`;   openstack baremetal port create --node ${uuid} ${mac}; done < <(cat ironic_list)

while IFS= read -r line; do      mac=`echo $line|awk '{print $1}'`;   name=`echo $line|awk '{print $2}'`;   kvm_ip=`echo $line|awk '{print $3}'`;   profile=`echo $line|awk '{print $4}'`;   ipmi_port=`echo $line|awk '{print $5}'`;   uuid=`openstack baremetal node create --driver pxe_ipmitool --property cpus=32 --property memory_mb=65536 --property local_gb=500 --property cpu_arch=x86_64 --driver-info ipmi_username=ADMIN --driver-info ipmi_address=${kvm_ip} --driver-info ipmi_password=ADMIN --driver-info ipmi_port=${ipmi_port} --name=${name} --property capabilities=profile:${profile},boot_option:local -c uuid -f value`;   openstack baremetal port create --node ${uuid} ${mac}; done < <(cat ironic_list_compute)

DEPLOY_KERNEL=$(openstack image show bm-deploy-kernel -f value -c id)
DEPLOY_RAMDISK=$(openstack image show bm-deploy-ramdisk -f value -c id)
for i in `openstack baremetal node list -c UUID -f value`; do openstack baremetal node set $i --driver-info deploy_kernel=$DEPLOY_KERNEL --driver-info deploy_ramdisk=$DEPLOY_RAMDISK; done

for i in `openstack baremetal node list -c UUID -f value`; do openstack baremetal node show $i -c properties -f value; done
for node in $(openstack baremetal node list -c UUID -f value) ; do openstack baremetal node manage $node ; done
sleep 60

#once nodes moved to manageable state, run introspection for the nodes.
openstack --debug overcloud node introspect --all-manageable --provide 2>&1 | tee -a introspect.log
ret=$?
if [ $ret != 0 ];
then
    echo "Introspection of the nodes failed..."
    exit 1
fi

openstack baremetal node list -c 'Provisioning State' -f value| grep -v available
ret=$?
if [ ${ret} == 0  ]; then
    echo "Introspection failed for some of the nodes"
    exit 1
fi

openstack flavor delete contrail-controller-issu
#create the flavors
for i in compute-dpdk compute-sriov compute control contrail-controller; do   openstack flavor create $i --ram 4096 --vcpus 1 --disk 40;   openstack flavor set --property "capabilities:boot_option"="local" --property "capabilities:profile"="${i}" ${i}; done

#Deploy the stack
openstack --debug overcloud deploy --templates ~/tripleo-heat-templates -e ~/overcloud_images.yaml -e ~/tripleo-heat-templates/environments/network-isolation.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-plugins.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-net.yaml --roles-file ~/tripleo-heat-templates/roles_data_contrail_aio.yaml 2>&1 | tee -a deploy.log
