#!/usr/bin/bash

UNDERCLOUD_STACK_USER=$1
UNDERCLOUD_IP=$2
UNDERCLOUD_PASSWORD=$3
UNDERCLOUD_STACK_HOME=$4
DEFAULT_TEST_YAML=$5
CONTRAIL_REGISTRY=$6
SANITY_VERSION=$7
REDHAT_USER=${8}
REDHAT_PASS=${9}
REDHAT_POOL=${10}

API_SERVER_HOST_STRING=`sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP "grep -r \"cfgm0_host_string:\" ${UNDERCLOUD_STACK_HOME}/${DEFAULT_TEST_YAML} | cut -d ':' -f 2"`
API_SERVER_HOST_PWD=`sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP "grep -r "cfgm0_host_pwd:" ${UNDERCLOUD_STACK_HOME}/${DEFAULT_TEST_YAML} | cut -d ':' -f 2"`
API_SERVER_IP=`echo $API_SERVER_HOST_STRING | cut -d'@' -f 2`
COMPUTE0_HOST_STRING=`sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP "grep -r \"cmpt0_host_string:\" ${UNDERCLOUD_STACK_HOME}/${DEFAULT_TEST_YAML} | cut -d ':' -f 2"`
COMPUTE1_HOST_STRING=`sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP "grep -r \"cmpt1_host_string:\" ${UNDERCLOUD_STACK_HOME}/${DEFAULT_TEST_YAML} | cut -d ':' -f 2"`
COMPUTE2_HOST_STRING=`sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP "grep -r \"cmpt2_host_string:\" ${UNDERCLOUD_STACK_HOME}/${DEFAULT_TEST_YAML} | cut -d ':' -f 2"`

sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
sshpass ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COMPUTE0_HOST_STRING} \" (
                #sudo subscription-manager register --username ${REDHAT_USER} --password ${REDHAT_PASS} --force
                #sudo subscription-manager attach --pool ${REDHAT_POOL}
                sudo subscription-manager unregister
                sudo yum localinstall -y katello-ca-consumer-latest.noarch.rpm
                sudo subscription-manager register --activationkey=ak_rh_13_release --org=BLR_RHOSP
                sudo yum -y install iperf3

        ) \"
)"

sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
sshpass ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COMPUTE1_HOST_STRING} \" (
                #sudo subscription-manager register --username ${REDHAT_USER} --password ${REDHAT_PASS} --force
                #sudo subscription-manager attach --pool ${REDHAT_POOL}
                sudo subscription-manager unregister
                sudo yum localinstall -y katello-ca-consumer-latest.noarch.rpm
                sudo subscription-manager register --activationkey=ak_rh_13_release --org=BLR_RHOSP
                sudo yum -y install iperf3
        ) \"
)"

sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
sshpass ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${COMPUTE2_HOST_STRING} \" (
                #sudo subscription-manager register --username ${REDHAT_USER} --password ${REDHAT_PASS} --force
                #sudo subscription-manager attach --pool ${REDHAT_POOL}
                sudo subscription-manager unregister
                sudo yum localinstall -y katello-ca-consumer-latest.noarch.rpm
                sudo subscription-manager register --activationkey=ak_rh_13_release --org=BLR_RHOSP
                sudo yum -y install iperf3
        ) \"
)"

sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
    cat ~/.ssh/id_rsa.pub | ssh -o StrictHostKeyChecking=no ${API_SERVER_HOST_STRING} 'cat >> /home/heat-admin/id_rsa.pub'
    cat ~/.ssh/id_rsa | ssh -o StrictHostKeyChecking=no ${API_SERVER_HOST_STRING} 'cat >> /home/heat-admin/id_rsa'
    cat ${UNDERCLOUD_STACK_HOME}/${DEFAULT_TEST_YAML} | ssh -o StrictHostKeyChecking=no ${API_SERVER_HOST_STRING} 'cat >> /home/heat-admin/${DEFAULT_TEST_YAML}'
    cat << EOF > sed_mx_gw_test_set.sh
sudo sed -i '/EXTRA_RUN_TEST_ARGS/ s/\"$/-e MX_GW_TEST=1\"/' /usr/local/bin/testrunner.sh
EOF
    
    cat sed_mx_gw_test_set.sh | ssh -o StrictHostKeyChecking=no ${API_SERVER_HOST_STRING} 'cat >> /home/heat-admin/sed_mx_gw_test_set.sh'
    rm sed_mx_gw_test_set.sh
    sshpass -p ${API_SERVER_HOST_PWD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${API_SERVER_HOST_STRING} \" (
        echo RELEASE_5_1
        set -e
        sudo chmod 0600 /home/heat-admin/id_rsa.pub
        sudo chmod 0600 /home/heat-admin/id_rsa
        sudo chmod +x sed_mx_gw_test_set.sh
        sudo cp /home/heat-admin/id_rsa.pub /root/.ssh/ >> sanity.log
        sudo cp /home/heat-admin/id_rsa /root/.ssh/ >> sanity.log
        sudo curl -o /usr/local/bin/testrunner.sh https://raw.githubusercontent.com/Juniper/contrail-test/master/testrunner.sh >> sanity.log
        sudo chmod +x /usr/local/bin/testrunner.sh >> sanity.log
        
        ./sed_mx_gw_test_set.sh
        rm sed_mx_gw_test_set.sh
        sudo sed -i 's/--privileged/--privileged --network host/g' /usr/local/bin/testrunner.sh >> sanity.log
        echo `sudo diff /usr/local/bin/testrunner.sh testrunner_bkp.sh` 
        sudo sed -i '/nameserver/i\nameserver 172.21.200.60' /etc/resolv.conf
        echo ${CONTRAIL_REGISTRY}
        echo ${SANITY_VERSION}
        sleep 30
        
        sudo /usr/local/bin/testrunner.sh pull ${CONTRAIL_REGISTRY}/contrail-nightly/contrail-test-test:${SANITY_VERSION} >> sanity.log
        sudo echo "Running Sanity on the setup"
      
        sudo bash -x /usr/local/bin/testrunner.sh run -k /root/.ssh/id_rsa -K /root/.ssh/id_rsa.pub -P /home/heat-admin/${DEFAULT_TEST_YAML} -f sanity ${CONTRAIL_REGISTRY}/contrail-nightly/contrail-test-test:${SANITY_VERSION} >> sanity.log
    ) \"
) "
