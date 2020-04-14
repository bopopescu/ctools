#!/usr/bin/bash
control_num=1
contrail_num=3
ip=10.204.217.128
libvirt_images=/home/libvirt_images
mkdir ${libvirt_images}
root_password=contrail123
ipmi_port=16230
rm -f ironic_list
for num in `seq 0 $((${control_num} - 1))`
do
	virsh destroy control_${num}
	virsh undefine control_${num}
	vbmc delete control_${num}
	virsh vol-delete ${libvirt_images}/control_${num}.qcow2
	qemu-img create -f qcow2 ${libvirt_images}/control_${num}.qcow2 100G
	virt-install --name control_${num} --disk ${libvirt_images}/control_${num}.qcow2 --vcpus=4 --ram=32768 --network network=br0,model=virtio,portgroup=overcloud --network network=br1,model=virtio --virt-type kvm --cpu host --import --os-variant rhel7 --serial pty --console pty,target_type=virtio --print-xml > control_${num}.xml
	virsh define control_${num}.xml
	vbmc add control_${num} --port $((${ipmi_port} + 2 * ${num} + 1)) --username ADMIN --password ADMIN
	vbmc start control_${num} > /dev/null
	prov_mac=`virsh domiflist control_${num}|grep br0 |awk '{print $5}'`
	port=`vbmc show control_${num}| grep port|awk '{print $4}'`
	echo ${prov_mac} control_${num} ${ip} control ${port} >> ironic_list
done
for num in `seq 0 $((${contrail_num} - 1))`
do
	 virsh destroy contrail-controller_${num}
	 virsh undefine contrail-controller_${num}
	 virsh vol-delete ${libvirt_images}/contrail-controller_${num}.qcow2
	 vbmc delete contrail-controller_${num}
	 qemu-img create -f qcow2 ${libvirt_images}/contrail-controller_${num}.qcow2 200G
	 virt-install --name contrail-controller_$num --disk ${libvirt_images}/contrail-controller_${num}.qcow2 --vcpus=4 --ram=32768 --network network=br0,model=virtio,portgroup=overcloud --network network=br1,model=virtio --virt-type kvm --cpu host --import --os-variant rhel7 --serial pty --console pty,target_type=virtio --print-xml > contrail-controller_${num}.xml
	 virsh define contrail-controller_${num}.xml
	 vbmc add contrail-controller_${num} --port $((${ipmi_port} + 2 * ${num})) --username ADMIN --password ADMIN
	 vbmc start contrail-controller_${num} > /dev/null
	 prov_mac=`virsh domiflist contrail-controller_${num}|grep br0 |awk '{print $5}'`
	 port=`vbmc show contrail-controller_${num}| grep port|awk '{print $4}'`
	 echo ${prov_mac} contrail-controller_${num} ${ip} contrail-controller ${port} >> ironic_list
 done
 iptables -I INPUT 1 -i eno1 -p udp -j ACCEPT
