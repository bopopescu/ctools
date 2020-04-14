#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}
source $TOOLS_WS/testers/utils

# AVAILABLE_TESTBEDS is a comma separated list of testbed filenames or paths
testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"

function run_ui_sanity {
    if [ $SKIP_SANITY -ne 0 ]
    then
        return 0
    fi
    search_package
    copy_fabric_test_artifacts
    run_fab "install_test_repo"
    run_fab "setup_test_env"
    run_fab "install_webui_packages:~"
    run_fab "update_config_option:openstack,/etc/keystone/keystone.conf,token,expiration,86400,keystone"
    run_fab "update_js_config:openstack,/etc/contrail/config.global.js,contrail-webui"
    check_venv_exists
    setup_sanity_base
}

function run_ui_task() {
    create_testbed || die "Failed to create required testbed details" 
    echo "running on testbed $TBFILE_NAME"
    reimage_and_bringup
    install_third_party_pkgs || die "installing GDB/ant failed" 
    run_ui_sanity || die "Run_sanity step failed"
    echo "Test Done" 
    collect_tech_support || die "Task to collect logs/cores failed"
    echo "Ending test on $TBFILE_NAME"
}

get_testbed
run_ui_task
unlock_testbed $TBFILE_NAME 
