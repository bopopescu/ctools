#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}
source $TOOLS_WS/testers/utils
source $TOOLS_WS/testers/micro_services_utils_rhel
# AVAILABLE_TESTBEDS is a comma separated list of testbed filenames or paths
#testbeds=(${AVAILABLE_TESTBEDS//,/ })
#echo "AVAILABLE TESTBEDS : ${testbeds[@]}"
echo removed testbed lock here
#get_testbed
run_rhel_sanity_task
#unlock_testbed $TBFILE_NAME
