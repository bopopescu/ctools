#!/usr/bin/bash

TOOLS_WS=/root/contrail-tools
DEFAULT_TEST_YAML=contrail_test_input.yaml
UNDERCLOUD_PASSWORD=contrail123
UNDERCLOUD_STACK_USER=stack
UNDERCLOUD_STACK_HOME=/home/stack
UNDERCLOUD_IP=$1
UNDERCLOUD_REG=$2
YAML=$3
AGENT_MODE=$4
CONTRAIL_REG_INSECURE=$5
CONTRAIL_REGISTRY=$6
VERSION=$7
NTP_SERVER=$8
SKIP_COPY_EDIT_YAML=$9
VLAN_1=${10}
VLAN_2=${11}
VLAN_3=${12}
VLAN_4=${13}
SRIOV_INT=${14}
SKIP_DEL_OF_CONTRAIL_HEAT_TEMP=${15}
INS_DIR='--insecure-registry'

sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/${YAML}_${AGENT_MODE} ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/${DEFAULT_TEST_YAML}
sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/update_test_yaml.py ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/
sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/get_server_ip.sh ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/
sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/deploy.sh ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/
sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP "chmod +x get_server_ip.sh"
if [ ${SKIP_COPY_EDIT_YAML} -eq 0 ]
then

    if [ ${SKIP_DEL_OF_CONTRAIL_HEAT_TEMP} -eq 0 ]
    then
        sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
            rm -rf contrail-tripleo-heat-templates
	        git clone https://github.com/juniper/contrail-tripleo-heat-templates -b stable/queens
	 )"
    fi
    
    sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
        rm -rf tripleo-heat-templates
        rm -f /tmp/contrail_container.yaml
        cp -r /usr/share/openstack-tripleo-heat-templates/ tripleo-heat-templates
        cp -r contrail-tripleo-heat-templates/* tripleo-heat-templates/
        
        ~/tripleo-heat-templates/tools/contrail/import_contrail_container.sh -f /tmp/contrail_container.yaml -r ${CONTRAIL_REGISTRY}/contrail-nightly -i 1 -t ${VERSION}
        openstack --debug overcloud container image upload --config-file  /tmp/contrail_container.yaml --verbose 2>&1 | tee -a upload-image-${VERSION}.log
        echo MASTER
        sed -i '/  ContrailRegistryInsecure: /a \  ContrailRegistryInsecure: ${CONTRAIL_REG_INSECURE}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/ContrailRegistryInsecure: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        sed -i '/  DockerInsecureRegistryAddress: /a \  DockerInsecureRegistryAddress: ${UNDERCLOUD_REG} ${INS_DIR} ${CONTRAIL_REGISTRY}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/DockerInsecureRegistryAddress: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        sed -i '/#  ContrailRegistry:/d' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '/  ContrailRegistry: /a \  ContrailRegistry: ${UNDERCLOUD_REG}/contrail-nightly' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/ContrailRegistry: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        sed -i '/#  ContrailImageTag:/d' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '/  ContrailImageTag: /a \  ContrailImageTag: ${VERSION}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/ContrailImageTag: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        sed -i '/  ControllerCount: /a \  ControllerCount: 3' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ControllerCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        sed -i '/  ContrailControllerCount: /a \  ContrailControllerCount: 3' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ContrailControllerCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        sed -i '/  NtpServer: /a \  NtpServer: ${NTP_SERVER}' tripleo-heat-templates/environments/contrail/contrail-net.yaml
        sed -i '0,/NtpServer: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-net.yaml
        echo '  ContrailAnalyticsDBMinDiskGB: 40' >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
        echo '  AdminPassword: c0ntrail123' >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
        echo '  AAAMode: rbac' >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
    )"
    if [ ${VLAN_1} -ne '710' ]
    then    
        sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
        sed -i '/  InternalApiNetworkVlanID: /a \  InternalApiNetworkVlanID: ${VLAN_1}' tripleo-heat-templates/environments/contrail/contrail-net_aio.yaml
        sed -i '0,/InternalApiNetworkVlanID: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-net_aio.yaml
        sed -i '/  InternalApiNetworkVlanID: /a \  InternalApiNetworkVlanID: ${VLAN_1}' tripleo-heat-templates/environments/contrail/contrail-net.yaml
        sed -i '0,/InternalApiNetworkVlanID: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-net.yaml
        sed -i '/  ExternalNetworkVlanID: /a \  ExternalNetworkVlanID: ${VLAN_2}' tripleo-heat-templates/environments/contrail/contrail-net_aio.yaml
        sed -i '0,/ExternalNetworkVlanID: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-net_aio.yaml
        sed -i '/  ExternalNetworkVlanID: /a \  ExternalNetworkVlanID: ${VLAN_2}' tripleo-heat-templates/environments/contrail/contrail-net.yaml
        sed -i '0,/ExternalNetworkVlanID: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-net.yaml
        sed -i '/  StorageNetworkVlanID: /a \  StorageNetworkVlanID: ${VLAN_3}' tripleo-heat-templates/environments/contrail/contrail-net_aio.yaml
        sed -i '0,/StorageNetworkVlanID: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-net_aio.yaml
        sed -i '/  StorageNetworkVlanID: /a \  StorageNetworkVlanID: ${VLAN_3}' tripleo-heat-templates/environments/contrail/contrail-net.yaml
        sed -i '0,/StorageNetworkVlanID: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-net.yaml
        sed -i '/  StorageMgmtNetworkVlanID: /a \  StorageMgmtNetworkVlanID: ${VLAN_4}' tripleo-heat-templates/environments/contrail/contrail-net_aio.yaml
        sed -i '0,/StorageMgmtNetworkVlanID: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-net_aio.yaml
        sed -i '/  StorageMgmtNetworkVlanID: /a \  StorageMgmtNetworkVlanID: ${VLAN_4}' tripleo-heat-templates/environments/contrail/contrail-net.yaml
        sed -i '0,/StorageMgmtNetworkVlanID: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-net.yaml
    ) "
    fi

    #sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/contrail-config-database.yaml ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/tripleo-heat-templates/docker/services/contrail/contrail-config-database.yaml
    #sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/contrail-analytics-database.yaml ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/tripleo-heat-templates/docker/services/contrail/contrail-analytics-database.yaml
    if [ ${AGENT_MODE} == 'kernel' ]
    then 
        sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/compute-nic-config.yaml ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/tripleo-heat-templates/network/config/contrail/compute-nic-config.yaml
        sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
        sed -i '/  ComputeCount: /a \  ComputeCount: 3' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ComputeCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '/  ContrailSriovCount: /a \  ContrailSriovCount: 0' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ContrailSriovCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '/  ContrailDpdkCount: /a \  ContrailDpdkCount: 0' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ContrailDpdkCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        ) "
    elif [ ${AGENT_MODE} == 'dpdk' ]
    then
        sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/contrail-dpdk-nic-config.yaml ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/tripleo-heat-templates/network/config/contrail/contrail-dpdk-nic-config.yaml
        sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
        sed -i '/  ContrailDpdkCount: /a \  ContrailDpdkCount: 3' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ContrailDpdkCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        sed -i '/  ContrailDpdkHugepages1GB: /a \  ContrailDpdkHugepages1GB: 32' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ContrailDpdkHugepages1GB: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        
        sed -i '/  ComputeCount: /a \  ComputeCount: 0' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ComputeCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml        
        sed -i '/  ContrailSriovCount: /a \  ContrailSriovCount: 0' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ContrailSriovCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        ) "
    elif [ ${AGENT_MODE} == 'sriov' ]
    then
        sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/contrail-dpdk-nic-config.yaml ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/tripleo-heat-templates/network/config/contrail/contrail-dpdk-nic-config.yaml
        sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/compute-nic-config.yaml ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/tripleo-heat-templates/network/config/contrail/compute-nic-config.yaml
        sshpass -p ${UNDERCLOUD_PASSWORD} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${TOOLS_WS}/yamls/rhosp13/contrail-sriov-nic-config.yaml ${UNDERCLOUD_STACK_USER}@${UNDERCLOUD_IP}:${UNDERCLOUD_STACK_HOME}/tripleo-heat-templates/network/config/contrail/contrail-sriov-nic-config.yaml
        sshpass -p ${UNDERCLOUD_PASSWORD} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${UNDERCLOUD_STACK_USER} $UNDERCLOUD_IP " (
        sed -i '/  ContrailSriovCount: /a \  ContrailSriovCount: 3' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ContrailSriovCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        sed -i '/  ContrailSriovHugepages1GB: /a \  ContrailSriovHugepages1GB: 10' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ContrailSriovHugepages1GB: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        
        sed -i '/  ComputeCount: /a \  ComputeCount: 0' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ComputeCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '/  ContrailDpdkCount: /a \  ContrailDpdkCount: 0' tripleo-heat-templates/environments/contrail/contrail-services.yaml
        sed -i '0,/  ContrailDpdkCount: /{//d;}' tripleo-heat-templates/environments/contrail/contrail-services.yaml

        echo '  NovaPCIPassthrough:' >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
        echo '    - devname: \"${SRIOV_INT}\"' >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
        echo '      physical_network: \"sriov1\"' >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
        echo '  ContrailSriovNumVFs: [\"${SRIOV_INT}:7\"]' >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
) "
    fi
fi
