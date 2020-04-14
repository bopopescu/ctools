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
         test_obj.argument['%s_handle'%node] = test_obj.create_ssh_handle(node_name=node,ntp_update=True)

      fab_node_host = testbed_config['%s,fab_node'%profile_name]
      fab_node = testbed_config['%s,node_name'%fab_node_host]

      fab_node_handle = test_obj.argument['%s_handle'%fab_node]
      fab_node_prompt = testbed_config['%s,prompt'%fab_node]

      host_name = testbed_config['%s,new_compute_storage_host_name'%profile_name]
      node = testbed_config['%s,node_name'%host_name]
      new_compute_storage_node_ip = testbed_config['%s,ip'%node]
      stgy_handle = test_obj.create_ssh_handle(node_name=node)
      stgy_prompt = testbed_config['%s,prompt'%node]
      ceph.ExecuteSetupStorage(test_obj,stgy_handle,stgy_prompt)

      testbed_file = testbed_config['%s,testbed_file2,loc'%profile_name]
      ceph.update_testbed_file(test_obj,fab_node_handle,testbed_file,globals())

      cmd = "cd /opt/contrail/utils"
      output = gen_lib.send_cmd(test_obj,fab_node_handle,cmd,testbed_config['%s,prompt'%fab_node],10)

      cmd = "fab upgrade_kernel_node:%s"%new_compute_storage_node_ip
      output = gen_lib.send_cmd(test_obj,fab_node_handle,cmd,testbed_config['%s,prompt'%fab_node],900)

      cmd = "reboot"
      output = gen_lib.send_cmd(test_obj,stgy_handle,cmd,stgy_prompt,60)
      time.sleep(300)

      stgy_handle = test_obj.create_ssh_handle(node_name=node)
      stgy_prompt = testbed_config['%s,prompt'%node]

      cmd = "fab add_vrouter_node:root@%s"%new_compute_storage_node_ip
      output = gen_lib.send_cmd(test_obj,fab_node_handle,cmd,testbed_config['%s,prompt'%fab_node],900)

      if re.search('Abort',output):
        gen_lib.Print("ERROR: %s Aborted"%cmd)
        test_obj.argument['err_msg'] += "ERROR: fab add_vroute_node failed.\n"
        sys.exit()

      cmd = "fab add_storage_node:root@%s"%new_compute_storage_node_ip
      output = gen_lib.send_cmd(test_obj,fab_node_handle,cmd,testbed_config['%s,prompt'%fab_node],1200)

      if re.search('Abort',output):
        gen_lib.Print("ERROR: %s Aborted"%cmd)
        test_obj.argument['err_msg'] += "ERROR: fab add_storage_node failed.\n"
        sys.exit()

      test_obj.argument['exp_osd_map_count']        = testbed_config['%s,osd_count,2'%profile_name]
      test_obj.argument['expected_monitor_ip_list'] = testbed_config['%s,mon_ip,2'%profile_name]

      handle   = test_obj.create_ssh_handle(node_name=fab_node)
      prompt   = testbed_config['%s,prompt'%fab_node]

      ceph.check_ceph_status(test_obj,handle,prompt)

  except :
      traceback.print_exc()
      test_obj.argument['err_msg'] += "Exception seen"

  test_obj.PostResult()
  test_obj.cleanup()
