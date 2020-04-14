#!/usr/bin/bash
hyperviser_ip=$1
hyperviser_pass=$2
nic_uc=$3
nic1_c0=$4
nic2_c0=$5
nic1_c1=$6
nic2_c1=$7
nic1_c2=$8
nic2_c2=$9
vlan_0=${10}
vlan_1=${11}
vlan_2=${12}
vlan_3=${13}
vlan_4=${14}
vlan_5=${15}
controller0_ip=${16}
controller1_ip=${17}
controller2_ip=${18}
controller_pass=${19}

 
sshpass -p ${hyperviser_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${hyperviser_ip} "(
  systemctl start libvirtd
  systemctl start openvswitch

) "

sshpass -p ${hyperviser_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${hyperviser_ip} " (
  ovs-vsctl add-br br0
  ovs-vsctl add-port br0 ${nic_uc}

) "

sshpass -p ${hyperviser_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${hyperviser_ip} " (
cat << EOF > br0.xml
<network>
  <name>br0</name>
  <forward mode='bridge'/>
  <bridge name='br0'/>
  <virtualport type='openvswitch'/>
  <portgroup name='overcloud'>
    <vlan trunk='yes'>
      <tag id='${vlan_0}' nativeMode='untagged'/>
      <tag id='${vlan_1}'/>
      <tag id='${vlan_2}'/>
      <tag id='${vlan_3}'/>
      <tag id='${vlan_4}'/>
      <tag id='${vlan_5}'/>
    </vlan>
  </portgroup>
</network>
EOF
) "

sshpass -p ${hyperviser_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${hyperviser_ip} " (
virsh net-define br0.xml
virsh net-start br0
virsh net-autostart br0

)"


sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller0_ip} "(
systemctl start libvirtd
systemctl start openvswitch
iptables -I INPUT 1 -i eno1 -p udp -j ACCEPT
) "

sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller0_ip} "(
ovs-vsctl add-br br0
ovs-vsctl add-br br1
ovs-vsctl add-port br0 ${nic1_c0} 
ovs-vsctl add-port br1 ${nic2_c0} 

) "


sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller1_ip} "(
systemctl start libvirtd
systemctl start openvswitch
iptables -I INPUT 1 -i eno1 -p udp -j ACCEPT

) "

sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller1_ip} "(
ovs-vsctl add-br br0
ovs-vsctl add-br br1
ovs-vsctl add-port br0 ${nic1_c1}
ovs-vsctl add-port br1 ${nic2_c1}

) "


sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller2_ip} "(
systemctl start libvirtd
systemctl start openvswitch
iptables -I INPUT 1 -i eno1 -p udp -j ACCEPT

) "

sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller2_ip} "(
ovs-vsctl add-br br0
ovs-vsctl add-br br1
ovs-vsctl add-port br0 ${nic1_c2}
ovs-vsctl add-port br1 ${nic2_c2}

) "

sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller0_ip} "(
cat << EOF > br0.xml
<network>
  <name>br0</name>
  <forward mode='bridge'/>
  <bridge name='br0'/>
  <virtualport type='openvswitch'/>
  <portgroup name='overcloud'>
    <vlan trunk='yes'>
      <tag id='${vlan_0}' nativeMode='untagged'/>
      <tag id='${vlan_1}'/>
      <tag id='${vlan_2}'/>
      <tag id='${vlan_3}'/>
      <tag id='${vlan_4}'/>
      <tag id='${vlan_5}'/>
    </vlan>
  </portgroup>
</network>
EOF
cat << EOF > br1.xml
<network>
  <name>br1</name>
  <forward mode='bridge'/>
  <bridge name='br1'/>
  <virtualport type='openvswitch'/>
</network>
EOF

) "

sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller1_ip} "(
cat << EOF > br0.xml
<network>
  <name>br0</name>
  <forward mode='bridge'/>
  <bridge name='br0'/>
  <virtualport type='openvswitch'/>
  <portgroup name='overcloud'>
    <vlan trunk='yes'>
      <tag id='${vlan_0}' nativeMode='untagged'/>
      <tag id='${vlan_1}'/>
      <tag id='${vlan_2}'/>
      <tag id='${vlan_3}'/>
      <tag id='${vlan_4}'/>
      <tag id='${vlan_5}'/>
    </vlan>
  </portgroup>
</network>
EOF
cat << EOF > br1.xml
<network>
  <name>br1</name>
  <forward mode='bridge'/>
  <bridge name='br1'/>
  <virtualport type='openvswitch'/>
</network>
EOF

) "

sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller2_ip} "(
cat << EOF > br0.xml
<network>
  <name>br0</name>
  <forward mode='bridge'/>
  <bridge name='br0'/>
  <virtualport type='openvswitch'/>
  <portgroup name='overcloud'>
    <vlan trunk='yes'>
      <tag id='${vlan_0}' nativeMode='untagged'/>
      <tag id='${vlan_1}'/>
      <tag id='${vlan_2}'/>
      <tag id='${vlan_3}'/>
      <tag id='${vlan_4}'/>
      <tag id='${vlan_5}'/>
    </vlan>
  </portgroup>
</network>
EOF
cat << EOF > br1.xml
<network>
  <name>br1</name>
  <forward mode='bridge'/>
  <bridge name='br1'/>
  <virtualport type='openvswitch'/>
</network>
EOF

) "

sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller0_ip} "(
virsh net-define br0.xml
virsh net-start br0
virsh net-autostart br0
virsh net-define br1.xml
virsh net-start br1
virsh net-autostart br1

) "

sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller1_ip} "(
virsh net-define br0.xml
virsh net-start br0
virsh net-autostart br0
virsh net-define br1.xml
virsh net-start br1
virsh net-autostart br1

) "

sshpass -p ${controller_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${controller2_ip} "(
virsh net-define br0.xml
virsh net-start br0
virsh net-autostart br0
virsh net-define br1.xml
virsh net-start br1
virsh net-autostart br1

) "
