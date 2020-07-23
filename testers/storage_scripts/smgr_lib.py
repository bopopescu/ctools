import pexpect
import sys
import time
from time import gmtime, strftime
import simplejson
import gen_lib
import re
import os
import ceph

def get_cluster_id(json_file):

    jsonFile = open(json_file, "r")
    data = simplejson.load(jsonFile)
    jsonFile.close()

    return data["cluster"][0]["id"]

def execute_smgr_cli(test_obj,handle,prompt,cmd,timeout):

    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,timeout)
    ret = re.search('error',output,re.I)
    if ret:
      msg = "ERROR : error seen for cmd : %s"%cmd
      print msg
      test_obj.argument['err_msg'] += msg
    return output

class Smgr_lib :

  def __init__(self,arg):
    
      self.arg = arg

  def upgrade_smgr(self):

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']
     
      test_obj = self.arg['test_obj']

      test_conf  = test_obj.argument['test_conf']['test_conf']
      smgr_host_type = test_conf['smgr_host_type']

      testbed_config = test_obj.argument['testbed_config']['testbed_config']
      smgr_ip = testbed_config['server_manager,%s,ip'%smgr_host_type]

      smgr_host_type = test_conf['smgr_host_type'] 

      src_ip      = testbed_config['regression,ip']
      src_login   = testbed_config['regression,login']
      src_passwd  = testbed_config['regression,password']

      src_file_list = []
      src_file_list.append(testbed_config['%s,smgr_upgrade_script'%smgr_host_type])
      src_file_list.append(test_conf['smgr_main_pkg'])
      src_file_list.append(test_conf['smgr_client_pkg'])

      cmd = "rm -rf /tmp/smgr_files/"
      output = execute_smgr_cli(test_obj,handle,prompt,cmd,300)

      cmd = "mkdir /tmp/smgr_files/"
      output = execute_smgr_cli(test_obj,handle,prompt,cmd,60)
     
      dest_path = "/tmp/smgr_files/"

      for src_file in src_file_list :

        status = test_obj.remote_scp_from(handle,prompt,src_file,src_ip,src_login,src_passwd,dest_path)

        if not status :
          msg = "ERROR : test_obj.remote_scp for %s failed"%src_file
          print msg
          test_obj.argument['err_msg'] += msg
          sys.exit()

      d,f = os.path.split(test_conf['smgr_main_pkg'])
      server_pkg = "/tmp/smgr_files/" + f
      d,f = os.path.split(test_conf['smgr_client_pkg'])
      client_pkg = "/tmp/smgr_files/" + f

      d,f = os.path.split(testbed_config['%s,smgr_upgrade_script'%smgr_host_type])
      upgrade_script = "/tmp/smgr_files/" + f
      cmd = "python %s %s %s %s"%(upgrade_script,smgr_ip,server_pkg,client_pkg)
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,1800)

      if not re.search('INFO: INSTALL SUCCESS',output):
         msg = "ERROR: contrail-server-manager/client upgrade failed.\n"
         print msg
         test_obj.argument['err_msg'] += msg

      cmd = "/etc/init.d/contrail-server-manager restart"
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,120)

      #cmd = "service cobblerd restart"
      #output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

      cmd = "service puppetmain restart"
      execute_smgr_cli(test_obj,handle,prompt,cmd,60)

      #cmd = "sed -i 's|partman-auto/disk string /dev/sd?|partman-auto/disk string /dev/sda|' /var/www/html/kickstarts/contrail-ubuntu.seed"
      #output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

  def upgrade_smgr_latest(self):

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']
     
      test_obj = self.arg['test_obj']

      test_conf  = test_obj.argument['test_conf']['test_conf']
      smgr_host_type = test_conf['smgr_host_type']

      testbed_config = test_obj.argument['testbed_config']['testbed_config']
      smgr_ip = testbed_config['server_manager,%s,ip'%smgr_host_type]

      smgr_host_type = test_conf['smgr_host_type'] 

      src_ip      = testbed_config['regression,ip']
      src_login   = testbed_config['regression,login']
      src_passwd  = testbed_config['regression,password']

      src_file_list = []
      src_file_list.append(testbed_config['%s,smgr_upgrade_script_latest'%smgr_host_type])
      src_file_list.append(test_conf['smgr_installer'])

      cmd = "rm -rf /tmp/smgr_files/"
      output = execute_smgr_cli(test_obj,handle,prompt,cmd,300)

      cmd = "mkdir /tmp/smgr_files/"
      output = execute_smgr_cli(test_obj,handle,prompt,cmd,60)
     
     
      dest_path = "/tmp/smgr_files/"

      for src_file in src_file_list :

        status = test_obj.remote_scp_from(handle,prompt,src_file,src_ip,src_login,src_passwd,dest_path)

        if not status :
          msg = "ERROR : test_obj.remote_scp for %s failed"%src_file
          print msg
          test_obj.argument['err_msg'] += msg
          sys.exit()

      d,f = os.path.split(test_conf['smgr_installer'])
      smgr_installer_file = "/tmp/smgr_files/" + f

      d,f = os.path.split(testbed_config['%s,smgr_upgrade_script_latest'%smgr_host_type])
      upgrade_script = "/tmp/smgr_files/" + f
      cmd = "python %s %s %s"%(upgrade_script,smgr_ip,smgr_installer_file)
      output = gen_lib.send_cmd(test_obj,handle,cmd,'INSTALLATION_COMPLETED',1800)

      if not re.search('INFO: INSTALL SUCCESS',output):
         msg = "ERROR: contrail-installer upgrade failed.\n"
         print msg
         test_obj.argument['err_msg'] += msg

      cmd = "/etc/init.d/contrail-server-manager restart"
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)


  def setup_dhcp(self):

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']

      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']
      testbed_config = test_obj.argument['testbed_config']['testbed_config']

      smgr_host_type = test_conf['smgr_host_type']

      src_ip      = testbed_config['regression,ip']
      src_login   = testbed_config['regression,login']
      src_passwd  = testbed_config['regression,password']

      src_file = testbed_config['server_manager,%s,dhcpd_file'%smgr_host_type]
      dest_path = "/etc/cobbler/dhcp.template"

      status = test_obj.remote_scp_from(handle,prompt,src_file,src_ip,src_login,src_passwd,dest_path)

      if not status :
         msg = "ERROR : test_obj.remote_scp for %s failed"%src_file
         print msg
         test_obj.argument['err_msg'] += msg
         sys.exit()

      cmd = "service cobblerd restart"
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,120)


      cmd = "setsebool -P httpd_can_network_connect true"
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

      time.sleep(10)

      cobbler_sync_done = False

      for i in xrange(5):

        cmd = "cobbler sync"
        output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,120)
        if re.search('TASK COMPLETE',output):
            print "INFO: cobbler sync done"
            cobbler_sync_done = True
        else:
            time.sleep(60)
      if not cobbler_sync_done :
            msg = "ERROR : cobbler sync failed.stopping dhcpd"
            print msg
            test_obj.argument['err_msg'] += msg
            #cmd = "service dhcpd stop"
            #output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
            #sys.exit()

      #json_data = open(testbed_config['server_json_file'])
      #data = simplejson.load(json_data)
      #json_data.close()
      #server_list = data['server']

      #for server in server_list:
      #    server_name = server['id']
      #    domain = server['domain']
      #    cmd = "puppet cert --revoke %s.%s"%(server_name,domain)
      #    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

      cmd = "ps -eaf | grep server_mgr_main | awk '{print $2'} | xargs kill -9"
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
      cmd = "/etc/init.d/contrail-server-manager restart"
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,120)
      time.sleep(30)

  def show(self,param):
 
      handle = self.arg['handle'] 
      prompt = self.arg['prompt']

      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']

      cmd = test_conf['smgr_client_cmd'] + " show %s"%param

      for i in xrange(5):
        output = execute_smgr_cli(test_obj,handle,prompt,cmd,60)
        ret = re.search('({.*})',output,re.DOTALL)
        if ret:
          break
        else:
           time.sleep(30)
      output = re.search('({.*})',output,re.DOTALL).group(1)

      data = simplejson.loads(output)

      return data
   
  def delete_images(self) :

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']

      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']

      data = self.show('image')

      if len(data) != 0 :
        image_list = data['image']

      for image in image_list :
        ver = re.search('contrail-install-packages_([\d.]+)-',test_conf['contrail-install-packages'])
        if ver and float(ver.group(1)) >= 1.2  :
          cmd = test_conf['smgr_client_cmd'] + " delete image --image_id %s"%image['id']
        else:
          cmd = test_conf['smgr_client_cmd'] + " delete image %s"%image['id']
        output = execute_smgr_cli(test_obj,handle,prompt,cmd,60)
        ret = re.search('Image Deleted',output)
        if not ret:
           msg = "ERROR: image delete failed: %s.\n"%image['id']
           print msg
           test_obj.argument['err_msg'] += msg

  def add_cluster(self):

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']
      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']
      testbed_config = test_obj.argument['testbed_config']['testbed_config']

      cmd = "mkdir /tmp/smgr_files/"
      output = execute_smgr_cli(test_obj,handle,prompt,cmd,60)

      src_ip      = testbed_config['regression,ip']
      src_login   = testbed_config['regression,login']
      src_passwd  = testbed_config['regression,password']

      src_file = testbed_config['cluster_json_file']
      dest_path = "/tmp/smgr_files/"
     
      status = test_obj.remote_scp_from(handle,prompt,src_file,src_ip,src_login,src_passwd,dest_path)
      if not status :
         print "ERROR"
         test_obj.argument['err_msg'] += "test_obj.remote_scp for %s failed"%src_file
         sys.exit()

      d,f = os.path.split(src_file)

      cmd = test_conf['smgr_client_cmd'] + " add cluster -f /tmp/smgr_files/%s"%f
      output = execute_smgr_cli(test_obj,handle,prompt,cmd,60)
      ret = re.search('Cluster Add/Modify Success',output)
      if not ret:
         msg = "ERROR: cluster Add failed.\n"
         print msg
         test_obj.argument['err_msg'] += msg

  def delete_cluster(self):

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']
      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']

      data = self.show('cluster')
      cluster_list = data['cluster']

      if len(cluster_list) != 0 :
        cluster = cluster_list[0]
        ver = re.search('contrail-install-packages_([\d.]+)-',test_conf['contrail-install-packages'])
        if ver and float(ver.group(1)) >= 1.2 :
           cmd = test_conf['smgr_client_cmd'] + " delete cluster --cluster_id %s"%cluster['id']
        else:
           cmd = test_conf['smgr_client_cmd'] + " delete cluster %s"%cluster['id']
        output = execute_smgr_cli(test_obj,handle,prompt,cmd,60)

  def delete_servers(self):

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']
      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']

      data = self.show('server')

      if len(data) != 0 :
         server_list = data['server']
       
      for server in server_list :
        ver = re.search('contrail-install-packages_((\d.)+)-',test_conf['contrail-install-packages'])
        cmd = test_conf['smgr_client_cmd'] + " delete server --server_id %s"%server['id']
        output = execute_smgr_cli(test_obj,handle,prompt,cmd,60)
        ret = re.search('Server deleted',output)
        if not ret:
           msg = "ERROR : Server delete failed : %s"%server['id']
           print msg
           test_obj.argument['err_msg'] += msg

  def add_servers(self):

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']
      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']
      testbed_config = test_obj.argument['testbed_config']['testbed_config']

      src_ip      = testbed_config['regression,ip']
      src_login   = testbed_config['regression,login']
      src_passwd  = testbed_config['regression,password']

      profile_name = test_conf['profile_name']
      
      ceph_build_version = ceph.get_ceph_build_version(test_obj)
      node_ubuntu_version =test_conf['ubuntu_version']

      if float(ceph_build_version) >= float("2.10") :
        src_file = testbed_config['%s,%s,server_json_file_post_2.10'%(profile_name,node_ubuntu_version)]
      else:
        src_file = testbed_config['%s,%s,server_json_file_pre_2.10'%(profile_name,node_ubuntu_version)]

      dest_path = "/tmp/smgr_files/"
     
      status = test_obj.remote_scp_from(handle,prompt,src_file,src_ip,src_login,src_passwd,dest_path)
      if not status :
         print "ERROR"
         test_obj.argument['err_msg'] += "test_obj.remote_scp for %s failed"%src_file
         sys.exit()

      d,f = os.path.split(src_file)

      cmd = test_conf['smgr_client_cmd'] + " add server -f /tmp/smgr_files/%s"%f
      output = execute_smgr_cli(test_obj,handle,prompt,cmd,60)
      ret = re.search('Server add/Modify Success',output,re.I)
      if not ret:
          msg = "ERROR: Server add failed.\n"
          print msg
          test_obj.argument['err_msg'] += msg

  def updateImageJsonFile(self,dest_file):

      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']
      testbed_config = test_obj.argument['testbed_config']['testbed_config']
     
      jsonFile = open(test_conf['image_json_file'], "r")
      data = simplejson.load(jsonFile)
      jsonFile.close()

      contrail_pkg = {}
      contrail_pkg['version'] = "5000"
      d,f = os.path.split(test_conf['contrail-install-packages'])
      contrail_pkg['path']    = "/tmp/smgr_files/" + f
      
      storage_pkg = {}
      storage_pkg['version'] = "6000"
      d,f = os.path.split(test_conf['contrail-storage-packages'])
      storage_pkg['path']    = "/tmp/smgr_files/" + f
      
      ubuntu_pkg = {}
      ubuntu_pkg['version'] = test_conf['ubuntu_version']
      ubuntu_version = test_conf['ubuntu_version']
      d,f = os.path.split(test_conf['%s,ubuntu-image'%ubuntu_version])
      ubuntu_pkg['path']    = "/tmp/smgr_files/" + f

      ubuntu_version = test_conf['ubuntu_version']
      ps_file = test_conf['%s,preseed'%ubuntu_version]
      ks_file = test_conf['%s,kickstart'%ubuntu_version]

      for image in data["image"] :
        
         if image["type"] == "contrail-ubuntu-package" :
           image["version"] = contrail_pkg["version"]
           image["path"]    = contrail_pkg["path"]
         elif image["type"] == "contrail-storage-ubuntu-package":
           image["version"] = storage_pkg["version"]
           image["path"]    = storage_pkg["path"]
         elif image["type"] == "ubuntu":
           image["version"] = ubuntu_pkg["version"]
           image["path"]    = ubuntu_pkg["path"]
           image['parameters']['kickseed'] = ps_file
           image['parameters']['kickstart'] = ks_file
  
      jsonFile = open(dest_file, "w+")
      jsonFile.write(simplejson.dumps(data,indent = 2, separators=(',', ': ')))
      jsonFile.close()

  def add_images(self):

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']
      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']
      testbed_config = test_obj.argument['testbed_config']['testbed_config']

      tmp_image_json_file = "/cloud/auto/tmp/smgr_image_%s.json"%strftime("%Y-%m-%d-%H:%M:%S", gmtime())
      print tmp_image_json_file

      file_list = []
      file_list.append(test_conf['contrail-install-packages'])
      file_list.append(test_conf['contrail-storage-packages'])
      ubuntu_version = test_conf['ubuntu_version']
      file_list.append(test_conf['%s,ubuntu-image'%ubuntu_version])
      file_list.append(tmp_image_json_file) 

      self.updateImageJsonFile(tmp_image_json_file)

      src_ip      = testbed_config['regression,ip']
      src_login   = testbed_config['regression,login']
      src_passwd  = testbed_config['regression,password']

      cmd = "mkdir /tmp/smgr_files/"
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

      for file in file_list:
        dest_path = "/tmp/smgr_files/"
        if re.search('http://',file):
            d,f = os.path.split(file)
            t = dest_path + f
            status = gen_lib.wget_file(test_obj,handle,prompt,file,t,300) 
        else:
            status = test_obj.remote_scp_from(handle,prompt,file,src_ip,src_login,src_passwd,dest_path)

        if status :
           msg = "FILE %s copied successfully"%file
           print msg
        else:
           msg = "test_obj.remote_scp/wget for %s failed"%file
           print msg
           test_obj.argument['err_msg'] += msg

      d,f = os.path.split(tmp_image_json_file)
      cmd = test_conf['smgr_client_cmd'] + " add image -f /tmp/smgr_files/%s"%f
      output = execute_smgr_cli(test_obj,handle,prompt,cmd,180)

  def wait_until_provision_complete(self,handle,prompt):

      test_obj = self.arg['test_obj']
      provision_complete = False
      for i in xrange(0,40):
         time.sleep(180)
         server_state = self.get_server_state(handle,prompt)
         if not server_state :
             msg = "ERROR: getting server status\n"
             print msg
             test_obj.argument['err_msg'] += msg
             return
         if len(set(server_state)) == 1 and server_state[0] == '"status": "provision_completed"' :
            provision_complete = True
            break
      if not provision_complete :
          msg = "ERROR: provision did not complete within specified time"
          print msg
          test_obj.argument['err_msg'] += msg
          return
 

  def wait_until_reimage_complete(self):

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']
      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']
      testbed_config = test_obj.argument['testbed_config']['testbed_config']

      profile_name = test_conf['profile_name']

      ceph_build_version = ceph.get_ceph_build_version(test_obj)
      node_ubuntu_version =test_conf['ubuntu_version']

      if float(ceph_build_version) >= float("2.10") :
        src_file = testbed_config['%s,%s,server_json_file_post_2.10'%(profile_name,node_ubuntu_version)]
      else:
        src_file = testbed_config['%s,%s,server_json_file_pre_2.10'%(profile_name,node_ubuntu_version)]

      node_ubuntu_version =test_conf['ubuntu_version']
      json_data = open(src_file)
      data = simplejson.load(json_data)
      json_data.close()
      server_list = data['server']

      server_list_t = []
      for server in server_list:
          server_list_t.append(server['id'])

      s_list = map(lambda x:x.strip(),server_list_t)
      servers = ",".join(s_list)

      src_file   = "/var/nkn/qa/smoke/utils/check_reimage_complete.py"
      src_ip     = testbed_config['regression,ip']
      src_login  = testbed_config['regression,login']
      src_passwd = testbed_config['regression,password']
      dest_path  = "/tmp/smgr_files/"
      status = test_obj.remote_scp_from(handle,prompt,src_file,src_ip,src_login,src_passwd,dest_path)

      if not status :
          msg = "ERROR : test_obj.remote_scp for %s failed"%src_file
          print msg 
          test_obj.argument['err_msg'] += msg
          sys.exit()

      cmd = "python /tmp/smgr_files/check_reimage_complete.py %s"%servers
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,1800)

  def re_image_all(self) :
    
      handle = self.arg['handle'] 
      prompt = self.arg['prompt']
      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']
      testbed_config = test_obj.argument['testbed_config']['testbed_config']

      cluster_id = get_cluster_id(testbed_config['cluster_json_file'])

      cmd = test_conf['smgr_client_cmd'] + " reimage --cluster_id %s ubuntu-server1"%cluster_id
      print "CMD: ",cmd
      handle.sendline(cmd)
      i = handle.expect (['y/N',pexpect.EOF,pexpect.TIMEOUT], timeout=120)    
      cmd = 'y'
      output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
      if re.search('No Image',output):
        err_msg = "ERROR: image-not found error seen\n"
        gen_lib.Print(err_msg)
        test_obj.argument['err_msg'] += err_msg
        sys.exit()
      ret = re.search('server\(s\) reimage queued|issued',output)
      if not ret:
         err_msg = "ERROR: server re-image command failed.\n"
         print err_msg
         test_obj.argument['err_msg'] += err_msg
         sys.exit()

      self.wait_until_reimage_complete()
      time.sleep(180) # to allow servers to reboot.

  def get_server_state(self,handle,prompt) :

      test_obj = self.arg['test_obj']

      for i in xrange(5):
        cmd = "server-manager status server"
        output = execute_smgr_cli(test_obj,handle,prompt,cmd,60)
        ret = re.findall('"status".*"',output)
        if ret:
          return ret
        else:
          time.sleep(60)

  def start_puppet_agent(self,handle,prompt):

      test_obj = self.arg['test_obj']

      cmd = "puppet agent -t"
      no_print = True
      #output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,1800,no_print)

  def provision_servers(self):

      smgr_handle = self.arg['handle'] 
      smgr_prompt = self.arg['prompt']
      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']
      testbed_config = test_obj.argument['testbed_config']['testbed_config']


      cluster_id = get_cluster_id(testbed_config['cluster_json_file'])
      cmd = test_conf['smgr_client_cmd'] + " provision --cluster_id %s contrail_test_pkg"%cluster_id
      print "CMD: ",cmd
      smgr_handle.sendline(cmd)
      i = smgr_handle.expect (['y/N',pexpect.EOF,pexpect.TIMEOUT], timeout=120)
      cmd = 'y'
      output = gen_lib.send_cmd(test_obj,smgr_handle,cmd,smgr_prompt,120)
      if not re.search('provision issued',output):
        err_msg = "ERROR: servers not provisioned..\n"
        gen_lib.Print(err_msg)
        test_obj.argument['err_msg'] += err_msg 
        sys.exit()

      self.wait_until_provision_complete(smgr_handle,smgr_prompt)

      time.sleep(180)

      return

  def setup_livem(self) :

      handle = self.arg['handle'] 
      prompt = self.arg['prompt']

      test_obj = self.arg['test_obj']
      test_conf  = test_obj.argument['test_conf']['test_conf']
      testbed_config = test_obj.argument['testbed_config']['testbed_config']

      src_ip     = testbed_config['regression,ip']
      src_login  = testbed_config['regression,login']
      src_passwd = testbed_config['regression,password']

      src_file   = test_conf['ceph_nfs_image_src']
      dest       = "/var/www/html/contrail/images"

      status = test_obj.remote_scp_from(handle,prompt,src_file,src_ip,src_login,src_passwd,dest)
      if not status :
        test_obj.argument['err_msg'] += "test_obj.remote_scp for %s failed"%src_file
        sys.exit()



