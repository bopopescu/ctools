source stackrc
NODES=`nova list | awk '/192/ {print $12}' | cut -d '=' -f 2`
echo $NODES
for IP in $NODES
do
	ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo contrail-status"
	ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo docker ps"
        ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo subscription-manager unregister"
done
for IP in $NODES
do
	ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null heat-admin@${IP} "sudo subscription-manager identity"
done
