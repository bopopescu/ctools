#!/usr/bin/bash

UNDERCLOUD_PASSWORD=contrail123
UNDERCLOUD_STACK_USER=stack
UNDERCLOUD_STACK_HOME=/home/stack
UNDERCLOUD_IP=$1

sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /root/contrail-tools/yamls/rhosp13/private_pub_key_issu.sh ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/
sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
    source stackrc
    sudo touch issu_converge.log
    sudo chmod 777 issu_converge.log
    openstack overcloud upgrade converge --stack overcloud --templates ~/tripleo-heat-templates -e ~/overcloud_images.yaml -e ~/tripleo-heat-templates/environments/network-isolation.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-plugins.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-net.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-issu.yaml --roles-file ~/tripleo-heat-templates/roles_data_contrail_aio.yaml 
    chmod +x satellite_unsubscribe.sh
    ./satellite_unsubscribe.sh >> issu_converge.log
)"
