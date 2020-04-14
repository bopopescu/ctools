#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}
source $TOOLS_WS/testers/utils
# AVAILABLE_TESTBEDS is a comma separated list of testbed filenames or paths
testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"

get_testbed
create_testbed || die "Failed to create required testbed details"
echo "Running tests on $TBFILE_NAME .."
reimage_setup || debug_and_die "Reimage failed!"
search_third_party_package
run_build_fab "cleanup_repo"

if [ -z $REDHAT_72 ]; then
    # Workaround for Bug #1463953; Adding carriage return to authorized keys
    (cd $TOOLS_WS/contrail-fabric-utils; fab -R openstack -- 'echo "$(cat ~/.ssh/authorized_keys)" > ~/.ssh/authorized_keys')

    if [ "$SKU" == icehouse ]; then
        run_build_fab install_rhosp5_repo || debug_and_die "Failed during installing rhosp5 repo"
    elif [ "$SKU" == juno ]; then
        run_build_fab install_rhosp6_repo || debug_and_die "Failed during installing rhosp6 repo"
    else
        run_build_fab install_rhosp7_repo || debug_and_die "Failed during installing rhosp7 repo"
    fi
else
    fab install_rhosp8_repo || debug_and_die "Failed during installing rhosp8 repo"
fi
run_build_fab "install_pkg_all_without_openstack:${THIRD_PARTY_PKG_FILE}"  || debug_and_die "Task install_pkg_all_without_openstack failed!!"
copy_fabric_test_artifacts
run_build_fab "install_pkg_all_without_openstack:${PKG_FILE}" || debug_and_die "Task install_pkg_all_without_openstack failed!!"
run_setup_shell_script

if [ -z $REDHAT_72 ]; then
    if [ "$SKU" == icehouse ]; then
        run_build_fab upgrade_kernel_without_openstack
    else
        run_build_fab update_all_node
        echo "Waiting for 300secs for target nodes to be UP"
        sleep 300
    fi
else
    run_build_fab update_all_node || debug_and_die "update_all_node failed"
    run_build_fab wait_till_all_up:waitdown=False,attempts=90 || debug_and_die "Failed waiting for nodes to come up after update_all"
    run_build_fab upgrade_kernel_all || debug_and_die "upgrade_kernel_all failed"
    run_build_fab wait_till_all_up:waitdown=False,attempts=90 || debug_and_die "Failed waiting for nodes to come up after upgrade_kernel_all"
fi

run_build_fab "setup_rhosp_node" || debug_and_die "Failed during setup_rhosp_node"
run_build_fab "update_keystone_admin_token"
if [ -z $REDHAT_72 ]; then
    run_build_fab "update_service_tenant"
    exec_cmds -s "root@10.204.217.134" -p ${API_SERVER_HOST_PASSWORD} -c "                                               
        openstack-config --set /etc/nova/nova.conf neutron url http://10.204.217.133:9696"
fi
run_build_fab "update_neutron_password"
run_build_fab "update_nova_password"
sshpass -p $API_SERVER_HOST_PASSWORD scp ${SSHOPT} $TOOLS_WS/contrail-fabric-utils/fabfile/testbeds/testbed.py  ${API_SERVER_HOST_STRING}:$tbpath/testbed.py

run_fab "install_without_openstack" || debug_and_die "Contrail install failed!"
sleep 300
run_fab "update_keystone_admin_token"

sshpass -p $API_SERVER_HOST_PASSWORD scp ${SSHOPT} $TOOLS_WS/contrail-fabric-utils/fabfile/testbeds/testbed.py  ${API_SERVER_HOST_STRING}:$tbpath/testbed.py
run_fab "setup_interface"
run_fab "setup_without_openstack"  || debug_and_die "Setup failed!"
sleep 120

if [[ $TEST_RUN_INFRA == 'docker' ]]; then
        search_package
        pkg_file_name=`basename $PKG_FILE`
        export PACKAGE_VERSION=`echo ${pkg_file_name} | sed 's/contrail-install-packages[-_]\([0-9\.\-]*\).*/\1/'`
        if [[ -z $TEST_HOST_STRING ]]; then
            export TEST_HOST_STRING=$API_SERVER_HOST_STRING
            export TEST_HOST_PASSWORD=$API_SERVER_HOST_PASSWORD
        fi
        export TEST_HOST_IP=`echo $TEST_HOST_STRING | cut -d @ -f2`
        export TEST_HOST_USER=`echo $TEST_HOST_STRING | cut -d @ -f1`
        export TEST_RUN='contrail-test'
        setup_testnode || die "test node setup failed"
        run_fab "install_test_repo"
        install_dep_pkgs_for_test
        run_sanity_simple || die "run_sanity_simple failed"
    else
        run_fab "install_test_repo"
        install_dep_pkgs_for_test
        run_sanity || die "Run_sanity step failed"
    fi

echo "Test Done"
collect_tech_support || die "Task to collect logs/cores failed"
echo "Ending test on $TBFILE_NAME"
unlock_testbed $TBFILE_NAME
