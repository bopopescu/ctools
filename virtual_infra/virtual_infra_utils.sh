#!/usr/bin/env bash
set -x
TOOLS_WS=${TOOLS_WS:-$(pwd)}
function launch_virtual_testbed() {
    export PROJECT=${BUILD_TAG}
    local ALL_YML=/root/${PROJECT}/ansible/inventory/group_vars/all.yml
    sshpass -p "c0ntrail123" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root $BASE_CLUSTER " (
      mkdir /root/${PROJECT}/
    ) " || exit 1
    sshpass -p "c0ntrail123" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r ${TOOLS_WS}/virtual_infra ${TOOLS_WS}/ansible root@$BASE_CLUSTER:/root/${PROJECT}/
    sshpass -p "c0ntrail123" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root $BASE_CLUSTER " (
      set -e
      cd /root/${PROJECT}/virtual_infra
      source /etc/contrail/openstackrc
      source clusters/${BASE_CLUSTER}.clusterrc
      export VERSION=$VERSION
      export BRANCH=$BRANCH
      export SKU=$SKU
      export APPFORMIX_VERSION=$APPFORMIX_VERSION
      export OSIMAGE=$OSIMAGE
      export WEBSERVER_REPORT_PATH=$WEBSERVER_REPORT_PATH
      python create_delete_topology.py -t topologies/${TOPOLOGY} -c configs/${CONFIG} -p ${PROJECT} -f ${ALL_YML}
      python get_cfgm_ip.py -i ${ALL_YML} > config_node_ip
    ) " || (teardown_virtual_testbed && exit 1)
}

function teardown_virtual_testbed() {
    export PROJECT=${BUILD_TAG}
    local ALL_YML=/root/${PROJECT}/ansible/inventory/group_vars/all.yml
    TEARDOWN=${TEARDOWN:-true}
    if [ "${TEARDOWN}" = true ]; then
        sshpass -p "c0ntrail123" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root $BASE_CLUSTER " (
          cd /root/${PROJECT}/virtual_infra
          source /etc/contrail/openstackrc
          source clusters/${BASE_CLUSTER}.clusterrc
          python create_delete_topology.py -t topologies/${TOPOLOGY} -p ${PROJECT} -o del
        ) "
    else
        echo "TEARDOWN is set to $TEARDOWN, so we are not tearing down the cluster"
        echo "To teardown the cluster manually, do the below on $BASE_CLUSTER"
        echo "cd /root/${PROJECT}/virtual_infra"
        echo "source /etc/contrail/openstackrc"
        echo "source clusters/${BASE_CLUSTER}.clusterrc"
        echo "python create_delete_topology.py -t topologies/${TOPOLOGY} -p ${PROJECT} -o del"
    fi
}

function provision_cluster_wrapper() {
    export PROJECT=${BUILD_TAG}
    sshpass -p "c0ntrail123" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root $BASE_CLUSTER " (
        set -e
        export FEATURES=${FEATURES}
        cd /root/${PROJECT}/virtual_infra
        export BASE_CLUSTER=${BASE_CLUSTER}
        ./provision_cluster_wrapper.sh ${PROJECT} \$(cat config_node_ip)
      ) "
}

function wait_till_node_up() {
    local node=$1
    ((count=60))
    while [[ $count -ne 0 ]] ; do
        sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$node 'uname -a'
        rc=$?
        if [[ $rc -eq 0 ]]; then
            break
        fi
        echo "Node $node is not yet reachable"
        ((count = count - 1))
        sleep 5
    done
    if [[ $count -eq 0 ]]
    then
        echo "Node $node is Not reachable"
            exit 1
    fi
}

function get_os_version() {
    local cfgm_node=$1
    export OS_INFO=${OS_INFO:-$(sshpass -p 'c0ntrail123' ssh -o 'StrictHostKeyChecking no' -o 'UserKnownHostsFile /dev/null' root@$cfgm_node 'cat /etc/*elease | grep "PRETTY_NAME"')}
}

function install_packages() {
    local cfgm_node=$1
    get_os_version $cfgm_node
    if [[ $OS_INFO == *"CentOS"* ]]; then
        sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$cfgm_node 'yum install -y git vim python-pip && pip install ansible==2.5.2'
    elif [[ $OS_INFO == *"Red Hat"* || $OS_INFO == *"OpenShift"* ]]; then
        echo 'sleep 600 seconds for subscription manager to complete'
        sleep 600
        sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$cfgm_node " (
            set -e
            yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
            yum install -y git ansible-2.6.14 vim python-pip
            ) "
    elif [[ $OS_INFO == *"Ubuntu"* ]]; then
        sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$cfgm_node 'apt-get update && apt-get install -y git python2.7-minimal vim python-pip && pip install ansible==2.5.5'
    fi
    sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$cfgm_node 'pip install junos-eznc==2.2.0 jxmlease==1.0.1 ncclient==0.6.3 && ansible-galaxy install Juniper.junos'
}

function provision_cluster() {
    local PROJECT=$1
    local cfgm_node=$2
    wait_till_node_up $cfgm_node
    get_os_version $cfgm_node
    install_packages $cfgm_node
    sshpass -p c0ntrail123 scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r /root/${PROJECT}/ansible root@$cfgm_node:/root/ansible
    sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$cfgm_node " (
      cd /root/ansible
      export FEATURES=${FEATURES}
      export BASE_CLUSTER=${BASE_CLUSTER}
      ansible-playbook -i inventory/ playbooks/configure_etc_hosts.yml -v
      ansible-playbook -i inventory/ playbooks/all.yml -v $extra_args
    ) "
}
