#!/bin/sh

sleep $2
for i in {0..119} # Try for 60 min and exit.
do
  result=$(docker exec contrail_command bash -c "export CONTRAIL_CONFIG='/etc/contrail/contrail.yml'; contrailcli show contrail_cluster $1 | grep 'provisioning_state'" | cut -d ' ' -f6)
  if [[ "$result" == "CREATED" ]] || [[ "$result" == "UPDATED" ]] ; then
    echo "Cluster Extention to public cloud SUCCESSFUL"
    exit 0
  fi
  sleep 30
done
echo "Cluster Extention to public cloud FAILED"
