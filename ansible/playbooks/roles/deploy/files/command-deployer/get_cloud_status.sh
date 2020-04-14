#!/bin/sh

sleep $2
for i in {0..79} # Try for 40 min and exit.
do
  result=$(docker exec contrail_command bash -c "export CONTRAIL_CONFIG='/etc/contrail/contrail.yml'; contrailcli show cloud $1 | grep 'provisioning_state'" | cut -d ' ' -f6)
  if [[ "$result" == "CREATED" ]] || [[ "$result" == "UPDATED" ]] ; then
    echo "Cloud Create/Update SUCCESSFUL"
    exit 0
  fi
  sleep 30
done
echo "Cloud Create/Update FAILED"
