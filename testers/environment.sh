#!/usr/bin/env bash
export TBFILE
# Both TEST_HOST_STRING AND TEST_HOST_PASSWORD would be set from utils in case they are not provided
export TEST_HOST_STRING=${TEST_HOST_STRING}
export TEST_HOST_PASSWORD=${TEST_HOST_PASSWORD}
export API_SERVER_HOST_STRING=${API_SERVER_HOST_STRING:-"root@127.0.0.1"}
export TOOLS_WS=${TOOLS_WS:-$PWD}

# Set the below 4 variables if PKG_FILE is not set
export BRANCH=${BRANCH:-mainline}
export BUILDID=${BUILDID:-LATEST}
export DISTRO=${DISTRO:-"ubuntu-12-04"}
export VCENTER_TEST_SKU=${VCENTER_TEST_SKU:-liberty}
if [[  $VCENTER_ONLY_TESTBED -eq 1 ]]; then
    export TEST_SKU=$VCENTER_TEST_SKU
else
    export TEST_SKU=${SKU:-icehouse}
fi
##
# TEST_RUN_INFRA: to specify where the test is run, possible values are
# docker: using docker container for test run
# legacy: Run legacy contrail-test - this is applicable for R2.x branches
##
if [[ $BRANCH =~ ^R[12]\. ]]; then
    export TEST_RUN_INFRA='legacy'
else
    export TEST_RUN_INFRA='docker'
fi
export TEST_RUN=${TEST_RUN:-'contrail-test'}
export TEST_CONTAINER_IMAGE=${TEST_CONTAINER_IMAGE:-''}

export TEST_CONTAINER_IMAGE_DIR=${TEST_CONTAINER_IMAGE_DIR:-"/github-build/${BRANCH}/${BUILDID}/${DISTRO}/${TEST_SKU}/artifacts/"}
# If BRANCH, BUILID, DISTRO, SKU are not defined,
# PKG_FILE path needs to be set
export PKG_FILE

#--------
# For Tempest
# You can override these from the results of 'fab export_testbed_details' task
export KEYSTONE_SERVICE_HOST_USER=${KEYSTONE_SERVICE_HOST_USER:-root}
export KEYSTONE_SERVICE_HOST_PASSWORD=${KEYSTONE_SERVICE_HOST_PASSWORD:-c0ntrail123}
export API_SERVER_IP=`echo $API_SERVER_HOST_STRING | cut -d @ -f2`
export API_SERVER_HOST_USER=`echo $API_SERVER_HOST_STRING | cut -d @ -f1`
export API_SERVER_HOST_PASSWORD=${API_SERVER_HOST_PASSWORD:-c0ntrail123}
#-------

export SKIP_REIMAGE=${SKIP_REIMAGE:-0}
export SKIP_KERNEL_UPGRADE=${SKIP_KERNEL_UPGRADE:-0}
export SKIP_BRINGUP=${SKIP_BRINGUP:-0}
export SKIP_ZONES=${SKIP_ZONES:-0}
export SKIP_SOURCELIST=${SKIP_SOURCELIST:-0}
export SKIP_SANITY=${SKIP_SANITY:-0}
export SKIP_LOGS_COLLECTION=${SKIP_LOGS_COLLECTION:-0}
# Skip running tempest by default
export SKIP_TEMPEST=${SKIP_TEMPEST:-1}

export SKIP_SM_PROVISION=${SKIP_SM_PROVISION:-0}
export SMLITE_REGRESSION=${SMLITE_REGRESSION:-0}
export SM_SERVER_PASSWORD=${SM_SERVER_PASSWORD:-c0ntrail123}

# set this flag to use contrail-cloud-pkgs.
export USE_CLOUD_PKG=${USE_CLOUD_PKG:-0}

# set this flag to use contrail-networking-pkgs.
export USE_NETWORKING_PKG=${USE_NETWORKING_PKG:-0}

# Enable tests which depend on public network connectivity
export MX_GW_TEST=${MX_GW_TEST:-0}

# By default, new test infra enables serial run. To force it to run in parallel 
export PARALLEL_RUN=${PARALLEL_RUN:-0}

# Knob to add basic images (fab add_basic_images) before the test run
export ADD_IMAGES=${ADD_IMAGES:-0}

# Knob to add basic flavors (fab add_basic_flavors) before the test run
export ADD_FLAVORS=${ADD_FLAVORS:-0}

# Location can be REMOTE or LOCAL 
# If REMOTE, reimage command will be triggered from TASK_RUNNER_HOST_STRING
export TESTBED_LOCATION=${TESTBED_LOCATION:-"LOCAL"}
export ESXI_ONLY_TESTBED=${ESXI_ONLY_TESTBED:-0}
export VCENTER_ONLY_TESTBED=${VCENTER_ONLY_TESTBED:-0}
export VCENTER_AS_COMPUTE_TESTBED=${VCENTER_AS_COMPUTE_TESTBED:-0}

#Wait random time before generating SCRIPT_TIMESTAMP
sleep $[ ( $RANDOM % 3 )  + 1 ]s
#
#if [[ -v BUILD_TAG ]] //This is not compatible with bash 4.1 (used in US jenkins server)
if [[ "$BUILD_TAG" != "" ]]
then
    export SCRIPT_TIMESTAMP=${BUILD_TAG}
    echo $SCRIPT_TIMESTAMP
else
    export SCRIPT_TIMESTAMP=`date +"%Y_%m_%d_%H_%M_%S"`
    echo $SCRIPT_TIMESTAMP
fi
     
export SSHOPT="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "
export NODEHOME=${NODEHOME:-/root}
export FAB_GIT_BRANCH=${BRANCH:-master}
export PARAMS_FILE=${PARAMS_FILE:-${NODEHOME}/contrail-test/scripts/sanity_params.ini}
export TEST_CONFIG_FILE=${TEST_CONFIG_FILE:-${NODEHOME}/contrail-test/sanity_params.ini}

# NOTE: in case of docker, TEST_RUN_CMD is used only when one need to run non-standard set of tests
if [[ $TEST_RUN_INFRA == 'legacy' ]]; then
    export TEST_RUN_CMD=${TEST_RUN_CMD:-"bash -x run_tests.sh -m -U -s "}
fi

export BUILD_SCRIPT_PATH=$TOOLS_WS/contrail-test
export FABRIC_SCRIPT_PATH='$TOOLS_WS/contrail-fabric-utils'
export RUN_WITHIN_VENV=0
export EMAIL_SUBJECT_PREFIX=${EMAIL_SUBJECT_PREFIX:-""}

# Location where locks are maintained for testbeds
export LOCK_FILE_DIR=${LOCK_FILE_DIR:-/cs-shared/testbed_locks}

# Location of Server Manager client used to reimage nodes.
export SMGR_CLIENT=${SMGR_CLIENT:-/cs-shared/server-manager/client/server-manager}

# Folder where debug logs/cores etc. are put
export DEBUG_LOG_DIR=${DEBUG_LOG_DIR:-/cs-shared/test_runs}

if [ ${BRANCH} == "mainline" ]; then
    FAB_GIT_BRANCH='master'
fi

lsb_dist=''

###########
# For usage outside Juniper, they need to make sure 
# a) fab and test code are copied to cfgm node 
# b) testbed.py should have env.test_repo_dir populated to point to contrail-test code
# c) CFGM_FAB_PATH and CFGM_TEST_CODE_PATH are updated
# d) JUNIPER_INTRANET is set to 0
#
# The default path for fab code is ~/fabric-utils

export CFGM_FAB_PATH=${CFGM_FAB_PATH:-${NODEHOME}/fabric-utils}
export CFGM_TEST_CODE_PATH=${CFGM_TEST_CODE_PATH:-${NODEHOME}/contrail-test}
export JUNIPER_INTRANET=${JUNIPER_INTRANET:-1}

export IMAGE_WEB_SERVER=${IMAGE_WEB_SERVER:-"10.204.217.158"}

# Choose whether to release the testbed on completion or not
# Default is to release
export RELEASE_TESTBED=${RELEASE_TESTBED:-1}

# Set test type to be one of daily/regression.
# Used by contrail-test/tools/upload_to_webserver.py
export TEST_TYPE=${TEST_TYPE:-daily}

# Incase reimage/bringup fails, locks the testbed for debugging 
# if the below variable is set. Default behavior is not to lock
export LOCK_TESTBED_ON_FAILURE=${LOCK_TESTBED_ON_FAILURE:-0}

# Kernel package for setting up Redhat nodes
export REDHAT_KERNEL_PACKAGE=${REDHAT_KERNEL_PACKAGE:-"/cs-shared/builder/cache/redhatenterpriselinuxserver70/icehouse/kernel-3.10.0-123.el7.0contrail.x86_64.rpm"}

# Choose whether to use the task-runner node for running fab cmds
# Typically used when we want to invoke tasks locally on a remote testbed
export USE_TASK_RUNNER_HOST=${USE_TASK_RUNNER_HOST:-0}
export TASK_RUNNER_HOST_STRING=${TASK_RUNNER_HOST_STRING:-stack@10.84.24.64}
export TASK_RUNNER_HOST_PASSWORD=${TASK_RUNNER_HOST_PASSWORD:-c0ntrail123}

# Set this flag if you need to pick latest contrail-test code instead of 
# the contrail-test artifact from the build
# Default is to pick test code from build-artifacts path
export USE_LATEST_TEST_CODE=${USE_LATEST_TEST_CODE:-0}

# Defaults for some test environment
export STACK_USER=${STACK_USER:-""}
export STACK_PASSWORD=${STACK_PASSWORD:-""}
export STACK_TENANT=${STACK_TENANT:-""}
export TENANT_ISOLATION=${TENANT_ISOLATION:-""}
export MAIL_TO=${MAIL_TO:-"dl-contrail-sw@juniper.net"}
export WEBSERVER_HOST=${WEBSERVER_HOST:-"10.204.216.50"}
export WEBSERVER_USER=${WEBSERVER_USER:-"bhushana"}
export WEBSERVER_PASSWORD=${WEBSERVER_PASSWORD:-"c0ntrail!23"}
export WEBSERVER_LOG_PATH=${WEBSERVER_LOG_PATH:-"/home/bhushana/Documents/technical/logs"}
export WEBSERVER_REPORT_PATH=${WEBSERVER_REPORT_PATH:-"/home/bhushana/Documents/technical/sanity"}
export WEBROOT=${WEBROOT:-"Docs/logs"}
export MAIL_SERVER=${MAIL_SERVER:-"10.204.216.49"}
export MAIL_PORT=${MAIL_PORT:-"25"}
export FIP_POOL_NAME=${FIP_POOL_NAME:-""}
export PUBLIC_VIRTUAL_NETWORK=${PUBLIC_VIRTUAL_NETWORK:-""}
export PUBLIC_TENANT_NAME=${PUBLIC_TENANT_NAME:-"admin"}
export FIXTURE_CLEANUP=${FIXTURE_CLEANUP:-"yes"}
export GENERATE_HTML_REPORT=${GENERATE_HTML_REPORT:-"True"}
export KEYPAIR_NAME=${KEYPAIR_NAME:-"contrail_key"}
export MAIL_SENDER=${MAIL_SENDER:-"contrailbuild@juniper.net"}
export DISCOVERY_IP=${DISCOVERY_IP:-""}
export CONFIG_API_IP=${CONFIG_API_IP:-""}
export ANALYTICS_API_IP=${ANALYTICS_API_IP:-""}
export DISCOVERY_PORT=${DISCOVERY_PORT:-""}
export CONFIG_API_PORT=${CONFIG_API_PORT:-""}
export ANALYTICS_API_PORT=${ANALYTICS_API_PORT:-""}
export CONTROL_PORT=${CONTROL_PORT:-""}
export DNS_PORT=${DNS_PORT:-""}
export AGENT_PORT=${AGENT_PORT:-""}
export USER_ISOLATION=${USER_ISOLATION:-"True"}

# Enable installation of some required packages on compute nodes
# for few tests to be runnable
# Default mode is enabled(1)
export INSTALL_EXTRA_PKG_ON_NODES=${INSTALL_EXTRA_PKG_ON_NODES:-1}
export USE_LATEST_ANSIBLE_CODE=${USE_LATEST_ANSIBLE_CODE:-0}

# CONTRAIL_TEST_CODE_PATH is the folder where both contrail-test and
# contrail-test-ci repo folder are present
export CONTRAIL_TEST_CODE_PATH=${CONTRAIL_TEST_CODE_PATH:-$TOOLS_WS}

# Tempest repo to use
export TEMPEST_REPO=${TEMPEST_REPO:-"https://github.com/Juniper/tempest.git"}
