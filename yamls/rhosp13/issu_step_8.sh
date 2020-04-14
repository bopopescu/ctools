#!/usr/bin/bash

source stackrc
CC_ISSU_0_IP=`nova list | awk '/overcloud-contrailcontrollerissu-0/ {print $12}' | cut -d '=' -f 2`
CC_ISSU_0_HOSP_STRING=heat-admin@${CC_ISSU_0_IP}

#sudo yum install sshpass -y
sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${CC_ISSU_0_HOSP_STRING} "(
    cd /etc/contrail/issu
    ./issu_node_sync_post.sh 
    sleep 5s
    ./issu_node_pair.sh del
    sleep 5s
    sudo contrail-status
    )"
