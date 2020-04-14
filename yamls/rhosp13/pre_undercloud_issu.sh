#!/usr/bin/bash
hyperviser_ip=$1
hyperviser_pass=$2
nic_uc=$3
nic1_n0=$4
nic2_n0=$5
nic1_n1=$6
nic2_n1=$7
vlan_0=$8
vlan_1=$9
vlan_2=${10}
vlan_3=${11}
vlan_4=${12}
vlan_5=${13}
node_0_ip=${14}
node_1_ip=${15}
node_pass=${16}
vlan_6=${17}

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
      <tag id='${vlan_6}'/>
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


sshpass -p ${node_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${node_0_ip} "(
systemctl start libvirtd
systemctl start openvswitch
iptables -I INPUT 1 -i eno1 -p udp -j ACCEPT
) "

sshpass -p ${node_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${node_0_ip} "(
ovs-vsctl add-br br0
ovs-vsctl add-br br1
ovs-vsctl add-port br0 ${nic1_n0} 
ovs-vsctl add-port br1 ${nic2_n0} 

) "

sshpass -p ${node_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${node_1_ip} "(
systemctl start libvirtd
systemctl start openvswitch
iptables -I INPUT 1 -i eno1 -p udp -j ACCEPT

) "

sshpass -p ${node_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${node_1_ip} "(
ovs-vsctl add-br br0
ovs-vsctl add-br br1
ovs-vsctl add-port br0 ${nic1_n1}
ovs-vsctl add-port br1 ${nic2_n1}

) "

sshpass -p ${node_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${node_0_ip} "(
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

sshpass -p ${node_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${node_1_ip} "(
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

sshpass -p ${node_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${node_0_ip} "(
virsh net-define br0.xml
virsh net-start br0
virsh net-autostart br0
virsh net-define br1.xml
virsh net-start br1
virsh net-autostart br1

) "

sshpass -p ${node_pass} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l root ${node_1_ip} "(
virsh net-define br0.xml
virsh net-start br0
virsh net-autostart br0
virsh net-define br1.xml
virsh net-start br1
virsh net-autostart br1

) "
