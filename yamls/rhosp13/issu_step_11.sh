#!/usr/bin/bash

source stackrc
AGENT_MODE=$1

###############
# KERNEL MODE #
###############

if [ ${AGENT_MODE} == 'kernel' ]
then
    nodes=overcloud-novacompute-0,overcloud-novacompute-1
    if ! openstack overcloud upgrade run --nodes $nodes --playbook post_upgrade_steps_playbook.yaml
    then
        echo FAILED: POST UPGRADE STEPS PLAYBOOK FAILED FOR NOVA COMPUTE-0 and 1
	exit 1
    fi
fi

#############
# DPDK MODE #
#############

if [ ${AGENT_MODE} == 'dpdk' ]
then
    nodes=overcloud-contraildpdk-0,overcloud-contraildpdk-1

    if ! openstack overcloud upgrade run --nodes $nodes --playbook post_upgrade_steps_playbook.yaml 
    then
        echo FAILED: POST UPGRADE STEPS PLAYBOOK FAILED FOR DPDK COMPUTE-0 and 1
	exit 1
    fi
fi

nodes=overcloud-controller-0
if ! openstack overcloud upgrade run --nodes $nodes --playbook post_upgrade_steps_playbook.yaml
then
    echo FAILED: POST UPGRADE STEPS PLAYBOOK FAILED FOR OC-0
    exit 1
fi
