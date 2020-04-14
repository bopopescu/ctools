contrail_build_no=$1
# Uninstall pip packages namely docker-py and docker
pip uninstall docker-py docker

# Install Docker 
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce-18.03.1.ce
systemctl start docker

# Allow Docker to connect to private insecure registry
echo '{"insecure-registries": ["ci-repo.englab.juniper.net:5010", "10.84.5.81:5010"]}' > /etc/docker/daemon.json
systemctl restart docker

# Pull contrail command docker container
export CCD_IMAGE=10.84.5.81:5010/contrail-command-deployer:5.0-357
docker pull $CCD_IMAGE

# Get instances.yaml anc command_server.yaml file used for provisioning
yum install -y sshpass
sshpass -p "c0ntrail123" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@10.87.70.9:/root/ztp-auto-files/provisioning_files/ztp_cc_command_servers.yml /root/command_servers.yml
sshpass -p "c0ntrail123" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null  root@10.87.70.9:/root/ztp-auto-files/provisioning_files/ztp_instances.yml /root/instances.yml

# Change build number in instances.yaml file and command_server.yaml file
sed -i 's/__CONTRAILBUILD__/'${contrail_build_no}'/' /root/command_servers.yml
sed -i 's/__CONTRAILBUILD__/'${contrail_build_no}'/' /root/instances.yml

# export variables for contrail_command.yaml and instances.yaml for provisioning 
export COMMAND_SERVERS_FILE=/root/command_servers.yml
export INSTANCES_FILE=/root/instances.yml

# Start Greenfield cluster Provision. This will bringup the contrail command ui and provision the contrail cluster
docker run -t --net host -e action=provision_cluster -v $COMMAND_SERVERS_FILE:/command_servers.yml -v $INSTANCES_FILE:/instances.yml -d --privileged --name contrail_command_deployer $CCD_IMAGE

#Docker logs for installing the contrail command UI
docker logs -f contrail_command_deployer


# Docker Logs for Contrail Provisioning
sleep 10
docker exec -it contrail_command tail -f /var/log/ansible.log


