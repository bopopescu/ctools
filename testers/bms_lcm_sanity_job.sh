#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}
source $TOOLS_WS/testers/utils
source $TOOLS_WS/testers/smgr_utils
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
  #initialize_any_vms
fi
reimage_using_smgr_simple || die "failed to reimage"
build_version_string || die "version string couldn't be built"
copy_and_edit_yaml_file || die "failed to copy and edit yaml file"
copy_contrail_tools_to_target || die "failed to copy contrail-tools to target"
install_prelim_pkgs_on_target || die "failed to install pre reqs on target"
configure_static_routes || die "failed to configure static routes"
provision_setup_ansible || die "failed to provision setup"
configure_static_configs || die "failed to configure mtu configuration"
run_sanity_ansible || die "failed to run sanity"
generate_core_email
unlock_testbed $TBFILE_NAME
