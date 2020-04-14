#!/bin/bash
set -x
set -e
cluster_name=$1
sm_client=${2:-"server-manager-client"}
echo "cluster_name is $cluster_name"
count=0
retry=1

json=""
if $sm_client status server --cluster_id $cluster_name --json; then
    json="--json"
fi

display="display"
if $sm_client show cluster --cluster_id $cluster_name; then
    display="show"
fi

sleep 120
while [ $($sm_client status server --cluster_id $cluster_name $json | grep -c id ) -ne $($sm_client status server --cluster_id $cluster_name $json | grep -c reimage_completed ) ]; do
    if [ "$count" -ne 45 ]
    then
        #Its observed that few servers were stuck in restart issued when the cluster is reimaged
        #Adding the workaround to retrigger reimage of the specific server which had issues
        if [ "$count" -eq 30 ] && [ "$retry" -eq 1 ]
        then
           retry=0
           for id in $($sm_client status server --cluster_id $cluster_name $json | grep id | awk '{print $2}' | sed 's/"//g' | sed 's/,//g'); do
               if $sm_client status server --server_id $id $json | grep status | grep restart_issued; then
                   image=$($sm_client $display cluster --cluster_id $cluster_name --detail | grep base_image_id | awk '{print $2}' | sed 's/"//g' | sed 's/,//g')
                   $sm_client reimage --no_confirm --server_id $id $image
                   count=15
               fi
           done
        fi
        sleep 60
        count=$((count+1))
        echo "reimage in progress, please wait..."
    else
        echo "seems to be problem with reimage, exiting!!!"
        exit 1
    fi
done
sleep 180 #Wait till the system boots up
