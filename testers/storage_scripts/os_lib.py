import time
import os
import sys
import re
import commands
import time
import gen_lib

def init_sources_list(test_obj,handle,prompt,run_setup=False):

    cmd = "echo > /etc/apt/sources.list"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

    cmd = "apt-get update"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

    if not run_setup:
       return
    cmd = "cd /opt/contrail/contrail_packages/"
    output = gen_lib.send_cmd(test_obj,handle,cmd,'contrail_packages#',10)

    cmd = "./setup.sh"
    output = gen_lib.send_cmd(test_obj,handle,cmd,'contrail_packages#',300)
    if re.search('Abort',output):
       test_obj.argument['err_msg'] += "ERROR: ./setup.sh aborted.\n"
       sys.exit()

    cmd = "./setup_storage.sh"
    output = gen_lib.send_cmd(test_obj,handle,cmd,'contrail_packages#',300)
    if re.search('Abort',output):
       test_obj.argument['err_msg'] += "ERROR: ./setup.sh aborted.\n"
       sys.exit()

def fix_default_gw(test_obj,handle,prompt):

   testbed_config  = test_obj.argument['testbed_config']['testbed_config']
   src_ip     = testbed_config['testbed_file,ip']
   src_login  = testbed_config['testbed_file,login']
   src_passwd = testbed_config['testbed_file,password']
   src_file   = testbed_config['route_file,loc']
   dest       = '/tmp'

   test_obj.remote_scp(handle,prompt,src_ip,src_login,src_passwd,src_file,dest)

   d,f = os.path.split(src_file)
   cmd = "python /tmp/%s\n"%f
   handle.write(cmd)
   handle.read_until('.*',5)

   cmd = "/etc/init.d/networking restart\n"
   handle.write(cmd)
   handle.read_until('.*',20)

   return

def get_data_interface_name(test_obj,handle,prompt,node_name):

  testbed_config = test_obj.argument['testbed_config']['testbed_config'] 

  cmd = "/sbin/ifconfig -a | grep '%s'" %testbed_config['%s,data_link,mac'%node_name]
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)
  gen_lib.Print("####")
  gen_lib.Print(output)
  gen_lib.Print("####")
  ret = re.search('eth\d',output)
  iface = ret.group(0)

  #ip = testbed_config['%s,data_link,ip'%node_name]
  #netmask = testbed_config['%s,data_link,netmask'%node_name]
  #cmd = "/sbin/ifconfig %s %s netmask %s up"%(iface,ip,netmask)
  #output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)
  #gen_lib.Print(output)

  return iface

def fix_telnet_login(test_obj,handle,prompt):

    src_ip = "10.87.129.2"
    src_login = "root"
    src_passwd = "n1keenA"
    src_file = "/tmp/telnet_0.17-36build1_amd64.deb"
    dest      = src_file

    test_obj.remote_scp(handle,prompt,src_ip,src_login,src_passwd,src_file,dest)

    cmd = "dpkg -i /tmp/telnet_0.17-36build1_amd64.deb"
    handle.write(cmd)
    gen_lib.Print(handle.read_until(prompt,120))

    #src_list = [ 'deb http://cz.archive.ubuntu.com/ubuntu lucid main universe']

    #cmd = "\cp -f /etc/apt/sources.list /etc/apt/sources.list.bk\n"
    #handle.write(cmd)
    #gen_lib.Print(handle.read_until(prompt,5))

    #cmd = "echo > /etc/apt/sources.list\n"
    #handle.write(cmd)
    #gen_lib.Print(handle.read_until(prompt,5))

    #for src in src_list :
    #   cmd = "echo \"" + src + "\"" + " >> /etc/apt/sources.list\n"
    #   handle.write(cmd)
    #   gen_lib.Print(handle.read_until(prompt,5))

    #cmd = "apt-get update\n"
    #handle.write(cmd)
    #gen_lib.Print(handle.read_until(prompt,600))

    #cmd = "apt-get install xinetd telnetd\n"
    #handle.write(cmd)
    #gen_lib.Print(handle.read_until('Do you want to continue',30))
    #handle.write('Y\n')
    #gen_lib.Print(handle.read_until(prompt,100))

    cmd = """# Simple configuration file for xinetd
             #
             # Some defaults, and include /etc/xinetd.d/
             defaults
             {
             # Please note that you need a log_type line to be able to use log_on_success
             # and log_on_failure. The default is the following :
             # log_type = SYSLOG daemon info
             instances = 60
             log_type = SYSLOG authpriv
             log_on_success = HOST PID
             log_on_failure = HOST
             cps = 25 30
             }
             """
    handle.write("echo \"" + cmd + " \" > /etc/xinetd.conf\n")
    gen_lib.Print(handle.read_until(prompt,30))

    handle.write("echo \"telnet stream tcp nowait telnetd /usr/sbin/tcpd /usr/sbin/in.telnetd\" > /etc/inetd.conf \n")
    gen_lib.Print(handle.read_until(prompt,30))

    cmd = "pts/0\npts/1\npts/2\npts/3\npts/4\npts/5\npts/6\npts/7\npts/8\npts/9\n"
    handle.write("echo \"" + cmd + " \" >> /etc/securetty\n")
    gen_lib.Print(handle.read_until(prompt,30))

    cmd = "service xinetd restart\n"
    handle.write(cmd)
    gen_lib.Print(handle.read_until(prompt,30))

    cmd = "sed -i 's/pam_secure//' /etc/pam.d/login\n"
    handle.write(cmd)
    gen_lib.Print(handle.read_until(prompt,30))

def change_bootcmd_install_and_reboot(test_obj,handle,preseed_file,ks_file,node_name,mgmt_iface):

  testbed_config = test_obj.argument['testbed_config']['testbed_config']

  passwd  = testbed_config['%s,password'%node_name]      
  prompt  = testbed_config['%s,prompt'%node_name]      

  time.sleep(2)
  out = handle.read_very_eager()

  gen_lib.Print(out)

  handle.write(chr(9)) # tab
  time.sleep(2)
  out = handle.read_very_eager()
  gen_lib.Print(out)
  ret = re.search('/Standard.*?ip=dhcp',out)
  buf = ret.group(0)
  print buf
  cmd = " url=%s"%preseed_file
  for c in cmd:
    handle.write(c)
    time.sleep(2)

  cmd = " ks=%s interface=%s"%(ks_file,mgmt_iface)
  for c in cmd:
    handle.write(c)
    time.sleep(2)

  cmd = " netdev=irq%s,io=%s,name=%s"%(testbed_config['%s,mgmt_iface,irq'%node_name],testbed_config['%s,mgmt_iface,address'%node_name],testbed_config['%s,mgmt_iface'%node_name])
  cmd += " biosdevname=0"

  for c in cmd:
      handle.write(c)
      time.sleep(2)
  
  time.sleep(30)

  handle.write('\r\n\r\n')

  for i in xrange(60):
    time.sleep(60)
    out = handle.read_very_eager()
    gen_lib.Print(out)
    if re.search('login:',out) or re.search('Network autoconfiguration failed',out):
      break

  if re.search('Network autoconfiguration failed',out):
     gen_lib.Print("ERROR: Ubuntu installation failed due to Network autoconfiguration failed: %s"%node_name)
     return False,"ERROR: installation failed due to Network autoconfiguration failed"
    
  install_status = False
  if re.search('login:',out):
      install_status = True
      handle.write('root\n')
      for i in xrange(60):
        time.sleep(1)
        out = handle.read_very_eager()
        gen_lib.Print(out)
        if re.search('Password',out):
          break
      handle.write('%s\n'%passwd)
      time.sleep(10)
      out = handle.read_very_eager()
      gen_lib.Print(out)

  if install_status :
     gen_lib.Print("PASS: Ubuntu installation done successfully : %s"%node_name)
     return True,"INFO: Installation success"
  else:
     gen_lib.Print("ERROR: Ubuntu installation failed : %s"%node_name)
     return False,"ERROR: installation failed due to other reasons"

def clear_pxe_new_page(mfc_tn):

  gen_lib.Print("PXE menu moving to next page. So clear the data")
  mfc_tn.read_until(".*",2)
  mfc_tn.write("[B")
  gen_lib.Print("==========")
  gen_lib.Print(mfc_tn.read_until("nopattern",2))
  gen_lib.Print("==========")
  mfc_tn.read_until(".*",2)
  mfc_tn.write("[A")
  image_2_1_out = mfc_tn.read_until("nopattern",2)
  mfc_tn.write("[B")
  mfc_tn.read_until(".*",2)
  mfc_tn.write("[B")
  image_2_3_out = mfc_tn.read_until("nopattern",2)
  mfc_tn.write("[A")
  mfc_tn.read_until(".*",2)
  mfc_tn.write("[A")
  mfc_tn.read_until(".*",2)
  return image_2_1_out,image_2_3_out

def PowerCycle(handle,menu_key):

  if menu_key == '^' :
    handle.write("")
  else :
    #handle.write("")
    handle.write(chr(26))
  
  out = handle.read_until("close current connection to port",10)
  gen_lib.Print(out)
  #ret = re.search('(\S)\s*reboot device using power-switch',out)
  #reboot_keystroke = ret.group(1)
  reboot_keystroke = 'r'
  handle.write(reboot_keystroke)
  out = handle.read_until("Are you sure you want to REBOOT this port",5)
  gen_lib.Print(out)
  if(not re.search("Are you sure you want to REBOOT this port",out,re.M)): return "FAILED"
  handle.write("y")
  out = handle.read_until("Rebooting",10)
  gen_lib.Print(out)

def powercycle_to_pxe_menu(handle,pxe_main,pxe_option,menu_key):

  PowerCycle(handle,menu_key)
  out = handle.read_until("PXE Main Menu",500)
  print out

  time.sleep(5)
  handle.write("[B")
  iterator=500
  prev_image = "nothing"
  cur_image = "something"
  direction = "down"
  time.sleep(5)
  discard = handle.read_very_eager()
  gen_lib.Print(discard)
  current_out = "nothing"
  out = "nothing"
  while((iterator>0)and(len(current_out)>0)):
    if(direction == "down"):
      handle.write("[B")
    else:
      handle.write("[A")
    iterator=iterator-1
    time.sleep(10)
    current_out = handle.read_very_eager()
    gen_lib.Print(current_out)
    mainpage_refreshed1 = re.search("Press \[Tab\] to edit options",current_out,re.M)
    mainpage_refreshed2 = re.search("Automatic",current_out,re.M)
    page_refreshed=False
    if(mainpage_refreshed1 or mainpage_refreshed2):
      image_2_1_out,image_2_3_out=clear_pxe_new_page(handle)
      page_refreshed=True
    cur_img = False
    if page_refreshed :
     find = re.search("Menu: (.*)",image_2_1_out,re.M)
     find1 = re.search("Menu: (.*)",image_2_3_out,re.M)   
     if re.search(pxe_main + " ",image_2_1_out,re.M) and (not re.search(pxe_main + " ",image_2_3_out,re.M)) :
       cur_img = True
     elif re.search(pxe_main + " ",image_2_1_out,re.M) and re.search(pxe_main + " ",image_2_3_out,re.M) :
      handle.write("[B")
      time.sleep(2)
      out = handle.read_very_eager()
      gen_lib.Print(out)
      cur_img = True
     elif (not re.search(pxe_main + " ",image_2_1_out,re.M))  and re.search(pxe_main + " ",image_2_3_out,re.M) :
      handle.write("[B")
      time.sleep(2)
      out = handle.read_very_eager()
      gen_lib.Print(out)
      handle.write("[B")
      time.sleep(2)
      out = handle.read_very_eager()
      cur_img = True
    else:
      find = re.search("Menu: (.*)",current_out,re.M)
      print "Current option: ", find.group(1)
      #pdb.set_trace()
      cur_img = re.search(pxe_main + " ",find.group(1))
    if(cur_img): # this can be True or regex match
        print "Successfully obtained the Pxe-boot build group"
        handle.write("\r\n")
        time.sleep(5)
        out = handle.read_very_eager()
        gen_lib.Print(out)
        while((iterator>0)and(len(out)>0)):
          prev_selection="nothing"
          cur_selection="something"
          if(direction == "down"):
            handle.write("[B")
          else:
            handle.write("[A")
          time.sleep(2)
          out = handle.read_very_eager()
          gen_lib.Print(out)
          print "Current selection : --- ", out, " ---"
          page_refreshed1 = re.search("Press \[Tab\] to edit options",out,re.M)
          page_refreshed2 = re.search("Automatic",out,re.M)
          page_refreshed=False
          if(page_refreshed1 or page_refreshed2):
            image_2_1_out,image_2_3_out=clear_pxe_new_page(handle)
            page_refreshed=True
          if page_refreshed :
            pattern = re.search(pxe_option + " ",image_2_1_out,re.M)
            patttern_tmp = re.search(pxe_option + " ",image_2_3_out,re.M)   
            print "image-2-1:",image_2_1_out,"return:",pattern
            print "image-2-3:",image_2_3_out,"return:",patttern_tmp
            if pattern and patttern_tmp :
              handle.write("[B")
              time.sleep(2)
              out = handle.read_very_eager()
              gen_lib.Print(out)
          else:
              pattern = re.search(pxe_option + " ",out,re.M)
          if(pattern):
            print "=================="
            print "Obtained the intended image: ", pattern.group(0)
            print "=================="
            #handle.write("\r\n")
            break
          iterator=iterator-1
          if(prev_selection==cur_selection):
            if(direction== "down"):
              direction = "up"
            else:
              direction = "down"
          prev_selection=cur_selection
          cur_selection=out
        break
    else:
        print "The current selection does not match our image"
        if(prev_image==cur_image):
          if(direction== "down"):
            direction = "up"
          else:
            direction = "down"
        prev_image=cur_image
        cur_image=find.group(1)

  #If unable to find the specified image, then exit and send mail.
  if(len(current_out)==0 or len(out)==0):
    gen_lib.Print("Unable to find the image specified on PXE server.\nHence, exiting!")

  return handle

