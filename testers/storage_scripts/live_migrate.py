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

def configure_livem(test_obj,handle,prompt,fab_node) :

    testbed_config = test_obj.argument['testbed_config']['testbed_config']
    test_conf      = test_obj.argument['test_conf']['test_conf']

    cmd = "mkdir /store"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

    src_ip     = testbed_config['regression,ip']
    src_login  = testbed_config['regression,login']
    src_passwd = testbed_config['regression,password']

    src_file   = test_conf['ceph_nfs_image_src']
    dest       = "/store"

    status = test_obj.remote_scp_from(handle,testbed_config['%s,prompt'%fab_node],src_file,src_ip,src_login,src_passwd,dest)
    if not status :
      test_obj.argument['err_msg'] += "test_obj.remote_scp for %s failed"%src_file
      sys.exit()


    cmd = "cd /store"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)
   
    d,f = os.path.split(test_conf['ceph_nfs_image_src'])
    cmd = "rm -rf livemnfs.qcow2"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,300)
    cmd = "gunzip %s"%f
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,300)

    cmd = "cd /opt/contrail/utils"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

    live_migration_enabled = False

    #args = {}
    #args['handle'] = handle
    #args['prompt'] = prompt
    #args['tenant_name'] = 'admin'
    #args['tenant_id'] = ostack.get_tenant_id(args)
    #args['quota'] = 1600
    #ostack.set_cinder_quota(args)

    for i in xrange(3):

      cmd = "fab setup_nfs_livem_global"
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,900)

      if re.search('Abort',output):
        test_obj.argument['warn_msg'] += "WARNING: fab setup_nfs_livem_global aborted and re-tried"
        gen_lib.Print("ERROR: %s Aborted"%cmd)
        cmd = "umount /var/lib/nova/instances/global"
        output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
      else:
        live_migration_enabled = True
        break
    if not live_migration_enabled:
       test_obj.argument['err_msg'] += "ERROR: fab setup_nfs_live_migration aborted more than once"
       sys.exit()

def live_migrate(test_obj,handle,prompt):

  testbed_config = test_obj.argument['testbed_config']['testbed_config']
  test_conf = test_obj.argument['test_conf']['test_conf']

  domain_name = "englab.juniper.net"

  vm_name = "VM1"
  vm_id = ostack.get_vm_id(test_obj,handle,prompt,vm_name)
  current_hostname1 = ostack.get_vm_hostinfo(test_obj,handle,prompt,vm_name) 
  current_hostname1 = current_hostname1.rsplit("." + domain_name)[0]
  new_host = ""
  compute_host_list = ceph.get_storage_host_list(test_obj,handle,prompt)
  print compute_host_list,current_hostname1
  for host in compute_host_list:
     host = host.rsplit("." + domain_name)[0]
     print host,current_hostname1
     if host != current_hostname1 :
       new_host = host
       break 

  print "Current host:",current_hostname1
  print "New host:",new_host
  ostack.live_migrate_vm(test_obj,handle,prompt,vm_id,new_host)

  time.sleep(60)

  args = {}
  args['handle']     = handle
  args['prompt']     = prompt
  args['test_obj']   = test_obj
  args['vm_name']    = "VM1"
  args['status'] = "ACTIVE"
  args['power_state'] = "Running"
  args['timeout']     = 600
  ostack.wait_until_vm_status(args)


  current_hostname2 = ostack.get_vm_hostinfo(test_obj,handle,prompt,vm_name) 
  current_hostname2 = current_hostname2.rsplit("." + domain_name)[0]
  new_host = new_host.rsplit("." + domain_name)[0]

  if current_hostname2 == new_host :
    gen_lib.Print("PASS: Live-migration working...")
  else:
    test_obj.argument['err_msg'] += "ERROR: Live-migration is not working...\n"
    gen_lib.Print("FAIL: Live-migration is not working...")

def deploy_vm(test_obj,handle,prompt):

  test_conf = test_obj.argument['test_conf']['test_conf']

  url =  test_conf['linux_vm_image_url']
  d,f = os.path.split(url)
  dest = "/tmp/%s"%f

  gen_lib.wget_file(test_obj,handle,prompt,url,dest,600) 

  ostack.init_credentials(test_obj,handle,prompt)

  args = {}
  args['handle']     = handle
  args['prompt']     = prompt
  args['image_name'] = "ubuntu"
  args['disk_format'] = 'raw'
  args['is_public']   = True
  args['container_format'] = "ovf"
  args['image']            = dest
  args['test_obj']         = test_obj

  ostack.delete_all_vms(test_obj,handle,prompt)
  #ostack.delete_vm(test_obj,handle,prompt,"VM1")

  ostack.delete_glance_image(args)
  ostack.add_glance_image(args)
  ostack.delete_neutron_net(test_obj,handle,prompt,'VN1')
  net_id = ostack.create_neutron_net(test_obj,handle,prompt,'VN1')
  ostack.create_neutron_subnet(test_obj,handle,prompt,'VN1','VN1','192.168.1.0/24')

  ostack.add_security_rules(test_obj,handle,prompt)

  args['flavor']     = "m1.medium"
  args['vm_name']    = "VM1"
  args['net_id']     = net_id
  args['security-groups'] = "default"
  ostack.boot_nova_image(args)

  args['status'] = "ACTIVE"
  args['power_state'] = "Running"
  args['timeout']     = 600
  ostack.wait_until_vm_status(args)

if __name__ == '__main__' :

  try:
    arg = {}
    test_obj = test_lib.lib(arg)
    testbed_config = test_obj.argument['testbed_config']['testbed_config']
    test_conf      = test_obj.argument['test_conf']['test_conf']

    profile_name = test_conf['profile_name']
    
    runtime = test_conf['runtime']

    if testbed_config['%s,live_migration'%profile_name] == False :
       print "INFO : live_migration test cannot be done in this testbed.skipping the test."
       test_obj.PostResult()
       test_obj.cleanup()
       sys.exit() 
      
    if testbed_config.has_key('%s,local_only_disks'%profile_name) and testbed_config['%s,local_only_disks'%profile_name] :
       print "INFO : local_only_disks.livem will not work.skipping the test."
       test_obj.PostResult()
       test_obj.cleanup()
       sys.exit() 
     
    fab_node_host = testbed_config['%s,fab_node'%profile_name]
    fab_node = testbed_config['%s,node_name'%fab_node_host]

    fab_node_handle   = test_obj.create_ssh_handle(node_name=fab_node,ntp_update=True,run_time=test_conf['runtime'])

    if runtime == "FAB":
      configure_livem(test_obj,fab_node_handle,testbed_config['%s,prompt'%fab_node],fab_node)

    ostack.init_credentials(test_obj,fab_node_handle,testbed_config['%s,prompt'%fab_node])

    deploy_vm(test_obj,fab_node_handle,testbed_config['%s,prompt'%fab_node])
    live_migrate(test_obj,fab_node_handle,testbed_config['%s,prompt'%fab_node])
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

