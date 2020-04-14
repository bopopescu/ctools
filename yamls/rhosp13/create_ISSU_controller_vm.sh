#!/usr/bin/bash
contrail_issu_num=3
ip=10.204.217.124
libvirt_images=/home/libvirt_images
mkdir ${libvirt_images}
root_password=contrail123
ipmi_port=16240
rm -f ironic_list
for num in `seq 0 $((${contrail_issu_num} - 1))`
do
	virsh destroy contrail-controller-issu_${num}
	virsh undefine contrail-controller-issu_${num}
	virsh vol-delete ${libvirt_images}/contrail-controller-issu_${num}.qcow2
	vbmc delete contrail-controller-issu_${num}
	qemu-img create -f qcow2 ${libvirt_images}/contrail-controller-issu_${num}.qcow2 200G
        virt-install --name contrail-controller-issu_$num --disk ${libvirt_images}/contrail-controller-issu_${num}.qcow2 --vcpus=4 --ram=32768 --network network=br0,model=virtio,portgroup=overcloud --network network=br1,model=virtio --virt-type kvm --cpu host --import --os-variant rhel7 --serial pty --console pty,target_type=virtio --print-xml > contrail-controller-issu_${num}.xml
	virsh define contrail-controller-issu_${num}.xml
	vbmc add contrail-controller-issu_${num} --port $((${ipmi_port} + 2 * ${num})) --username ADMIN --password ADMIN
	vbmc start contrail-controller-issu_${num} > /dev/null
	prov_mac=`virsh domiflist contrail-controller-issu_${num}|grep br0 |awk '{print $5}'`
	port=`vbmc show contrail-controller-issu_${num}| grep port|awk '{print $4}'`
	echo ${prov_mac} contrail-controller-issu_${num} ${ip} contrail-controller-issu ${port} >> ironic_list
done
iptables -I INPUT 1 -i eno1 -p udp -j ACCEPT
