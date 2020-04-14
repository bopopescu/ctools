#!/bin/bash
set -x
set -e
image_name=$1
count=0
while [ $(server-manager display image --image_id $image_name --json | grep -c  id) -ne 1 ]; do
    if [ "$count"  -ne 120 ]; then
        echo "Image is not added yet, lets wait for some more time"
        sleep 30
        count=$((count+1))
        echo "true" > /tmp/image_add
    else
        echo "waited for 60 minutes, but imgae add didn't go through, exiting"
        echo "false" > /tmp/image_add
        #break
        exit 1
    fi
done
echo "true" > /tmp/image_add
sleep 60
