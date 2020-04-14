#!/usr/bin/bash

source stackrc
CC_ISSU_0_IP=`nova list | awk '/overcloud-contrailcontrollerissu-0/ {print $12}' | cut -d '=' -f 2`
CC_ISSU_0_HOSP_STRING=heat-admin@${CC_ISSU_0_IP}

sudo yum install sshpass -y
sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_ISSU_0_HOSP_STRING} "(
    cd /etc/contrail/issu
    ./issu_node_pair.sh add pair_with_new
    sleep 5
    issu_config=issu_revert.conf ./issu_node_sync.sh
    sleep 5s
    )"

CC_0_IP=`nova list | awk '/overcloud-contrailcontroller-0/ {print $12}' | cut -d '=' -f 2`
CC_0_HOSP_STRING=heat-admin@${CC_0_IP}

sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_0_HOSP_STRING} "(
    sudo docker restart contrail_control_control
    )"

CC_1_IP=`nova list | awk '/overcloud-contrailcontroller-1/ {print $12}' | cut -d '=' -f 2`
CC_1_HOSP_STRING=heat-admin@${CC_1_IP}

sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_1_HOSP_STRING} "(
    sudo docker restart contrail_control_control
    )"

CC_2_IP=`nova list | awk '/overcloud-contrailcontroller-2/ {print $12}' | cut -d '=' -f 2`
CC_2_HOSP_STRING=heat-admin@${CC_2_IP}

sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_2_HOSP_STRING} "(
    sudo docker restart contrail_control_control
    )"
