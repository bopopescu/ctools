#!/bin/sh
set -x -v

if [ "$2" != "fresh" ];then
  service contrail-server-manager stop
  dpkg -l | grep contrail | awk -F ' ' '{print $2}' | xargs dpkg -P
  dpkg -l | grep puppet | awk -F ' ' '{print $2}' | xargs dpkg -P
  dpkg -l | grep cobbler | awk -F ' ' '{print $2}' | xargs dpkg -P
  dpkg -l | grep passenger | awk -F ' ' '{print $2}' | xargs dpkg -P
  rm -rf /etc/contrail_smgr/contrail-centos-repo /etc/contrail_smgr/contrail-redhat-repo /var/www/html/thirdparty_packages /opt/contrail/ /var/log/contrail /etc/cobbler/pxe /srv/www/cobbler/ /var/lib/cobbler/ /usr/src/contrail/contrail-web-core/webroot/img /etc/puppet/ /var/lib/puppet /usr/share/puppet /etc/contrail_smgr /etc/contrail /var/log/contrail
  rm -rf  /usr/bin/server-manager /usr/bin/server-manager-client /opt/contrail/bin/server-manager-client
  rm -rf /etc/apt/sources.list.d/*.list
  a2dismod passenger
  apt-get update > /dev/null 2>&1
  dpkg -l | grep contrail
  dpkg -l | grep puppet
  dpkg -l | grep cobbler
  rm -rf /var/lib/cobbler /var/lib/puppet /etc/puppet /etc/cobbler /etc/contrail* /opt/contrail/contrail_server_manager /opt/contrail/server_manager/sm-config.ini
fi
while [ "`lsof /var/lib/dpkg/lock`" ];do echo "waiting for dpkg lock to get freed"; sleep 5; done
dpkg -i $1
cd /opt/contrail/contrail_server_manager/
./setup.sh --all 
#cp /root/sm_files/dhcp.template /etc/cobbler/dhcp.template
service contrail-server-manager start
