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

    fab_node_host = testbed_config['%s,fab_node'%profile_name]
    fab_node = testbed_config['%s,node_name'%fab_node_host]
   
    fab_node_handle   = test_obj.create_ssh_handle(node_name=fab_node,ntp_update=True,run_time=test_conf['runtime'])

    ostack.init_credentials(test_obj,fab_node_handle,testbed_config['%s,prompt'%fab_node])

    output = gen_lib.send_cmd(test_obj,fab_node_handle,"ceph -s","#",120)
    print output
    if testbed_config['%s,osd_count'%profile_name] == -1 :
      if re.search('Error initializing cluster client: Error',output):
        msg = "PASS : ceph status is correct.Error seen due to local-only disks or nfs-only disks"
        print msg
      else:
        msg = "ERROR : ceph status is incorrect.supposed to see \"Error initializing cluster client: Error\""
        print msg
        test_obj.argument['err_msg'] += msg
        sys.exit(1)
    else:
       ret = re.search('HEALTH_WARN|HEALTH_OK|HEALTH_ERR',output)
       if ret and ret.group(0) in ['HEALTH_WARN','HEALTH_OK'] :
          print "CEPH health status is OK"
       else:
          print "CEPH health status is NOT OK"
          test_obj.argument['err_msg'] += "CEPH health status is NOT OK"
          sys.exit(1)

       if re.search('mons down',output):
          msg = "ERROR: some mons process is down."
          print msg
          test_obj.argument['err_msg'] += msg
          sys.exit(1)
          
       if re.search('stuck|degraded|unclean|undersized',output):
          msg = "ERROR: ceph status has issue."
          print msg
          test_obj.argument['err_msg'] += msg
          sys.exit(1)
          
       out = re.search('mons at.*',output).group()
       ret = re.findall('=(.*?):',out)
       ret.sort()
       expected_mon_list = testbed_config['%s,mon_ip'%profile_name]
       expected_mon_list.sort()
       print ret,expected_mon_list
       if ret == expected_mon_list :
           print "INFO: mon IP is correct"
       else:
           print "ERROR: mon IP list is not correct"
           test_obj.argument['err_msg'] += "ERROR: mon IP list is not correct"
           sys.exit(1)

       exp_osd_map_count = testbed_config['%s,osd_count'%profile_name]
       ret = re.search('osdmap .*: (\d+) osds: (\d+) up, (\d+) in',output)
       if ret and ( int(ret.group(1)) == int(exp_osd_map_count) ) and ( int(ret.group(2)) == int(exp_osd_map_count) ) and ( int(ret.group(1)) == int(exp_osd_map_count) ) :
          msg = "INFO: ceph status is PASS and osd count is PASS and all osds are up\n"
          print msg
       else :
          msg = "ERROR: ceph status is NOT OK, osdmap count does not match"
          print msg
          test_obj.argument['err_msg'] += msg
          sys.exit(1)

    print "CEPH_STATUS_CHECK_OK"


    cinder_type_list = ostack.get_cinder_type_list(test_obj,fab_node_handle,testbed_config['%s,prompt'%fab_node])
    cinder_type_list.sort()

    config_cinder_type_list = testbed_config['%s,cinder_volume_types'%profile_name][:]
    config_cinder_type_list.sort()

    if cinder_type_list == config_cinder_type_list :
      print "PASS : cinder type-list pass\n"
    else:
      msg =  "ERROR : cinder type-list failed\n"
      print msg
      print "Expected cinder type-list",config_cinder_type_list
      print "Actual cinder type-list",cinder_type_list

      test_obj.argument['err_msg'] += msg


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

