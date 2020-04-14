import pexpect
import traceback
import re
import time
import sys

def stripCtrl(str):
  result = ""
  for i in range(len(str)):
     if (str[i] != '\x08'):
        result = result+str[i]
  return result

def Print(str,DEBUG=True):
   if DEBUG:
     print time.ctime()+"\n"+stripCtrl(str)
   sys.stdout.flush()

def send_cmd(test_obj,handle,cmd,prompt,wait_time,calc_time=False,log_error=True):
    
   if isinstance(prompt,list) :
     exp_list = []
     exp_list.extend(prompt)
     exp_list.append(pexpect.EOF)
     exp_list.append(pexpect.TIMEOUT)
   else:
     exp_list = [prompt,pexpect.EOF,pexpect.TIMEOUT]

   try:
      handle.PROMPT = ".*"
      handle.expect(exp_list, timeout=2)
      print handle.before
   except:
      traceback.print_exc()
      pass

   Print("CMD:%s"%cmd)

   if calc_time:
     handle.sendline("time " + cmd)
   else:
     handle.sendline(cmd)


   #handle.PROMPT=prompt[0]
   handle.PROMPT = ".*"

   i = handle.expect (exp_list, timeout=wait_time)
   if exp_list[i] == pexpect.TIMEOUT :
     msg = "ERROR: cmd : %s timed-out"%cmd
     if log_error:
        test_obj.argument['err_msg'] += msg
     Print(msg)
     output = handle.before
     output += msg
   else:
     output = handle.before + handle.match.group()
   Print(output)
   return output

def wget_file(test_obj,handle,prompt,url,dest_file,time):
   
   cmd = "wget %s -O %s"%(url,dest_file)
   output = send_cmd(test_obj,handle,cmd,prompt,time)
   if re.search('saved',output):
      return True
   else:
      return False

