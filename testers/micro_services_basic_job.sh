#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}
source $TOOLS_WS/testers/utils
source $TOOLS_WS/testers/micro_services_utils
# AVAILABLE_TESTBEDS is a comma separated list of testbed filenames or paths
testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"

get_testbed
if [ -z $INITIALIZE_DEPLOYER_VM ]
then
  export INITIALIZE_DEPLOYER_VM=0
fi
if [ $INITIALIZE_DEPLOYER_VM -eq 1 ]
then
  checkout_fab_repo
  use_testbed_file
  initialize_any_vms
fi
run_sanity_task
generate_core_email
unlock_testbed $TBFILE_NAME
