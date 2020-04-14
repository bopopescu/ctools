#!/usr/bin/python
import sys
import traceback
import os
import re

import ceph
import os_lib
import test_lib
import ostack
import time
import gen_lib

if __name__ == '__main__' :

  try:
    arg = {}
    test_obj = test_lib.lib(arg)
    testbed_config = test_obj.argument['testbed_config']['testbed_config']
    test_conf      = test_obj.argument['test_conf']['test_conf']

    profile_name = test_conf['profile_name']
    hosts_list  = testbed_config['%s,hosts_list'%profile_name]

    for host in hosts_list :

     node_name = testbed_config['%s,node_name'%host] 
     handle = test_obj.create_ssh_handle(node_name=node_name)
     prompt = testbed_config['%s,prompt'%node_name]

     cmd = "service ntp stop"
     output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,120,True,False)
     cmd = "service ntp start"
     output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,120,True,False)
    
  except SystemExit:
     pass
  except :
    traceback.print_exc()
    test_obj.argument['err_msg'] += "Exception occured"

  test_obj.PostResult()
  test_obj.cleanup()
  if test_obj.argument['err_msg'] == "" :
    sys.exit(0)
  else:
    sys.exit(1)

