#!/usr/bin/bash

source stackrc

nodes=overcloud-contrailcontroller-0,overcloud-contrailcontroller-1,overcloud-contrailcontroller-2
if ! openstack overcloud upgrade run --nodes $nodes --playbook upgrade_steps_playbook.yaml
then
    echo FAILED: UPGRADE STEPS PLAYBOOK FAILED FOR CC-0-2 
    exit 1
fi

if ! openstack overcloud upgrade run --nodes $nodes --playbook deploy_steps_playbook.yaml
then
    echo FAILED: DEPLOY STEPS PLAYBOOK FAILED FOR CC-0-2 
    exit 1
fi

if ! openstack overcloud upgrade run --nodes $nodes --playbook post_upgrade_steps_playbook.yaml 
then
    echo FAILED: POST UPGRADE STEPS PLAYBOOK FAILED FOR CC-0-2 
    exit 1
fi

CC_0_IP=`nova list | awk '/overcloud-contrailcontroller-0/ {print $12}' | cut -d '=' -f 2`
CC_0_HOST_STRING=heat-admin@${CC_0_IP}
sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_0_HOST_STRING} "(
    sudo contrail-status
)"

CC_1_IP=`nova list | awk '/overcloud-contrailcontroller-1/ {print $12}' | cut -d '=' -f 2`
CC_1_HOST_STRING=heat-admin@${CC_1_IP}
sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_1_HOST_STRING} "(
    sudo contrail-status
)"

CC_2_IP=`nova list | awk '/overcloud-contrailcontroller-2/ {print $12}' | cut -d '=' -f 2`
CC_2_HOST_STRING=heat-admin@${CC_2_IP}
sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_2_HOST_STRING} "(
    sudo contrail-status
)"
