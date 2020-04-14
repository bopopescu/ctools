#!/bin/bash
set -x
set -e
tag=$1
echo "tag is $tag"
count=0
while [ $(server-manager-client status server --tag $tag --json | grep -c id ) -ne $(server-manager-client status server --tag $tag --json | grep -c reimage_completed ) ]; do
    if [ "$count" -ne 40 ]
    then
        sleep 100
        count=$((count+1))
        echo "reimage in progress, please wait..."
    else
        echo "seems to be problem with reimage, exiting!!!"
        exit 1
    fi
done

