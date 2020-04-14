#!/usr/bin/python
import traceback
import commands
import pdb
import os
import sys
import re
import time
import telnetlib
from threading import Thread

import test_lib
import gen_lib
import os_lib
import ostack
import ceph


if __name__ == '__main__' :

  try:
     arg = {}
     test_obj = test_lib.lib(arg)
     testbed_config = test_obj.argument['testbed_config']['testbed_config']
     test_conf      = test_obj.argument['test_conf']['test_conf']

     profile_name = test_conf['profile_name']
     fab_node_host = testbed_config['%s,fab_node'%profile_name]
     fab_node = testbed_config['%s,node_name'%fab_node_host]

     fab_node_handle   = test_obj.create_ssh_handle(node_name=fab_node,ntp_update=True)
     fab_node_prompt   = testbed_config['%s,prompt'%fab_node]

     src_ip     = testbed_config['sm_node,ip']
     src_login  = testbed_config['sm_node,login']
     src_passwd = testbed_config['sm_node,password']

     src_file = "%s/multi_chassis_internal.py"%os.getcwd()

     dest = "/tmp/multi_chassis_internal.py"

     status = test_obj.remote_scp_from(fab_node_handle,fab_node_prompt,src_file,src_ip,src_login,src_passwd,dest)
     if not status :
           test_obj.argument['err_msg'] += "test_obj.remote_scp for %s failed"%src_file
           sys.exit(1)

     cmd = "python %s"%dest
     output = gen_lib.send_cmd(test_obj,fab_node_handle,cmd,fab_node_prompt,1200)

     ret = re.search('TOTAL_OBJECT:(\d+),TEST_STATUS:(\S+)',output)
     if ret and int(ret.group(1)) != 0 and ret.group(2) == 'True' :
          print "INFO: multi-chassis configuration working fine."
     else:
          msg =  "ERROR: multi-chassis configuration failed"
          print msg
          test_obj.argument['err_msg'] += msg

  except SystemExit:
     pass
     
  except Exception:

     traceback.print_exc()
     test_obj.argument['err_msg'] += 'ERROR: exception seen'
  test_obj.PostResult()
  test_obj.cleanup()

  if test_obj.argument['err_msg'] == "" :
    sys.exit(0)
  else:
    sys.exit(1)

