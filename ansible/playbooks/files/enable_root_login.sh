#!/bin/bash -eux
sudo sed -e '/PermitRootLogin/ s/^#*/#/' -i /etc/ssh/sshd_config
sudo sed '/^#PermitRootLogin/a PermitRootLogin yes' -i /etc/ssh/sshd_config
sudo sed -i '/^#ListenAddress 0.0.0.0/s/^#//' -i /etc/ssh/sshd_config
sudo sed '/^#PasswordAuthentication/a PasswordAuthentication yes' -i /etc/ssh/sshd_config
sleep 5
sudo service sshd restart
echo "root:c0ntrail123" | sudo chpasswd
sudo iptables -F 
