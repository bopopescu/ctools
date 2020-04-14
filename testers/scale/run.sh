
#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}
# AVAILABLE_TESTBEDS is a comma separated list of testbed filenames or paths
source $TOOLS_WS/testers/utils
testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"


get_testbed

exec_cmds -s ${API_SERVER_HOST_STRING} -p ${API_SERVER_HOST_PASSWORD} -c "mkdir /tmp/run"
sshpass -p $API_SERVER_HOST_PASSWORD scp ${SSHOPT} $TOOLS_WS/testers/scale/scale_test.py $TOOLS_WS/testers/scale/lib.py  ${API_SERVER_HOST_STRING}:/tmp/run/
result=`exec_cmds -s ${API_SERVER_HOST_STRING} -p ${API_SERVER_HOST_PASSWORD} -c "rm -f /tmp/last_cmd_status;source /etc/contrail/openstackrc;cd /tmp/run;python scale_test.py --sm_node_ip $SM_NODE_IP --n_tenants $NUM_OF_TENANTS --n_vns $NUM_OF_VNS --n_vms $NUM_OF_VMS --cleanup $ENABLE_CLEANUP"`
result=`exec_cmds -s ${API_SERVER_HOST_STRING} -p ${API_SERVER_HOST_PASSWORD} -c "cat /tmp/last_cmd_status"`

result=`echo $result | sed 's/\\r//g'`
if [ "$result" != '0' ]; then
        echo "ERROR: scale test failed"
        exit 1
else
    echo "PASS: scale test passed"
fi


unlock_testbed $TBFILE_NAME

