echo "Creating new Sources.list file ....."

mv /etc/apt/sources.list /etc/apt/sources.list.old
echo "deb [arch=amd64] http://us.archive.ubuntu.com/ubuntu trusty-updates main universe " >> /etc/apt/sources.list
echo "deb [arch=amd64] http://us.archive.ubuntu.com/ubuntu trusty main universe" >> /etc/apt/sources.list

echo "============\n"

echo "Install all the pre-reqs .....\n"
echo "============\n"
echo ""
apt-get update
apt-get install -y wget git bridge-utils python python-pip tmux apt-transport-https software-properties-common vim sshpass

echo "Install Virtual Box .....\n"
echo "============\n"
echo ""
wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb http://download.virtualbox.org/virtualbox/debian `lsb_release -cs` contrib"
sudo apt-get update
sudo apt-get -y install virtualbox-5.2

echo "Install Vagrant .....\n"
echo "============\n"
echo ""
wget https://releases.hashicorp.com/vagrant/2.1.1/vagrant_2.1.1_x86_64.deb
dpkg -i vagrant_2.1.1_x86_64.deb
sudo apt-get update

echo "Install Ansible .....\n"
echo "============\n"
echo ""
sudo apt-add-repository ppa:ansible/ansible -y
sudo apt-get update
sudo apt-get -y install ansible
pip install --upgrade pip
sudo apt-get update

echo "Add Centos-7.5 Box to vagrant .....\n"
echo "============\n"
echo ""
vagrant box add qarham/CentOS7.5-350GB
vagrant box list

sleep 10
echo "Create Bridge Interfaces .....\n"
echo "============\n"
echo ""
python ztp_automation.py basic_details.json create_bridge_interfaces >> /etc/network/interfaces
ifdown -a; ifup -a

sleep 10
echo "============\n"
echo ""
echo "Transfer a;; the Vagrant files from the build server"
cd /root
sshpass -p "soumilk123" scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r soumilk@10.84.5.39:/users/soumilk/vagrant/vagrant .
host_name="$(hostname)"
temp_path="/root/vagrant/"
path=$temp_path$host_name"/"
echo "Path Where the vagrant files are stored is "$path
cd $path

sleep 5
vagrant up
echo "Done !!!!!!"
echo "+++++++++++++++"
 
