#!/bin/bash
virsh destroy undercloud 
virsh undefine undercloud
rm -rf  /root/.ssh/known_hosts
/usr/bin/expect <<EOD
set timeout 30000 
spawn ansible-playbook -i inventory/ playbooks/start.yml
expect "Are you sure you want to continue connecting (yes/no)?"
send "yes\r"
expect "PLAY RECAP"
send "yes\r" 
EOD
echo "Done"
