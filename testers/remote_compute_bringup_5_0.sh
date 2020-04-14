#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}
source $TOOLS_WS/testers/utils
source $TOOLS_WS/testers/utils_virtual
# AVAILABLE_TESTBEDS is a comma separated list of testbed filenames or paths
launch_remote_compute_setup_5_0
