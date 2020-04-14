#!/usr/bin/bash

source stackrc
CC_ISSU_0_IP=`nova list | awk '/overcloud-contrailcontrollerissu-0/ {print $12}' | cut -d '=' -f 2`
CC_ISSU_0_HOSP_STRING=heat-admin@${CC_ISSU_0_IP}

sudo yum install sshpass -y
sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_ISSU_0_HOSP_STRING} "(
    cd /etc/contrail/issu
    ./issu_node_pair.sh
    sleep 5s
    sudo contrail-status
    ./issu_node_sync.sh
    sleep 5s
    sudo docker restart contrail_control_control
    )"

CC_ISSU_1_IP=`nova list | awk '/overcloud-contrailcontrollerissu-1/ {print $12}' | cut -d '=' -f 2`
CC_ISSU_1_HOSP_STRING=heat-admin@${CC_ISSU_1_IP}

sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_ISSU_1_HOSP_STRING} "(
    sudo docker restart contrail_control_control
    )"

CC_ISSU_2_IP=`nova list | awk '/overcloud-contrailcontrollerissu-2/ {print $12}' | cut -d '=' -f 2`
CC_ISSU_2_HOSP_STRING=heat-admin@${CC_ISSU_2_IP}

sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_ISSU_2_HOSP_STRING} "(
    sudo docker restart contrail_control_control
    )"
