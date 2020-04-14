#!/usr/bin/bash
cloud_image=~/images/rhel-server-7.7-x86_64-kvm.qcow2
libvirt_images=/home/libvirt_images
mkdir ${libvirt_images}
undercloud_name=$9
undercloud_suffix=local
root_password=contrail123
stack_password=contrail123
stack_user=stack
export LIBGUESTFS_BACKEND=direct
redat_user=$1
redhat_password=$2
redhat_pool=$3
contrail_registry=$4
undercloud_reg=$5
contrail_tag=$6
vlan_2=$7
activation_key=$8

virsh destroy ${undercloud_name}
virsh undefine ${undercloud_name}
virsh vol-delete ${libvirt_images}/${undercloud_name}.qcow2

qemu-img create -f qcow2 ${libvirt_images}/${undercloud_name}.qcow2 500G
virt-resize --expand /dev/sda1 ${cloud_image} ${libvirt_images}/${undercloud_name}.qcow2
virt-customize  -a ${libvirt_images}/${undercloud_name}.qcow2 --run-command 'xfs_growfs /' --root-password password:${root_password} --hostname ${undercloud_name}.${undercloud_suffix} --run-command 'useradd stack' --password stack:password:${stack_password} --run-command 'echo "stack ALL=(root) NOPASSWD:ALL" | tee -a /etc/sudoers.d/stack' --chmod 0440:/etc/sudoers.d/stack --run-command 'sed -i "s/PasswordAuthentication no/PasswordAuthentication yes/g" /etc/ssh/sshd_config' --run-command 'systemctl enable sshd' --run-command 'yum remove -y cloud-init' --selinux-relabel

virt-install --name ${undercloud_name} --disk ${libvirt_images}/${undercloud_name}.qcow2 --vcpus=8 --ram=32768 --network network=default,model=virtio --network network=br0,model=virtio,portgroup=overcloud --virt-type kvm --import --os-variant rhel7 --graphics vnc --serial pty --noautoconsole --console pty,target_type=virtio

virsh start ${undercloud_name}
sleep 30
undercloud_ip=`virsh domifaddr ${undercloud_name} |grep ipv4 |awk '{print $4}' |awk -F"/" '{print $1}'`

sshpass -p ${root_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${undercloud_ip} " (
    sed -i '/nameserver/i\nameserver 172.21.200.60' /etc/resolv.conf
    hostnamectl set-hostname ${undercloud_name}.${undercloud_suffix}
    hostnamectl set-hostname --transient ${undercloud_name}.${undercloud_suffix}
    echo ${undercloud_ip} ${undercloud_name}.${undercloud_suffix} ${undercloud_name} >> /etc/hosts
    #sudo subscription-manager register --username ${redat_user} --password ${redhat_password} --force
    #sudo subscription-manager attach --pool ${redhat_pool} 
    curl --insecure --output katello-ca-consumer-latest.noarch.rpm https://noden14.englab.juniper.net/pub/katello-ca-consumer-latest.noarch.rpm
    yum localinstall -y katello-ca-consumer-latest.noarch.rpm
    sudo subscription-manager unregister
    sudo subscription-manager register --activationkey=${activation_key} --org=BLR_RHOSP
    sudo subscription-manager attach --pool 8a4c58186e3f113601707ac13a087b80
    sleep 10s
    subscription-manager repos --enable=rhel-7-server-rpms --enable=rhel-7-server-rh-common-rpms --enable=rhel-ha-for-rhel-7-server-rpms --enable=rhel-7-server-openstack-13-rpms --enable=rhel-7-server-extras-rpms
    yum install -y python-tripleoclient tmux
    yum -y update
) "
sshpass -p ${root_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${undercloud_ip} " (
    reboot &
) "

sleep 10 

sshpass -p ${root_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${undercloud_ip} "sed -i '/nameserver/i\nameserver 172.21.200.60' /etc/resolv.conf"
ret=$?
if [ $ret != 0 ];
then
    echo "undercloud is not ready for ssh connections, waiting till it's ready.."
fi
while [[ $ret != 0 ]]
do
    sshpass -p ${root_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${undercloud_ip} "sed -i '/nameserver/i\nameserver 172.21.200.60' /etc/resolv.conf"
    ret=$?
done
echo "undercloud is ready for ssh connections"

sshpass -p ${stack_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${stack_user} ${undercloud_ip} " (
    cp /usr/share/instack-undercloud/undercloud.conf.sample ~/undercloud.conf
    openstack --debug undercloud install 2>&1 | tee -a undercloud_install.log
) "

sshpass -p ${stack_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${stack_user} ${undercloud_ip} "ls -l stackrc"
ret=$?
if [ $ret != 0 ];
then
    echo "Undercloud installation itself failed"
    exit 1
fi

sshpass -p ${stack_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${stack_user} ${undercloud_ip} " (
    source stackrc
    sudo iptables -A FORWARD -i br-ctlplane -o eth0 -j ACCEPT
    sudo iptables -A FORWARD -i eth0 -o br-ctlplane -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
) "

subnet_id=`sshpass -p ${stack_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${stack_user} ${undercloud_ip} " (
    source stackrc
    openstack subnet show ctlplane-subnet -c id -f value
) "`

sshpass -p ${stack_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${stack_user} ${undercloud_ip} " (
    source stackrc
    openstack subnet set ${subnet_id} --dns-nameserver 8.8.8.8 --dns-nameserver 172.21.200.60
    sudo ip link add name vlan${vlan_2} link br-ctlplane type vlan id ${vlan_2}
    sudo ip addr add 10.2.0.254/24 dev vlan${vlan_2}
    sudo ip link set dev vlan${vlan_2} up
    echo vlan${vlan_2}
    echo vlan${vlan_2}
    echo ${vlan_2}
    echo vlan${vlan_2}
    mkdir images
    sudo yum install -y rhosp-director-images rhosp-director-images-ipa
    tar -xvf /usr/share/rhosp-director-images/overcloud-full-latest-13.0.tar -C images
    tar -xvf /usr/share/rhosp-director-images/ironic-python-agent-latest-13.0.tar -C images
    openstack --debug overcloud image upload --image-path /home/stack/images/ 2>&1 | tee -a image_upload.log
    newgrp docker &
) "

sshpass -p ${stack_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${stack_user} ${undercloud_ip} " (
    source stackrc
    openstack overcloud container image prepare --push-destination=192.168.24.1:8787 --tag-from-label {version}-{release} --output-images-file ~/local_registry_images.yaml --namespace=registry.access.redhat.com/rhosp13 --prefix=openstack- --tag-from-label {version}-{release} --output-env-file ~/overcloud_images.yaml
) "

sshpass -p ${stack_password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l ${stack_user} ${undercloud_ip} " (
    source stackrc
    sudo sed -i 's/^INSECURE_REGISTRY=.*/INSECURE_REGISTRY=\"--insecure-registry ${contrail_registry} --insecure-registry ${undercloud_reg}\"/' /etc/sysconfig/docker
    sudo systemctl restart docker
    cp -r /usr/share/openstack-tripleo-heat-templates/ tripleo-heat-templates       
    git clone https://github.com/juniper/contrail-tripleo-heat-templates -b stable/queens
    cp -r contrail-tripleo-heat-templates/* tripleo-heat-templates/
    openstack --debug overcloud container image upload --config-file ~/local_registry_images.yaml --verbose 2>&1 | tee -a upload-image.log
)"
