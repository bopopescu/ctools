#!/usr/bin/bash

UNDERCLOUD_STACK_USER=$1
UNDERCLOUD_IP=$2
UNDERCLOUD_PASSWORD=$3
UNDERCLOUD_STACK_HOME=$4
DEFAULT_TEST_YAML=$5
CONTRAIL_REGISTRY=$6
SANITY_VERSION=$7

sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
    cp ~/.ssh/id_rsa.pub .
    cp ~/.ssh/id_rsa .
    sudo chmod 0600 id_rsa.pub
    sudo chmod 0600 id_rsa
    sudo curl -o /usr/local/bin/testrunner.sh https://raw.githubusercontent.com/Juniper/contrail-test/master/testrunner.sh
    sudo chmod +x /usr/local/bin/testrunner.sh
    sudo sed -i 's/--privileged/--privileged --network host/g' /usr/local/bin/testrunner.sh
    sudo sed -i '/nameserver/i\nameserver 172.21.200.60' /etc/resolv.conf
    sudo /usr/local/bin/testrunner.sh pull ${CONTRAIL_REGISTRY}/contrail-nightly/contrail-test-test:${SANITY_VERSION}
    ) "
