import pdb
import commands
import re
import pxssh
import pexpect
import sys
import telnetlib
import inspect
import logging
import traceback
import time

import os_lib
import gen_lib

class lib:

   def __init__(self,arg):

       self.argument = arg
       self.argument['testbed_config'] = {}
       self.argument['test_conf'] = {}

       execfile(sys.argv[1],self.argument['test_conf'])
       execfile(sys.argv[-1],self.argument['testbed_config'])

       self.argument['err_msg'] = ""
       self.argument['warn_msg'] = ""
       self.argument['telnet_handles'] = []
       self.argument['ssh_handles'] = []


   def PostResult(self):

       if self.argument['err_msg'] == "" :
         test_result = "PASS"
       else:
         test_result = "FAIL"

       gen_lib.Print("TEST RESULT: %s %s\n"%(sys.argv[0],test_result))

   def cleanup(self):

     for h in self.argument['telnet_handles'] :
      try:
        h.close()
      except:
        traceback.print_exc()
        gen_lib.Print("DEBUG: error closing telnet handle")

     for h in self.argument['ssh_handles'] :
      try:
        h.logout()
      except:
        traceback.print_exc()
        gen_lib.Print("DEBUG: error closing ssh handle")

   def create_ssh_handle(self,**kwargs):

     node_name = kwargs['node_name']
     handle = None 

     testbed_config = self.argument['testbed_config']['testbed_config']

     ip = testbed_config['%s,ip'%node_name]

     #run_time = kwargs['run_time']

     try:
       login   = testbed_config['%s,login'%node_name]
       passwd  = testbed_config['%s,password'%node_name]      
       prompt  = testbed_config['%s,prompt'%node_name]      
 
       cmd = "sed -i '/%s/d' /root/.ssh/known_hosts"%(ip)
       commands.getoutput(cmd)

       print "###",ip,login,passwd,prompt,"####"

       handle = pxssh.pxssh()

       if not handle.login (ip,login,passwd,original_prompt=prompt, login_timeout=120,auto_prompt_reset=False):
           print "SSH session failed on login."
           print str(handle)
       else:
           print "SSH session login successful"
           #if run_time == "SM" :
           #  cmd = "service ntp stop"
           #  output = gen_lib.send_cmd(self,handle,cmd,prompt,120,True,False)
           #  cmd = "service ntp start"
           #  output = gen_lib.send_cmd(self,handle,cmd,prompt,120,True,False)
           #else: # for FAB env
           #  cmd = "service ntp stop"
           #  output = gen_lib.send_cmd(self,handle,cmd,prompt,120,True,False)
           #  ntp_ip = "172.17.31.136"
           #  cmd = "ntpdate %s"%ntp_ip
           #  output = gen_lib.send_cmd(self,handle,cmd,prompt,120,True,False)
           #  if re.search('timed-out',output):
           #    handle = None
     except :
        traceback.print_exc()
        print "SSH session failed on login."
        handle =None

     if handle != None:
         self.argument['ssh_handles'].append(handle)
     return handle
       

   def create_telnet_handle(self,**kwargs) :
      
     handle = None
     
     node_name = kwargs['node_name']
     if kwargs.has_key('console'):   
       console = True
     else: 
       console = False

     testbed_config = self.argument['testbed_config']['testbed_config']

     if console :
       ip = testbed_config['%s,console_ip'%node_name]
       if testbed_config.has_key('%s,console_port'%node_name):
          port = testbed_config['%s,console_port'%node_name]
       else:
          port = 23
     else:
       ip = testbed_config['%s,ip'%node_name]
       port = 23

     try:
        login   = testbed_config['%s,login'%node_name]
        passwd  = testbed_config['%s,password'%node_name]      
        prompt  = testbed_config['%s,prompt'%node_name]      
        menu_key = testbed_config['%s,console_menu_key'%node_name]
         
        handle = telnetlib.Telnet(ip,port)

        #handle.write("\n")
        #output = handle.read_until('.*',30)
        #gen_lib.Print(output)
        #if not re.search('login',output) and re.search('root',output):
        #   handle.write('exit \n')
        #   output = handle.read_until('login',30)
        #   gen_lib.Print(output)
        #elif re.search('login',output):
        #   pass
        #else:
        #   os_lib.PowerCycle(handle,menu_key)
        #   output = handle.read_until('login',600)
        #handle.write(login + "\n")
        #gen_lib.Print(handle.read_until('Password',30))
        #handle.write( passwd + "\n")
        #gen_lib.Print(handle.read_until(prompt,30))
     except :
        traceback.print_exc("ERROR: Telnet to %s failed"%ip )
        handle = None

     if handle != None:
      self.argument['telnet_handles'].append(handle)
     return handle

   def remote_scp(self,handle,prompt,src_file,cmd,passwd,scp_timeout):

     handle.expect ('.*',timeout=1)
     gen_lib.Print(handle.before)

     gen_lib.Print("CMD:"+cmd)
     handle.sendline(cmd)
     ret = handle.expect (["\?","password:",pexpect.EOF,pexpect.TIMEOUT], timeout=scp_timeout)
     output = handle.before
     gen_lib.Print(output)

     if ret == 0 :
        handle.sendline("yes")
        ret = handle.expect (["password:",pexpect.EOF,pexpect.TIMEOUT], timeout=scp_timeout)
        output = handle.before
        gen_lib.Print(output)
        if ret == 0:
          ret = 1
        else:
          ret = -1
     if ret == 1 :
         handle.sendline(passwd)
         handle.expect ([prompt,pexpect.EOF,pexpect.TIMEOUT], timeout=scp_timeout)
         output = handle.before
         gen_lib.Print(output)
     else:
         gen_lib.Print("Unknown prompt received: " + output)
     if (re.search("100%", output, re.M)):
         gen_lib.Print("INFO: File : %s copied Successfully"%src_file)
         return True
     else:
         gen_lib.Print("ERROR: File : %s copy failed"%src_file)
         return False

   def remote_scp_from(self,handle,prompt,src_file,src_ip,src_login,src_passwd,dest,scp_timeout=600):

     cmd = "scp " + src_login + '@' + src_ip + ':' +  src_file + " " + dest
     return self.remote_scp(handle,prompt,src_file,cmd,src_passwd,scp_timeout)

   def remote_scp_to(self,handle,prompt,src_file,dest_ip,dest_login,dest_passwd,dest_path,scp_timeout=600):

     cmd = "scp " + src_file + " " + dest_login + "@" + dest_ip + ":" + dest_path
     return self.remote_scp(handle,prompt,src_file,cmd,dest_passwd,scp_timeout)


