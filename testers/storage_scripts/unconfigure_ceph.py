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
import disk

if __name__ == '__main__' :

  try:
      arg = {}
      test_obj = test_lib.lib(arg)
      testbed_config = test_obj.argument['testbed_config']['testbed_config']
      test_conf      = test_obj.argument['test_conf']['test_conf']

      profile_name = test_conf['profile_name']

      for host in testbed_config['%s,hosts_list'%profile_name] :
         node = testbed_config['%s,node_name'%host]
         test_obj.argument['%s_handle'%node] = test_obj.create_ssh_handle(node_name=node,ntp_update=True,run_time=test_conf['runtime'])

      fab_node_host = testbed_config['%s,fab_node'%profile_name]
      fab_node = testbed_config['%s,node_name'%fab_node_host]

      fab_node_handle = test_obj.argument['%s_handle'%fab_node]
      fab_node_prompt = testbed_config['%s,prompt'%fab_node]

      ostack.delete_all_vms(test_obj,fab_node_handle,fab_node_prompt,True)

      kwargs = {}
      kwargs['handle']      = fab_node_handle
      kwargs['prompt']      = fab_node_prompt
      kwargs['volume_name'] = ""
      kwargs['test_obj'] = test_obj

      ostack.delete_cinder_volume(kwargs)

      cmd = "cd /opt/contrail/utils/"
      output = gen_lib.send_cmd(test_obj,fab_node_handle,cmd,fab_node_prompt,10)
      cmd = "fab unconfigure_storage"
      output = gen_lib.send_cmd(test_obj,fab_node_handle,cmd,fab_node_prompt,300)
      
      if re.search('ERROR: cmd:.*timed-out',output) or re.search('Abort',output):
        msg = "ERROR: fab unconfigure_storage command timed out"
        gen_lib.Print(msg)
        test_obj.argument['err_msg'] += msg

      if re.search('Abort',output):
        msg = "ERROR: fab unconfigure command aborted."
        gen_lib.Print(msg)
        test_obj.argument['err_msg'] += msg
      
      cmd = "ceph -s"
      ceph_output = gen_lib.send_cmd(test_obj,fab_node_handle,cmd,fab_node_prompt,60)

      if re.search('Error initializing cluster client: Error',ceph_output):
        msg = "INFO : ceph got unconfigured correctly."
        gen_lib.Print(msg)
      else :
        msg = "ERROR : ceph did not get unconfigure correctly."
        gen_lib.Print(msg)
        test_obj.argument['err_msg'] += msg

      cinder_type_list = ostack.get_cinder_type_list(test_obj,fab_node_handle,fab_node_prompt)
       
      if len(cinder_type_list) == 0 :
        msg = "INFO : cinder type list is empty as expected."
        gen_lib.Print(msg)
      else:
        msg = "ERROR cinder type list is not empty after fab unconfigure."
        gen_lib.Print(msg)
        test_obj.argument['err_msg'] += msg

  except :
      traceback.print_exc()
      test_obj.argument['err_msg'] += "Exception seen"

  test_obj.PostResult()
  test_obj.cleanup()
