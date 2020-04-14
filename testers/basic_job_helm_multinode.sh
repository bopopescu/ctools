#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}
source $TOOLS_WS/testers/smgr_utils
source $TOOLS_WS/testers/utils
source $TOOLS_WS/testers/utils_helm
# AVAILABLE_TESTBEDS is a comma separated list of testbed filenames or paths

testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"

check_contrail_image

get_testbed

reimage_using_SM_helm

update_ssh_key

create_values_yaml

helm_copy_ansible
helm_preconfig
helm_provision

vrouter_version

run_tempest

unlock_testbed $TBFILE_NAME
