export BUILDID=13
export BRANCH=1912
echo "BRANCH is $BRANCH"
export SKU=queens
export BUILD_ISSU=1912.20-rhel

export DISTRO=redhat7.7-reg
export JENKINS_TRIGGERED=1
export LOCK_TESTBED_ON_FAILURE=1

export HYPERVISOR_IP=10.204.216.228
export HYPERVISOR_PASSWORD=c0ntrail123
export UNDERCLOUD_IP=$UNDERCLOUD_IP
export UNDERCLOUD_STACK_USER=stack
export UNDERCLOUD_PASSWORD=contrail123
export UNDERCLOUD_STACK_HOME=/home/stack

export CONTROLLER_HYPERVISORS="10.204.217.134 10.204.217.136 10.204.217.116"
export COMPUTES_MACS="10.207.25.169,00:25:90:e7:81:6e 10.207.25.203,00:25:90:e7:7f:aa"

export REDHAT_USER=kkaushal1
export REDHAT_PASSWORD=conTr@il
export REDHAT_POOL=8a85f99368b9397d01690f03af335fdf

export UNDERCLOUD_REG=192.168.24.1:8787
export CONTRAIL_REGISTRY=10.204.217.152:5000
#export CONTRAIL_REGISTRY=10.84.5.81:5010
export CONTRAIL_REG_INSECURE=true

export CB_SANITY=$CB_SANITY
export NTP_SERVER=10.204.217.158

export TOOLS_WS=/homes/kpatel/kpatel_proj/RHOSP/RHOSP_SANITY/ISSU/contrail-tools
export TEST_RUN_INFRA='docker'
export AVAILABLE_TESTBEDS=testbed_k8.py
export YAML=rhosp13-nodek8.yaml
export DEFAULT_TEST_YAML=contrail_test_input.yaml
export USE_CLOUD_PKG=$USE_CLOUD_PKG
export USE_LATEST_TEST_CODE=$USE_LATEST_TEST_CODE
export TASK_RUNNER_HOST_STRING=${TASK_RUNNER_HOST_STRING:-stack@10.204.216.49}
export TASK_RUNNER_HOST_PASSWORD=${TASK_RUNNER_HOST_PASSWORD:-stack@123}
export IMAGE_WEB_SERVER=10.204.217.158
export CT_IMAGE_WEB_SERVER=10.204.217.158
export SM_TYPE=1
export TEST_SETUP=MULTIINTERFACE

export EMAIL_SUBJECT="RHOSP13-Multi-Interface-HA-Sanity"
export WEBSERVER_HOST="10.204.216.50"
export WEBSERVER_USER="bhushana"
export WEBSERVER_PASSWORD="c0ntrail!23"
export WEBSERVER_LOG_PATH="/home/bhushana/Documents/technical/logs/"
export WEBROOT="Docs/logs"
export MAIL_SERVER="10.204.216.49"
export OS_PASSWORD=c0ntrail123

cd $TOOLS_WS

export NODE_0_IP=10.204.217.128
export NODE_1_IP=10.204.217.124
export NODE_PASS=c0ntrail123

export NIC_UC=eno2
export NIC1_N0=eno2
export NIC2_N0=enp4s0f1
export NIC1_N1=eno2
export NIC2_N1=enp4s0f1

export VLAN_0=701
export VLAN_1=711
export VLAN_2=721
export VLAN_3=731
export VLAN_4=741
export VLAN_5=751

export AGENT_MODE=dpdk
export SRIOV_INT=NA

export POOL_CLEAN=1
export SKIP_REIMAGE=1
export SKIP_PRE_UNDERCLOUD=0
export SKIP_UNDERCLOUD_REFRESH=0
export SKIP_COPY_EDIT_YAML=0
export SKIP_PROVISION=0
export SKIP_ISSU_DEPLOY=0
export SKIP_SANITY=0
export SKIP_ISSU_PREPARE=1
export SKIP_ISSU_STEP_5=1
export SKIP_ISSU_STEP_6=1
export SKIP_ISSU_STEP_7=1
export SKIP_ISSU_STEP_8=1
export SKIP_ISSU_STEP_9=1
export SKIP_ISSU_STEP_10=1
export SKIP_ISSU_STEP_11=1
export SKIP_ISSU_STEP_12=1
export SKIP_ISSU_CONVERGE=1
export SKIP_ISSU_REMOVE=1
#(undercloud) [stack@queensa common]$ vi deploy-steps.j2 -- Modify this file

export SKIP_ADD_ISO=1
export PARALLEL_RUN=1
export SKIP_TEMPEST=1
export MX_GW_TEST=0
export WEBSERVER_REPORT_PATH="/var/www/html/sanity/fb-sanity/FB-${BRANCH}-rhosp13-queens-ha-sanity"

if [ ${BRANCH} = 'latest' ]; then
	    echo "SKIP sanity for latest branch"
	        exit 0
	fi

	bash -x testers/micro_services_basic_job_rhel_issu.sh
