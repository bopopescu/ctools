import gen_lib
import re

def remove_volume_group(test_obj,handle,prompt,vg_name):

  cmd = "pvscan"
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60,True,False) 
  pv_ret = re.findall('PV\s+(\S+)\s+VG\s+%s\s+'%vg_name,output)
  
  if len(pv_ret) == 0 :
    return
   
  cmd = "lvs"
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30,True,False) 
  lv_ret = re.findall('(\S+)\s+%s'%vg_name,output)

  if len(lv_ret):
   cmd = "service tgt stop"
   output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30,True,False) 
   cmd = "service iscsitarget stop"
   output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30,True,False) 

  for lv in lv_ret :
    cmd = "lvremove /dev/%s/%s -ff"%(vg_name,lv)
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30,True,False) 
   
  cmd = "vgremove %s"%vg_name
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30,True,False) 

  for pv in pv_ret:
    cmd = "pvremove %s"%pv
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30,True,False) 
  
