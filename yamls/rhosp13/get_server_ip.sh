#!/usr/bin/bash

openstack server list -c Networks -c Name -f value > server_list
sed -i 's/ctlplane=//' server_list

for i in {1..9};do
        line=`sed -n ${i}p server_list`;host_name=`echo $line|awk '{print $1}'`; ip=`echo $line|awk '{print $2}'`; sshpass ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${ip} "sudo ip addr show|grep '10.0.0.\|10.1.0.'| cut -d / -f 1| cut -d 't' -f 2| cut -d ' ' -f 2" > ${host_name};
done

if [ ! -f "overcloudrc" ]; then
 source stackrc
 openstack action execution run   --save-result   --run-sync   tripleo.deployment.overcloudrc   '{"container":"overcloud"}'   | jq -r '.["result"]["overcloudrc.v3"]'   > overcloudrc
fi

cat overcloudrc | grep OS_PASSWORD| cut -d = -f 2 > keystone
openstack_ip=`cat server_list| grep overcloud-controller-0| awk '{print $2}'`
sshpass ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${openstack_ip} "sudo netstat -anp|grep 5000|grep haproxy| grep 0.0.0.0" >> keystone
