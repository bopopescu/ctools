import time
import os
import sys
import re
import traceback
import commands
from threading import Thread

import gen_lib
import os_lib

def InstallContrail(test_obj,handle,prompt): 

       testbed_config = test_obj.argument['testbed_config']['testbed_config']
       test_conf  = test_obj.argument['test_conf']['test_conf']

       src_ip     = testbed_config['regression,ip']
       src_login  = testbed_config['regression,login']
       src_passwd = testbed_config['regression,password']
       src_file_list  = test_conf['install_packages']
       dest           = "/tmp"

       for src_file in src_file_list :
         status = test_obj.remote_scp_from(handle,prompt,src_file,src_ip,src_login,src_passwd,dest)
         if not status :
           test_obj.argument['err_msg'] += "test_obj.remote_scp for %s failed"%src_file
           sys.exit()

       src_ip     = testbed_config['regression,ip']
       src_login  = testbed_config['regression,login']
       src_passwd = testbed_config['regression,password']
       src_file   = testbed_config['route_file,loc']
       dest = "/tmp/"
 
       status = test_obj.remote_scp_from(handle,prompt,src_file,src_ip,src_login,src_passwd,dest)
       if not status :
          test_obj.argument['err_msg'] += "test_obj.remote_scp for %s failed"%src_file
          sys.exit()
   
       d,f = os.path.split(src_file)
       cmd = "python /tmp/%s"%f 

       for src_file in src_file_list :
          d,f = os.path.split(src_file)
          cmd = "dpkg --info /tmp/%s"%f
          output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)
          pkg_name = re.search('Package: (\S*)',output).group(1)
         
          cmd = "dpkg -i /tmp/%s"%f
          output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

          cmd = "dpkg --list %s"%pkg_name
          output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
  
          if re.search('ii',output) :
              gen_lib.Print("INFO: Package %s installed successfully"%pkg_name)
          else:
              gen_lib.Print("ERROR: Package %s installation failed"%pkg_name)
              test_obj.argument['err_msg'] += "EROOR: dpkg %s installation failed.\n"%pkg_name
              sys.exit()

       cmd = "cd /opt/contrail/contrail_packages"
       output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

       cmd = "grep 'pip install' setup.sh"
       output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)
       
       pkg_list = re.findall('pip install (.*?tar.gz)',output,re.M)

       fab_version_to_be = re.search('Fabric-([0-9a-zA-Z.]+).tar.gz',output).group(1)

       cmd = "./setup.sh"
       output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,300)
       if re.search('Abort',output):
          test_obj.argument['err_msg'] += "ERROR: ./setup.sh aborted.\n"
          sys.exit()

       cmd = "fab --version"
       output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

       fab_version = re.search('Fabric\s*(\S+)',output).group(1)

       if fab_version != fab_version_to_be :
          gen_lib.Print("ERROR: Fabric version is incorrect")
          test_obj.argument['err_msg'] += "ERROR: fabric version is incorrect.\n"
          sys.exit()

def ExecuteSetupStorage(test_obj,handle,prompt):

       cmd = "cd /opt/contrail/contrail_packages"
       output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

       cmd = "./setup_storage.sh"
       output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,300)
       if re.search('Abort',output):
         gen_lib.Print("ERROR: %s Aborted"%cmd)
         test_obj.argument['err_msg'] += "ERROR: ./setup_storage.sh failed.\n"
         sys.exit()

def ntp_update_all_nodes(test_obj,handle,prompt):
    
     cmd = "cd /opt/contrail/utils"
     output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
     cmd = "fab -R all  -w -- ' ntpdate 172.17.31.136'"
     output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,180)

def check_ceph_status(test_obj,handle,prompt,fab_node_ip=None):

     try:
          testbed_config = test_obj.argument['testbed_config']['testbed_config']
          test_conf      = test_obj.argument['test_conf']['test_conf']
          profile_name = test_conf['profile_name']

          exp_osd_map_count = test_obj.argument['exp_osd_map_count']
          exp_monitor_ip_list = test_obj.argument['expected_monitor_ip_list']

          cmd = "ceph -v"
          ceph_v_output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)


          status_dict = {}

          if fab_node_ip == None :
             cmd = "ceph -s"
             ceph_output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
             if testbed_config.has_key('%s,local_only_disks'%profile_name) and testbed_config['%s,local_only_disks'%profile_name] :
                if re.search('Error initializing cluster client: Error',ceph_output) :
                   print "INFO: ceph -s throws error correctly for only local-disks"
                else: 
                   err_msg = "ERROR: ceph -s does not throw error for only local-disks"
                   print err_msg
                   test_obj.argument['err_msg'] += err_msg
                return
          else:
             cmd = "curl http://%s:5005/api/v0.1/status"%fab_node_ip
             ceph_output = commands.getoutput(cmd)
             if testbed_config.has_key('%s,local_only_disks'%profile_name) and testbed_config['%s,local_only_disks'%profile_name] :
               print "INFO : only local-disks.ignore ceph status"
               return

          print '####',ceph_output,'####'

          if exp_osd_map_count == -1 :
             if re.search('(Error initializing cluster client: Error)|(couldn\'t connect to host)',ceph_output) :
                print "INFO : ceph -s output failed as expected.ceph disks are not configured , as expected"
                return
             else:
                msg = "ERORR : ceph disks are configured incorrectly.\n"
                print msg
                test_obj.argument['err_msg'] += msg   
                return

          ret = re.search('HEALTH_WARN|HEALTH_OK|HEALTH_ERR',ceph_output)
          status_dict['health'] = ret.group()
         
          if re.search('mons down',ceph_output) :
             err_msg = "ERROR: ceph monitor is down in some nodes\n"
             gen_lib.Print(err_msg)
             test_obj.argument['err_msg'] += err_msg

          out = re.search('monmap.*',ceph_output).group()
          ret = re.findall('=(.*?):',out) 
          status_dict['monitor_ip_list'] = ret

          status_dict['monitor_ip_list'].sort()
          exp_monitor_ip_list.sort()

          print "ceph monitor ip list:",status_dict['monitor_ip_list']
          print "expected monitor ip list :",exp_monitor_ip_list

          if status_dict['monitor_ip_list'] == exp_monitor_ip_list :
             msg = "INFO: ceph monitor IP is correct\n"
             gen_lib.Print(msg)
          else:
             err_msg = "ERROR: ceph monitor IP is not correct\n"
             gen_lib.Print(err_msg)
             test_obj.argument['err_msg'] += err_msg

          #pool_cnt = re.search(' (\d+) pools',ceph_output).group(1)
          #status_dict['pool_cnt'] = pool_cnt

          #if int(pool_cnt) == 2 : # volumes,image
          #  msg = "INFO: ceph pool_count is correct\n"
          #  gen_lib.Print(msg)
          #else:
          #  err_msg = "ERROR: ceph pool count is NOT correct\n"
          #  gen_lib.Print(err_msg)
          #  test_obj.argument['err_msg'] += err_msg

          if ret  and status_dict['health'] == 'HEALTH_OK' :
            gen_lib.Print("INFO: ceph status OK")
          elif ret and status_dict['health'] == 'HEALTH_WARN':
            gen_lib.Print("WARNING: ceph status is HEALTH_WARN")
          else :
            err_msg = "ERROR: ceph status is NOT OK, HEALTH_OK|HEALTH_WARN NOT SEEN"
            gen_lib.Print(err_msg)
            test_obj.argument['err_msg'] += err_msg


          ret = re.search('osdmap .*: (\d+) osds: (\d+) up, (\d+) in',ceph_output) 
          if ret and ( int(ret.group(1)) == exp_osd_map_count ) and ( int(ret.group(2)) == exp_osd_map_count ) and ( int(ret.group(1)) == exp_osd_map_count ) :
             msg = "INFO: ceph status is PASS and osd count is PASS and all osds are up\n"
             gen_lib.Print(msg)
          else :
             err_msg = "ERROR: ceph status is NOT OK, osdmap count does not match"
             gen_lib.Print(err_msg)
             test_obj.argument['err_msg'] += err_msg

          if test_obj.argument.has_key('expected_storage_memory'):
              if re.search(test_obj.argument['expected_storage_memory'],ceph_output):
                msg = "INFO: storage memory in ceph -s output is correct\n"
                gen_lib.Print(msg)
              else :
                err_msg = "ERROR : storage memory in ceph -s output is NOT correct\n"
                gen_lib.Print(err_msg)
                test_obj.argument['err_msg'] += err_msg
          return status_dict
     except:
          err_msg = "ERROR: exception seen in ceph -s.\n"
          gen_lib.Print(err_msg)
          traceback.print_exc()  
          test_obj.argument['err_msg'] += err_msg


def install_storage_pkg_all(test_obj,handle,prompt,storage_pkg):

       cmd = "cd /opt/contrail/utils"
       output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

       for i in xrange(5):
         cmd = "fab install_storage_pkg_all:/%s"%storage_pkg
         output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,600)
         if not re.search('Parallel execution exception',output):
           break

def install_pkg_all(test_obj,handle,prompt,contrail_pkg):

       cmd = "cd /opt/contrail/utils"
       output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

       for i in xrange(5):
         time.sleep(30)
         cmd = "fab install_pkg_all:/%s"%contrail_pkg
         output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,600)
         if not re.search('Parallel execution exception',output):
           break

def upgrade_kernel(test_obj,handle,prompt,setup_data_interface,host_list=None):

       test_conf      = test_obj.argument['test_conf']['test_conf']
       testbed_config = test_obj.argument['testbed_config']['testbed_config']
       profile_name = test_conf['profile_name']

       fab_node_host = testbed_config['%s,fab_node'%profile_name]
       fab_node = testbed_config['%s,node_name'%fab_node_host]

       #if test_conf['ubuntu_version'] == "14.04" :
       #    return False

       cmd = "cd /opt/contrail/utils"
       output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

       cmd = "fab upgrade_kernel_all"
       output = gen_lib.send_cmd(test_obj,handle,cmd,['to boot with new kernel version','kernel is already of expected version'],1800)

       time.sleep(600)

       contrail_branch = re.search('contrail-install-packages_(\d\.\d+)',test_conf['install_packages'][0]).group(1)
   
       if test_conf['ubuntu_version'] == "12.04" :
           exp_kernel_version = test_conf['12.04,kernel_upgrade,version']
       elif test_conf['ubuntu_version'] == "14.04" and contrail_branch <= "2.0" :
           exp_kernel_version = test_conf['14.04,kernel_upgrade,version,2.0']
       else:
           exp_kernel_version = test_conf['14.04,kernel_upgrade,version,2.10']

       if host_list == None :
          host_list = testbed_config['%s,hosts_list'%profile_name]    
       for host in host_list:
          node = testbed_config['%s,node_name'%host]
          cmd = "uname -a"
          test_obj.argument['%s_handle'%node] = test_obj.create_ssh_handle(node_name=node,ntp_update=True,run_time=test_conf['runtime'])
          output = gen_lib.send_cmd(test_obj,test_obj.argument['%s_handle'%node],cmd,testbed_config['%s,prompt'%node],10)
          if re.search(exp_kernel_version,output):
             msg = "INFO: %s kernel upgrade done\n"%node
             gen_lib.Print(msg)
          else:
             err_msg = "ERROR: %s kernel upgrade failed\n"%node
             gen_lib.Print(err_msg)
             test_obj.argument['err_msg'] += err_msg
       handle = test_obj.argument['%s_handle'%fab_node]
       if setup_data_interface:
         fab_setup_interface(test_obj,handle,prompt)

       return True

def get_compute_host_list(test_obj,handle,prompt):

     cmd = "nova-manage service list"
     output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
     return re.findall('nova-compute\s+(\S+)\s+',output)

def get_storage_host_list(test_obj,handle,prompt):

     testbed_config = test_obj.argument['testbed_config']['testbed_config']

     cmd = "ceph osd dump"
     output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

     ip_list = list(set(re.findall('osd.* (\d+\.\d+\.\d+\.\d+):',output)))
     print ip_list
     host_list = []
     for ip in ip_list:
       for k,v in testbed_config.items():
           if v == ip:
             print v,k
           if v == ip and ( re.match('node\d+,ip',k) or re.search('node\d+,data_link,ip',k)):
               node_name = k.split(",")[0]
               host_list.append(testbed_config['%s,host_name'%node_name])
               break
     return host_list


def fab_setup_interface(test_obj,handle,prompt):

    cmd = "cd /opt/contrail/utils"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

    cmd = "fab setup_interface"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,300)

def run_fab_commands1(test_obj,handle,prompt,setup_data_interface=False,host_list=None):

    test_conf      = test_obj.argument['test_conf']['test_conf']
    testbed_config = test_obj.argument['testbed_config']['testbed_config']
    profile_name = test_conf['profile_name']
    fab_node_host = testbed_config['%s,fab_node'%profile_name]
    fab_node = testbed_config['%s,node_name'%fab_node_host]

    node_rebooted = upgrade_kernel(test_obj,handle,prompt,setup_data_interface,host_list)  

    if node_rebooted :
       handle = test_obj.argument['%s_handle'%fab_node]

    cmd = "cd /opt/contrail/utils"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)
    
    cmd = "fab install_contrail"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,3600)

    if re.search('Abort',output):
      gen_lib.Print("ERROR: %s Aborted"%cmd)
      test_obj.argument['err_msg'] += "ERROR: fab install_contrail failed.\n"
      sys.exit()

    cmd = "cd /opt/contrail/utils"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

    cmd = "fab setup_all"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,1800)

    if re.search('Abort',output):
      gen_lib.Print("ERROR: %s Aborted"%cmd)
      test_obj.argument['err_msg'] += "ERROR: fab setup_all falied.\n"
      sys.exit()


def setup_storage(test_obj,handle,prompt):

    test_conf      = test_obj.argument['test_conf']['test_conf']
    testbed_config = test_obj.argument['testbed_config']['testbed_config']
   
    cmd = "cd /opt/contrail/utils"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

    cmd = "fab setup_storage"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,1200)

    if re.search('Abort',output):
      gen_lib.Print("ERROR: %s Aborted"%cmd)
      test_obj.argument['err_msg'] += "ERROR: fab setup_storage failed.\n"
      sys.exit()

def unconfigure_ceph(test_obj,handle,prompt):

    test_conf      = test_obj.argument['test_conf']['test_conf']
    testbed_config = test_obj.argument['testbed_config']['testbed_config']
   
    cmd = "cd /opt/contrail/utils"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

    cmd = "fab unconfigure_storage"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,1200)

    if re.search('Abort',output):
      gen_lib.Print("ERROR: %s Aborted"%cmd)
      test_obj.argument['err_msg'] += "ERROR: fab install_storage failed.\n"
      sys.exit()

    return

def run_fab_commands2(test_obj,handle,prompt):

    test_conf      = test_obj.argument['test_conf']['test_conf']
    testbed_config = test_obj.argument['testbed_config']['testbed_config']
   
    cmd = "cd /opt/contrail/utils"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

    cmd = "fab install_storage"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,1200)

    if re.search('Abort',output):
      gen_lib.Print("ERROR: %s Aborted"%cmd)
      test_obj.argument['err_msg'] += "ERROR: fab install_storage failed.\n"
      sys.exit()

    ntp_update_all_nodes(test_obj,handle,prompt)

    cmd = "fab setup_storage"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,1200)

    if re.search('Abort',output):
      gen_lib.Print("ERROR: %s Aborted"%cmd)
      test_obj.argument['err_msg'] += "ERROR: fab setup_storage failed.\n"
      sys.exit()

    #time.sleep(30)
    #check_ceph_status(test_obj,handle,prompt)

    return


def get_ceph_build_version(test_obj):

   test_conf      = test_obj.argument['test_conf']['test_conf']
   contrail_install_pkg = test_conf['contrail-install-packages']

   ret = re.search('contrail-install-packages_([0-9.]+)-',contrail_install_pkg)
   ver = ret.group(1)
   return ver

def update_testbed_file(test_obj,fab_node_handle,testbed_file,info):

   testbed_config  = test_obj.argument['testbed_config']['testbed_config']
   test_conf      = test_obj.argument['test_conf']['test_conf']
   src_ip     = testbed_config['regression,ip']
   src_login  = testbed_config['regression,login']
   src_passwd = testbed_config['regression,password']

   profile_name = test_conf['profile_name']
   fab_node_host = testbed_config['%s,fab_node'%profile_name]
   fab_node = testbed_config['%s,node_name'%fab_node_host]

   d,f = os.path.split(testbed_file)

   for host in testbed_config['%s,hosts_list'%profile_name] :
     node = testbed_config['%s,node_name'%host]
     test_obj.argument['%s_data_iface'%node] = os_lib.get_data_interface_name(test_obj,test_obj.argument['%s_handle'%node],testbed_config['%s,prompt'%node],node)

   cmd = "cp %s /tmp/"%testbed_file
   gen_lib.Print(cmd)
   output = commands.getoutput(cmd)
   gen_lib.Print(output)

   for host in testbed_config['%s,hosts_list'%profile_name] :
     node = testbed_config['%s,node_name'%host]
     iface = test_obj.argument['%s_data_iface'%node]
     cmd = "sed -i 's/%s_data_interface/%s/' /tmp/%s "%(node,iface,f)
     gen_lib.Print(cmd)
     output = commands.getoutput(cmd)
     gen_lib.Print(output)
   
   src_file = "/tmp/%s"%f
   dest       = '/opt/contrail/utils/fabfile/testbeds/testbed.py'
   test_obj.remote_scp_from(fab_node_handle,testbed_config['%s,prompt'%fab_node],src_file,src_ip,src_login,src_passwd,dest)


