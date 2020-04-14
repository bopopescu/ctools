#!/usr/bin/env bash
set -x
TESTBED_FILE_LOCATION=${TESTBED_FILE_LOCATION:-"ansible/testbeds"}
TIMESTAMP=$(date +%Y%m%d%H%M%S)
SSHVAR='sshpass -p c0ntrail123 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
SCPVAR='sshpass -p c0ntrail123 scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
TOOLS_WS=${TOOLS_WS:-$(pwd)}
SKIP_REIMAGE=${SKIP_REIMAGE:-0}
SKIP_CONFIGURE_VM=${SKIP_CONFIGURE_VM:-0}
SKIP_PROVISION=${SKIP_PROVISION:-0}
SKIP_SANITY=${SKIP_SANITY:-0}
ANSIBLE_NODE_IP=${ANSIBLE_NODE_IP:-"localhost"}
function reimage_cluster() {
    $SCPVAR -r $TOOLS_WS root@$ANSIBLE_NODE_IP:/root/ansible-$TIMESTAMP/
    if [[ $SKIP_REIMAGE = 0 ]]; then
        $SSHVAR root@$ANSIBLE_NODE_IP " (
            cd /root/ansible-$TIMESTAMP/ansible
            export OS_IMAGE=$OS_IMAGE
            ansible-playbook -i inventory/ playbooks/reimage.yml -vv
        ) " || exit 1
    fi
    if [[ $SKIP_CONFIGURE_VM = 0 ]]; then
        $SSHVAR root@$ANSIBLE_NODE_IP " (
            set -e
            cd /root/ansible-$TIMESTAMP/ansible
            ansible-playbook -i inventory/ playbooks/configure_vm.yml -vv
            ansible-playbook -i inventory/ playbooks/configure_ctrldata.yml -vv
        ) " || exit 1
    fi
}

function provision_cluster() {
    $SCPVAR -r $TOOLS_WS/ansible root@$TEST_NODE_IP:/root/ansible-$TIMESTAMP/
    $SSHVAR root@$TEST_NODE_IP " (
        yum install -y git epel-release sshpass; yum install -y python-pip; pip install ansible==2.7.11
        set -e
        cd /root/ansible-$TIMESTAMP
        export SKU=${SKU}
        export VERSION=${VERSION}
        ansible-playbook -i inventory/ playbooks/install.yml -vv
        ansible-playbook -i inventory/ playbooks/configure_static_routes.yml -vv
        ansible-playbook -i inventory/ playbooks/deploy.yml -vv
    ) " || exit 1
}

function run_sanity() {
    $SSHVAR root@$TEST_NODE_IP " (
        cd /root/ansible-$TIMESTAMP
        export FEATURES=${FEATURES}
        export VERSION=${VERSION}
        ansible-playbook -i inventory/ playbooks/run_sanity.yml
        ansible-playbook -i inventory/ playbooks/upload_logs_cores.yml -vv
    ) "
}

if [[ -z "$TESTBED_INPUT_FILE" ]]
then
    ALL_YML=$TOOLS_WS/$TESTBED_FILE_LOCATION/$TESTBED_FILE
else
    ALL_YML=$WORKSPACE/TESTBED_INPUT_FILE
fi
cp $ALL_YML $TOOLS_WS/ansible/inventory/group_vars/all.yml
reimage_cluster

TEST_NODE_IP=$($SSHVAR root@$ANSIBLE_NODE_IP "cd /root/ansible-$TIMESTAMP/; python virtual_infra/get_cfgm_ip.py -i ansible/inventory/group_vars/all.yml")
if [[ $SKIP_PROVISION = 0 ]]; then
    provision_cluster
fi

if [[ $SKIP_SANITY = 0 ]]; then
    run_sanity
fi
