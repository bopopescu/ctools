#!/usr/bin/bash

num=$1
ip=$2
#Create VM's disk image
libvirt_images=/home/libvirt_images
mkdir ${libvirt_images}
root_password=contrail123
ipmi_port_controller=$((16230+2*$num))
ipmi_port_control=$(($ipmi_port_controller+1))
rm -f ironic_list
for i in control contrail-controller
do
    virsh destroy ${i}_${num} 
    virsh undefine ${i}_${num} 
    virsh vol-delete ${libvirt_images}/${i}_${num}.qcow2
done

for i in control contrail-controller
do
    qemu-img create -f qcow2 ${libvirt_images}/${i}_${num}.qcow2 300G
    virt-install --name ${i}_$num --disk ${libvirt_images}/${i}_${num}.qcow2 --vcpus=16 --ram=32768 --network network=br0,model=virtio,portgroup=overcloud --network network=br1,model=virtio --virt-type kvm --cpu host --import --os-variant rhel7 --serial pty --console pty,target_type=virtio --print-xml > ${i}_${num}.xml
    virsh define ${i}_${num}.xml
done

vbmc delete contrail-controller_${num}
vbmc delete control_${num}
vbmc add contrail-controller_${num} --port ${ipmi_port_controller} --username ADMIN --password ADMIN
vbmc add control_${num} --port ${ipmi_port_control} --username ADMIN --password ADMIN
vbmc start contrail-controller_${num} > /dev/null
vbmc start control_${num} > /dev/null

#Create ironic_list file
for i in control contrail-controller
do
 prov_mac=`virsh domiflist ${i}_${num}|grep br0 |awk '{print $5}'`
 port=`vbmc show ${i}_${num}| grep port|awk '{print $4}'`
 echo ${prov_mac} ${i}_${num} ${ip} ${i} ${port} >> ironic_list
done
