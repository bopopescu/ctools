source stackrc
NODES=`nova list | awk '/192/ {print $12}' | cut -d '=' -f 2`
echo $NODES
for IP in $NODES
do
        ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo sed -i '1 i\nameserver 192.168.122.1' /etc/resolv.conf"
        ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "curl --insecure --output katello-ca-consumer-latest.noarch.rpm https://noden14.englab.juniper.net/pub/katello-ca-consumer-latest.noarch.rpm"
        ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo yum localinstall -y katello-ca-consumer-latest.noarch.rpm"
	ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo subscription-manager unregister"
        ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo subscription-manager register --activationkey=ak_rh_13_release --org=BLR_RHOSP --force"
	ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo subscription-manager attach --pool 8a4c58186e3f113601707ac13a087b80"
        ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo subscription-manager repos --enable=rhel-7-server-rpms --enable=rhel-7-server-rh-common-rpms --enable=rhel-ha-for-rhel-7-server-rpms --enable=rhel-7-server-openstack-13-rpms --enable=rhel-7-server-extras-rpms"
done
for IP in $NODES
do
	ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo subscription-manager identity"
done
