#!/bin/bash
set -x
set -e
cluster_name=$1
is_svl_testbed=$2
count=0
cat /etc/ntp.conf | sed -e '/.*pool.ntp.org.*/s/^/#/g' | sed -e '/.*ntp.ubuntu.com.*/s/^/#/g' > /tmp/ntp.conf
rm -f /etc/ntp.conf
mv /tmp/ntp.conf /etc/ntp.conf
if [[ $is_svl_testbed ]];then
  echo "server 172.21.200.60" >> /etc/ntp.conf
else
  echo "server ntp.juniper.net" >> /etc/ntp.conf
fi
service ntp restart
while [ $(server-manager status server --cluster_id $cluster_name | grep -c  id) -ne $(server-manager status server --cluster_id $cluster_name | grep -c  provision_completed)  ]; do
    if [ "$count"  -ne 40 ]; then
        echo "Provisioing is not done yet, lets wait for some more time"
        sleep 100
        count=$((count+1))
        echo "true" > /tmp/smgr_prov
    else
        echo "waited for 3000 seconds, but provisioning did not go through, exiting"
        echo "false" > /tmp/smgr_prov
        #break
        exit 1
    fi
done
echo "true" > /tmp/smgr_prov
sleep 300
