#!/usr/bin/bash

UNDERCLOUD_PASSWORD=contrail123
UNDERCLOUD_STACK_USER=stack
UNDERCLOUD_STACK_HOME=/home/stack
UNDERCLOUD_IP=$1
BUILD_ISSU=$2
CONTRAIL_REGISTRY=$3

sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /root/contrail-tools/yamls/rhosp13/private_pub_key_issu.sh ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/
sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
    cp contrail-tripleo-heat-templates/environments/contrail/contrail-issu.yaml /home/stack/tripleo-heat-templates/environments/contrail/contrail-issu.yaml
    sed -i '/  ContrailControllerIssuCount: /a \  ContrailControllerIssuCount: 3' tripleo-heat-templates/environments/contrail/contrail-issu.yaml
    sed -i '0,/  ContrailControllerIssuCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-issu.yaml
    sed -i '/  ContrailIssuImageTag: /a \  ContrailIssuImageTag: ${BUILD_ISSU}' tripleo-heat-templates/environments/contrail/contrail-issu.yaml
    sed -i '0,/  ContrailIssuImageTag: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-issu.yaml
    chmod +x private_pub_key_issu.sh
    ./private_pub_key_issu.sh
    source stackrc
    openstack flavor delete contrail-controller-issu
    openstack flavor create contrail-controller-issu --ram 4096 --vcpus 1 --disk 40
    openstack flavor set --property "capabilities:boot_option"="local" --property "capabilities:profile"="contrail-controller-issu" contrail-controller-issu
    ~/tripleo-heat-templates/tools/contrail/import_contrail_container.sh -f /tmp/contrail_container.yaml -r ${CONTRAIL_REGISTRY}/contrail-nightly -i 1 -t ${BUILD_ISSU}
    openstack --debug overcloud container image upload --config-file  /tmp/contrail_container.yaml --verbose 2>&1 | tee -a upload-image-${BUILD_ISSU}.log

    openstack overcloud deploy --templates ~/tripleo-heat-templates -e ~/overcloud_images.yaml -e ~/tripleo-heat-templates/environments/network-isolation.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-plugins.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-net.yaml -e ~/tripleo-heat-templates/environments/contrail/contrail-issu.yaml --roles-file ~/tripleo-heat-templates/roles_data_contrail_aio.yaml
)"
