#!/usr/bin/bash

UNDERCLOUD_PASSWORD=contrail123
UNDERCLOUD_STACK_USER=stack
UNDERCLOUD_IP=$1
BUILD_ISSU=$2

sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
    sed -i '/  ContrailImageTag: /a \  ContrailImageTag: ${BUILD_ISSU}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
    sed -i '0,/  ContrailImageTag: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
    source stackrc
    sudo touch issu_prepare.log
    sudo chmod 777 issu_prepare.log
    openstack overcloud upgrade prepare --stack overcloud --templates ~/tripleo-heat-templates -e ~/overcloud_images.yaml -e ~/tripleo-heat-templates/environments/network-isolation.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-plugins.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-net.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-issu.yaml --roles-file ~/tripleo-heat-templates/roles_data_contrail_aio.yaml >> issu_prepare.log
    chmod +x satellite_subscribe.sh
    ./satellite_subscribe.sh >> issu_prepare.log
    )"
