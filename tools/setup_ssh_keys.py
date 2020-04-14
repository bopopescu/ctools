#----------------- 
# From the testbed file, enable automatic ssh login
# usage: python setup_ssh_keys.py <path of testbed.py>
#----------------
import os
import sys
import imp
from fabric.api import *

testbed_path = sys.argv[1]
testbed = imp.load_source('testbed', testbed_path)

env.disable_known_hosts = True
# Read pub file content
pub_file = os.path.expanduser('~/.ssh/id_rsa.pub')
if not os.path.isfile(pub_file):
    # Generate ssh-keys
    local('ssh-keygen -f ~/.ssh/id_rsa -t rsa -N \'\'')
id_rsa_pub = open('%s' %(pub_file), 'r').read().strip()

for host_string in testbed.env.roledefs['all']:
    (u, host) = host_string.split('@')
    with settings(host_string=host_string, password=env.passwords[host_string]):
        run('mkdir -p .ssh ; chmod 700 .ssh')

		# Ensure that pub key is present
        auth_file = '~/.ssh/authorized_keys'
        run('grep -q -F "%s" %s || echo "%s" >> %s' %(id_rsa_pub, auth_file,
            id_rsa_pub, auth_file))

		# Check and update known_hosts
        keyscan = local('ssh-keyscan -H %s' %(host), capture=True)

        known_hosts = ''
        if os.path.isfile('~/.ssh/known_hosts'):
            known_hosts = open(os.path.expanduser('~/.ssh/known_hosts'), 'r').read()
        if not keyscan in known_hosts:
            print 'Adding host %s in known_hosts' %(host)
            local('echo "%s" >> ~/.ssh/known_hosts' %(keyscan))
