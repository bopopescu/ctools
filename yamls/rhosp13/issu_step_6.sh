#!/usr/bin/bash

source stackrc
AGENT_MODE=$1

###############
# KERNEL MODE #
###############

if [ ${AGENT_MODE} == 'kernel' ]
then
    nodes=overcloud-novacompute-0
    if ! openstack overcloud upgrade run --nodes $nodes --playbook upgrade_steps_playbook.yaml
    then
        echo FAILED: UPGRADE STEPS PLAYBOOK FAILED FOR NOVA COMPUTE-0
	exit 1
    fi
    if ! openstack overcloud upgrade run --nodes $nodes --playbook deploy_steps_playbook.yaml
    then
        echo FAILED: DEPLOY STEPS PLAYBOOK FAILED FOR NOVA COMPUTE-0
	exit 1
    fi

    COM_KERNEL_0_IP=`nova list | awk '/overcloud-novacompute-0/ {print $12}' | cut -d '=' -f 2`
    COM_KERNEL_0_HOST_STRING=heat-admin@${COM_KERNEL_0_IP}
    sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COM_KERNEL_0_HOST_STRING} "(
        sudo contrail-status
    )"

fi

if [ ${AGENT_MODE} == 'kernel' ]
then
    nodes=overcloud-novacompute-1

    if ! openstack overcloud upgrade run --nodes $nodes --playbook upgrade_steps_playbook.yaml
    then
        echo FAILED: UPGRADE STEPS PLAYBOOK FAILED FOR NOVA COMPUTE-1
	exit 1
    fi
    if ! openstack overcloud upgrade run --nodes $nodes --playbook deploy_steps_playbook.yaml
    then
        echo FAILED: DEPLOY STEPS PLAYBOOK FAILED FOR NOVA COMPUTE-1 
	exit 1
    fi

    COM_KERNEL_1_IP=`nova list | awk '/overcloud-novacompute-1/ {print $12}' | cut -d '=' -f 2`
    COM_KERNEL_1_HOST_STRING=heat-admin@${COM_KERNEL_1_IP}
    sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COM_KERNEL_1_HOST_STRING} "(
        sudo contrail-status
    )"

fi


#############
# DPDK MODE #
#############

if [ ${AGENT_MODE} == 'dpdk' ]
then
    nodes=overcloud-contraildpdk-0

    if ! openstack overcloud upgrade run --nodes $nodes --playbook upgrade_steps_playbook.yaml
    then
        echo FAILED: UPGRADE STEPS PLAYBOOK FAILED FOR DPDK COMPUTE-0 
	exit 1
    fi

    if ! openstack overcloud upgrade run --nodes $nodes --playbook deploy_steps_playbook.yaml
    then
        echo FAILED: DEPLOY STEPS PLAYBOOK FAILED FOR DPDK COMPUTE-0 
	exit 1
    fi

    COM_DPDK_0_IP=`nova list | awk '/overcloud-contraildpdk-0/ {print $12}' | cut -d '=' -f 2`
    COM_DPDK_0_HOST_STRING=heat-admin@${COM_DPDK_0_IP}
    sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COM_DPDK_0_HOST_STRING} "(
        sudo contrail-status
        sudo ifdown vhost0
    )"
    sleep 20s
    sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COM_DPDK_0_HOST_STRING} "(
        sudo ifup vhost0
    )"
    sleep 20s
    sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COM_DPDK_0_HOST_STRING} "(
        sudo contrail-status
    )"

fi

if [ ${AGENT_MODE} == 'dpdk' ]
then
    nodes=overcloud-contraildpdk-1
    
    if ! openstack overcloud upgrade run --nodes $nodes --playbook upgrade_steps_playbook.yaml
    then
        echo FAILED: UPGRADE STEPS PLAYBOOK FAILED FOR DPDK COMPUTE-1 
	exit 1
    fi

    if ! openstack overcloud upgrade run --nodes $nodes --playbook deploy_steps_playbook.yaml
    then 
        echo FAILED: DEPLOY STEPS PLAYBOOK FAILED FOR DPDK COMPUTE-1
	exit 1
    fi

    COM_DPDK_1_IP=`nova list | awk '/overcloud-contraildpdk-1/ {print $12}' | cut -d '=' -f 2`
    COM_DPDK_1_HOST_STRING=heat-admin@${COM_DPDK_1_IP}
    sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COM_DPDK_1_HOST_STRING} "(
        sudo contrail-status
        sudo ifdown vhost0
    )"
    sleep 20s
    sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COM_DPDK_1_HOST_STRING} "(
        sudo ifup vhost0
    )"
    sleep 20s
    sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COM_DPDK_1_HOST_STRING} "(
        sudo contrail-status
    )"

fi
