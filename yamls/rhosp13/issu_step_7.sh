#!/usr/bin/bash

source stackrc

nodes=overcloud-controller-0
if ! openstack overcloud upgrade run --nodes $nodes --playbook upgrade_steps_playbook.yaml
then
    echo FAILED: UPGRADE STEPS PLAYBOOK FAILED FOR OC-0
    exit 1
fi

if ! openstack overcloud upgrade run --nodes $nodes --playbook deploy_steps_playbook.yaml
then
    echo FAILED: DEPLOY STEPS PLAYBOOK FAILED FOR OC-0
    exit 1
fi
