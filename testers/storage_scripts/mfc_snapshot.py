#!/usr/bin/python
import thread
import traceback
import commands
import pdb
import os
import sys
import pexpect
import re
import time
import telnetlib
from threading import Thread

if os.geteuid() != 0:
    os.execvp("sudo", ["sudo"] + ["python"] + sys.argv)

import test_lib
import gen_lib
import os_lib
import ostack
import ceph

def ssh_to_ip(handle,host_ip,login,password,prompt):

   cmd = "ssh %s@%s -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"%(login,host_ip)
   print cmd
   handle.sendline(cmd)
   i = handle.expect ([prompt,pexpect.EOF,pexpect.TIMEOUT,'password:'], timeout=30)
   output = handle.before
   print output,"hello:%d"%i
   if i == 3: 
      handle.sendline(password)
      i = handle.expect ([prompt,pexpect.EOF,pexpect.TIMEOUT], timeout=30)
      output = handle.before
      print "hello,",output

def exit_compute(test_obj,handle,prompt):
   
   cmd = "exit"
   gen_lib.send_cmd(test_obj,handle,cmd,prompt,60) 

def exit_mfc(test_obj,handle,prompt):
   
   cmd = "quit"
   gen_lib.send_cmd(test_obj,handle,cmd,prompt,60) 

def identify_vm_ip(test_obj,handle,prompt):

   cmd = "route -n"
   output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60) 

   ret = re.findall('(169.254\.\d+\.\d+) ',output)
   return ret

def check_disk_list(test_obj,handle,prompt):

   cmd = "show media-cache disk list"

   output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,20)

   ret = re.findall('dc_\d+\s*SAS',output)
   if len(ret) != 2 :
     err_msg = "ERROR: disk did not attach correctly to MFC\n"
     gen_lib.Print(err_msg)
     test_obj.argument['err_msg'] += err_msg

def deploy_linux_vm(test_obj,handle,prompt,host,net_id):

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
  args['test_obj'] = test_obj
  
  ostack.add_glance_image(args)
  
  args['flavor']     = "m1.medium"
  args['vm_name']    = "client"
  args['net_id']     = net_id
  #args['zone']       = host
  args['security-groups'] = "default"
  ostack.boot_nova_image(args)


  args['status'] = "ACTIVE"
  args['power_state'] = "Running"
  args['timeout']     = 600
  ret = ostack.wait_until_vm_status(args)
  if not ret :
    msg = "ERROR: %s VM did not come up correctly.timeout:%d\n"%(args['vm_name'], args['timeout'])
    print msg
    test_obj.argument['err_msg'] += msg

  time.sleep(120) # to let VM to come up fully.scp service was failing inconsistently.

def check_mfc_version(test_obj,handle,qcow_file):

     cmd = "show version"
     op = gen_lib.send_cmd(test_obj,handle,cmd,'\(config\)',30)

     d,f = os.path.split(qcow_file)
     build_id = f.split("-")[-1].strip(".qcow2")
     version = f.split("-" + build_id)[0]
     
     version_match = True
     find=re.search(".*Product release: \s*([a-z0-9_.-]+)",op,re.M)
     if find.group(1) != version :
          version_match = False
     
     find=re.search(".*Build ID: *([0-9_]*)",op,re.M)
     if find.group(1) != build_id :
          version_match = False

     return version_match

def configure_namespace(test_obj,handle,origin_ip):

    cmd = "namespace abcd origin-server http %s"%origin_ip
    gen_lib.send_cmd(test_obj,handle,cmd,'\(config\)',10)
    cmd = "namespace abcd match uri /"
    gen_lib.send_cmd(test_obj,handle,cmd,'\(config\)',10)
    cmd = "namespace abcd status active"
    gen_lib.send_cmd(test_obj,handle,cmd,'\(config\)',10)

def reboot_mfc(handle,prompt):

   handle.PROMPT=prompt

   cmd = "reload"
   handle.sendline(cmd)
   i = handle.expect ([prompt,pexpect.EOF,pexpect.TIMEOUT,'save first','Confirm reload'], timeout=10)
   output = handle.before
   print output

   if i == 3 or i == 4 :
     cmd = "yes"
     handle.sendline(cmd)
     i = handle.expect ([prompt,pexpect.EOF,pexpect.TIMEOUT,'Confirm reload'], timeout=10)
     output = handle.before
     print output

     if i == 3 :
       cmd = "yes"
       handle.sendline(cmd)
       i = handle.expect ([prompt,pexpect.EOF,pexpect.TIMEOUT,'Confirm reload'], timeout=10)
       output = handle.before
       print output

   if i == 0 :
       gen_lib.Print("INFO: vm rebooted successfully")
   else:
       msg = "ERROR: vm did not reboot correctly"
       test_obj.argument['err_msg'] += msg
     

client_complete = False

def run_http_server(test_obj,handle,file,mfc_private_ip):
    
    global client_complete
    
    gen_lib.send_cmd(test_obj,handle,"python " + file + "&",'#',30)
    time.sleep(10)
    cmd = "curl -iv http://%s/abcd[1-25000] -H \"Cache-Control:'max-age=0'\""%mfc_private_ip
    gen_lib.send_cmd(test_obj,handle,cmd,'##',1800,True,False)
    client_complete = True

def snapshot(test_obj,fab_node_handle,fab_node_prompt,vm,snapshot_name):

   cmd = "time nova image-create %s %s --poll"%(vm,snapshot_name)
   output = gen_lib.send_cmd(test_obj,fab_node_handle,cmd,fab_node_prompt,900) 
   
   if not re.search('100%\s*complete',output):
     return -1
   ret = re.search('real\s+(\d+)m(\d+)',output)
   if ret:
      snapshot_time = int(ret.group(1))*60 + int(ret.group(2))
   else:
      snapshot_time = -1
   return snapshot_time

def telnet_to_mfc(handle,mfc_ip):

   handle.expect ('.*',timeout=2)

   for i in xrange(5):
   
       cmd = "telnet %s"%mfc_ip
       handle.sendline(cmd)
       i = handle.expect (['login','Connection timed out','Unable to connect to remote host',pexpect.EOF,pexpect.TIMEOUT],timeout=300)
       output = handle.before
       print output
       
       if i == 0 :
          break
       else:
          time.sleep(10)
          continue

   cmd = "admin"
   handle.sendline(cmd)
   i = handle.expect ([pexpect.EOF,pexpect.TIMEOUT,'>','Password'], timeout=100)
   output = handle.before
   print output

   if i == 3 :
     cmd = "n1keenA"
     handle.sendline(cmd)
     i = handle.expect ([pexpect.EOF,pexpect.TIMEOUT,'>'], timeout=100)
     output = handle.before
     print output

   cmd = "en"
   output = gen_lib.send_cmd(test_obj,handle,cmd,'#',60) 
   cmd = "config term"
   output = gen_lib.send_cmd(test_obj,handle,cmd,'\(config\)',60) 

if __name__ == '__main__' :


  try:
     arg = {}
     test_obj = test_lib.lib(arg)
     testbed_config = test_obj.argument['testbed_config']['testbed_config']
     test_conf      = test_obj.argument['test_conf']['test_conf']

     if test_conf.has_key('smgr_client'):
       time.sleep(600) # to ensure live-migrateion vm settles up in SM environment

     profile_name = test_conf['profile_name']
     fab_node_host = testbed_config['%s,fab_node'%profile_name]
     fab_node = testbed_config['%s,node_name'%fab_node_host]

     fab_node_handle1   = test_obj.create_ssh_handle(node_name=fab_node,ntp_update=True,run_time=test_conf['runtime'])
     ostack.init_credentials(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node])

     fab_node_handle2   = test_obj.create_ssh_handle(node_name=fab_node,ntp_update=True,run_time=test_conf['runtime'])
     ostack.init_credentials(test_obj,fab_node_handle2,testbed_config['%s,prompt'%fab_node])

     fab_node_handle3   = test_obj.create_ssh_handle(node_name=fab_node,ntp_update=True,run_time=test_conf['runtime'])
     ostack.init_credentials(test_obj,fab_node_handle3,testbed_config['%s,prompt'%fab_node])


     #cmd = "ceph osd pool get volumes size"
     #output = gen_lib.send_cmd(test_obj,fab_node_handle1,cmd,testbed_config['%s,prompt'%fab_node],20)
     #
     #replica_count = re.search('^\s*size:\s*(\d+)\s*$',output,re.M)
     #if replica_count and int(replica_count.group(1)) == int(testbed_config['replica_count']) :
     #  msg = "INFO: replica count is set correctly\n"
     #  gen_lib.Print(msg)
     #else:
     #  err_msg = "ERROR: replica count is not set correctly.\n"
     #  gen_lib.Print(err_msg)
     #  test_obj.argument['err_msg'] += err_msg

     cmd = "mkdir /store"
     output = gen_lib.send_cmd(test_obj,fab_node_handle1,cmd,testbed_config['%s,prompt'%fab_node],10)

     src_ip     = testbed_config['regression,ip']
     src_login  = testbed_config['regression,login']
     src_passwd = testbed_config['regression,password']

     src_file   = test_conf['mfc_image']
     dest       = "/store/"

     d,mfc_image_file = os.path.split(src_file)

     args = {}
     args['handle']           = fab_node_handle1
     args['prompt']           = testbed_config['%s,prompt'%fab_node] 
     args['image_name']       = "mfc"
     args['disk_format']      = 'qcow2'
     args['is_public']        = True
     args['container_format'] = "ovf"
     args['image']            = dest + mfc_image_file
     args['vm_name']          = test_conf['mfc_vm_name']
     args['test_obj']         = test_obj

     status = test_obj.remote_scp_from(fab_node_handle1,testbed_config['%s,prompt'%fab_node],src_file,src_ip,src_login,src_passwd,dest)
     if not status :
        test_obj.argument['err_msg'] += "test_obj.remote_scp for %s failed"%src_file
        sys.exit()

     ostack.delete_glance_image(args)
     args['image_name'] = "ubuntu"
     ostack.delete_glance_image(args)
     args['image_name'] = test_conf['mfc_snapshot_name']
     ostack.delete_glance_image(args)

     ostack.delete_all_vms(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node])

     args['image_name'] = "mfc"
     ostack.add_glance_image(args) 

     ostack.add_security_rules(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node])

     args['volume_name'] = "disk1"
     #ostack.delete_cinder_volume(args)
     args['volume_name'] = "disk2"
     #ostack.delete_cinder_volume(args)

     args['volume_name'] = "disk1"
     args['volume_type'] = "ocs-block-disk"
     args['volume_size'] = "10"
     #volume_id1 = ostack.create_cinder_volume(args)

     args['volume_name'] = "disk2"
     args['volume_type'] = "ocs-block-disk"
     args['volume_size'] = "10"
     #volume_id2 = ostack.create_cinder_volume(args)

     ostack.delete_neutron_net(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node],test_conf['vn_name'])
     net_id = ostack.create_neutron_net(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node],test_conf['vn_name'])
     ostack.create_neutron_subnet(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node],test_conf['subnet_name'],test_conf['vn_name'],test_conf['vm_network'])
     args['flavor']     = "m1.medium"
     args['net_id']     = net_id
     args['security-groups'] = "default"

     time.sleep(30) # to ensure network configuration settles
     ostack.boot_nova_image(args)

     instance_id = ostack.get_vm_id(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node],args['vm_name'])
     
     args['status'] = "ACTIVE"
     args['power_state'] = "Running"
     args['timeout']     = 600
     ret = ostack.wait_until_vm_status(args)
     if not ret :
        msg = "ERROR: %s VM did not come up correctly.timeout:%d\n"%(args['vm_name'], args['timeout'])
        print msg
        test_obj.argument['err_msg'] += msg

     #ostack.attach_cinder_volume(fab_node_handle,testbed_config['%s,prompt'%fab_node],instance_id,volume_id1)
     #ostack.attach_cinder_volume(fab_node_handle,testbed_config['%s,prompt'%fab_node],instance_id,volume_id2)

     current_hostname1 = ostack.get_vm_hostinfo(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node],args['vm_name'])

     node_name1 = testbed_config['%s,node_name'%current_hostname1]
     compute_login1 = testbed_config['%s,login'%node_name1]
     compute_prompt1 = testbed_config['%s,prompt'%node_name1]
     compute_password1 = testbed_config['%s,password'%node_name1]
      
     ssh_to_ip(fab_node_handle2,current_hostname1,compute_login1,compute_password1,compute_prompt1)


     mfc_public_ip = identify_vm_ip(test_obj,fab_node_handle2,compute_prompt1)[0]
     #exit_compute(fab_node_handle2,':~#')

     
     if testbed_config.has_key('%s,other_name'%current_hostname1):
         host = testbed_config['%s,other_name'%current_hostname1]
     else:
         host = current_hostname1

     deploy_linux_vm(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node],host,net_id)
     current_hostname2 = ostack.get_vm_hostinfo(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node],test_conf["client_vm_name"])
     node_name2 = testbed_config['%s,node_name'%current_hostname2]
     compute_login2 = testbed_config['%s,login'%node_name2]
     compute_prompt2 = testbed_config['%s,prompt'%node_name2]
     compute_password2 = testbed_config['%s,password'%node_name2]
     ssh_to_ip(fab_node_handle3,current_hostname2,compute_login2,compute_password2,compute_prompt2)

     if current_hostname1 == current_hostname2 :
       index = 1
     else:
       index = 0

     client_public_ip = identify_vm_ip(test_obj,fab_node_handle3,compute_prompt2)[index]

     cmd = "nova list"
     output = gen_lib.send_cmd(test_obj,fab_node_handle1,cmd,testbed_config['%s,prompt'%fab_node],60)

     ret = re.search('%s.*%s=([\d\.]+)'%(test_conf['mfc_vm_name'],test_conf["vn_name"]),output)
     if ret :
       mfc_private_ip = ret.group(1)

     ret = re.search('%s.*%s=([\d\.]+)'%(test_conf['client_vm_name'],test_conf["vn_name"]),output)
     if ret :
       client_private_ip = ret.group(1)

     print "MFC public IP: ",mfc_public_ip
     print "MFC private IP: ",mfc_private_ip
     print "CLIENT public IP:",client_public_ip
     print "CLIENT private IP:",client_private_ip

     telnet_to_mfc(fab_node_handle2,mfc_public_ip)
     configure_namespace(test_obj,fab_node_handle2,client_private_ip)


     src_ip     = testbed_config['regression,ip']
     src_login  = testbed_config['regression,login']
     src_passwd = testbed_config['regression,password']

     src_file = test_conf['http_server_file']
     dest     = "/tmp/"

     status = test_obj.remote_scp_from(fab_node_handle3,compute_prompt2,src_file,src_ip,src_login,src_passwd,dest)
     if not status :
        test_obj.argument['err_msg'] += "test_obj.remote_scp for %s failed"%src_file
        sys.exit()

     dest_ip = client_public_ip
     dest_login = "ubuntu"
     dest_passwd = "ubuntu"
   
     d,f = os.path.split(test_conf['http_server_file'])
     src_file = "/tmp/" + f 

     status = test_obj.remote_scp_to(fab_node_handle3,compute_prompt2,src_file,dest_ip,dest_login,dest_passwd,dest)
     if not status :
        test_obj.argument['err_msg'] += "test_obj.remote_scp for %s failed"%src_file
        sys.exit()

     ssh_to_ip(fab_node_handle3,client_public_ip,"ubuntu","ubuntu","~$")

     gen_lib.send_cmd(test_obj,fab_node_handle3,"sudo bash","~#",60)
      
     simple_http_server = src_file
     thread.start_new_thread(run_http_server,(test_obj,fab_node_handle3,simple_http_server,mfc_private_ip))

     exit_mfc(test_obj,fab_node_handle2,compute_prompt1)

     #reboot_mfc(fab_node_handle,prompt)

     #time.sleep(180)

     #telnet_to_mfc(fab_node_handle,mfc_ip)
     #check_disk_list(test_obj,fab_node_handle,'#')

     #exit_mfc(fab_node_handle,prompt)
     #exit_compute(fab_node_handle,':~#')

     time.sleep(40)

     snapshot_time = snapshot(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node],test_conf['mfc_vm_name'],test_conf['mfc_snapshot_name'])
     print "snapshot time : %d s"%snapshot_time

     if snapshot_time == -1 :
         msg = "ERROR: nova snapshot failed.\n"
         print msg
         test_obj.argument['err_msg'] += msg

     branch = ostack.get_build_branch(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node])

     if snapshot_time > test_conf['%s,snapshot_time'%branch] :
         msg = "ERROR: nova snapshot took long time.actual time : %d , expected time : %d"%(snapshot_time,test_conf['%s,snapshot_time'%branch])
         print msg
         test_obj.argument['err_msg'] += msg
         
     ## boot MFC from snapshot glance image
     #args['image_name'] = test_conf['mfc_snapshot_name']
     #args['vm_name']    = test_conf['mfc_vm_name_snapshot']
     #args['zone']       = host
     #ostack.boot_nova_image(args)
     #ostack.wait_until_vm_status(args)

     #mfc1_public_ip = identify_vm_ip(fab_node_handle2,compute_prompt)[2]

     #telnet_to_mfc(fab_node_handle2,mfc1_public_ip)
     #ret = check_mfc_version(fab_node_handle2,test_conf['mfc_image'])
     #if ret:
     #  print "PASS : mfc version check passed , for the vm boot from snapshot"
     #else:
     #  msg = "FAIL : mfc version check failed , for the vm boot from snapshot"
     #  print msg
     #  test_obj.argument['err_msg'] += msg

     ostack.delete_all_vms(test_obj,fab_node_handle1,testbed_config['%s,prompt'%fab_node])

     #cmd = "ps -eaf | grep 'python %s' | awk '{print $2}' | xargs kill -9"%simple_http_server
     #gen_lib.send_cmd(test_obj,fab_node_handle2,cmd,'#',60)

     #cmd = "ps -eaf | grep curl | awk '{print $2}' | xargs kill -9"
     #gen_lib.send_cmd(test_obj,fab_node_handle2,cmd,'#',60)

     #exit_compute(test_obj,fab_node_handle2,'closed')
     #exit_compute(test_obj,fab_node_handle3,'closed')
     
     test_obj.cleanup()
     test_obj.PostResult()
     
  except Exception:

     traceback.print_exc()
     test_obj.argument['err_msg'] += 'ERROR: exception seen'
     test_obj.PostResult()
     test_obj.cleanup()

