#!/usr/bin/python2.7

import subprocess
import json
import sys
import paramiko
import time
import pdb

CLUSTER='test-cluster'
KERNEL_VERSION='3.13.0-106'
cmd='server-manager-client display server --cluster_id ' + CLUSTER + ' -d --json'
data = subprocess.check_output(cmd, shell=True)
data_as_json = json.loads(data)
result=0
for each_server in data_as_json['server']:
    server_id=each_server['id']
    server_ip=each_server['ip_address']
    #password=each_server['password']
    password='c0ntrail123'
    sshc = paramiko.SSHClient()
    sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshc.connect(server_ip, username='root', password=password)
    sshc_stdin, sshc_stdout, sshc_stderr = sshc.exec_command('uname -r')
    error=sshc_stderr.read()
    if error == '':
        output=sshc_stdout.read()
    else:
        print "failed to get kernel version on the node: %s" % error
        sys.exit(-1)
    sshc.close()

    if 'kernel_version' in each_server['parameters']:
        if each_server['parameters']['kernel_version'] in output:
            print "Kernel upgrade to proper version"
            result=result+1
        else:
            print "Kernel upgrade check failed"
            sys.exit(-1)
    else:
        if KERNEL_VERSION in output:
            print "Kernel upgrade to proper version"
            result=result+1
        else:
            print "Kernel upgrade check failed"
            sys.exit(-1)

if (result != 0) and (result == len(data_as_json['server'])):
    print "Kernel upgrade passed on all servers"
    sys.exit(0)
else:
    print "Kernel upgrade failed on servers"
    sys.exit(-1)

