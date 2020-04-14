import re
import pdb
import time
import gen_lib
import test_lib

def init_credentials(test_obj,handle,prompt):

  cmd = "source  /etc/contrail/openstackrc"
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,10)

   
def add_security_rules(test_obj,handle,prompt):

  cmd = "nova secgroup-add-rule default icmp -1 -1 0.0.0.0/0"
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,20)
  cmd = "nova secgroup-add-rule default tcp 22 22 0.0.0.0/0"
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,20)

def delete_vm(test_obj,handle,prompt,vm_name):

  init_credentials(test_obj,handle,prompt)

  cmd = "nova list --name %s"%vm_name
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
  ret = re.findall("^\s*\|\s*(\S+)\s*\|",output,re.M)
  for i in xrange(1,len(ret)): 
    cmd = "nova delete %s"%ret[i]
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
    time.sleep(5)

def get_cinder_type_list(test_obj,handle,prompt):

  init_credentials(test_obj,handle,prompt)

  cmd = "cinder type-list"
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
  return re.findall('ocs\S+',output)

def delete_all_vms(test_obj,handle,prompt,all=False):

  init_credentials(test_obj,handle,prompt)

  cmd = "nova list"
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
  ret = re.findall("^\s*\|\s*(\S+)\s*\|\s*(\S+)",output,re.M)
  for i in xrange(1,len(ret)): 
    vm_id,vm_name = ret[i]
    if vm_name == "livemnfs" and not all:
      continue
    cmd = "nova delete %s"%vm_id
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
    time.sleep(5)
  
def delete_glance_image(kwargs):

  handle = kwargs['handle']
  prompt = kwargs['prompt']
  test_obj = kwargs['test_obj']

  cmd = "glance image-list --name=%s"%kwargs['image_name']
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,300)

  ret = re.findall('\|\s*(\S+)\s*\| %s'%kwargs['image_name'],output)

  for im in ret:
    cmd = "glance image-delete %s"%im
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,300)

def check_cinder_volume_state(kwargs):

  handle = kwargs['handle']
  prompt = kwargs['prompt']
  test_obj = kwargs['test_obj']
  vol_name = kwargs['volume_name']
  vol_state = kwargs['volume_state']

  cmd = "cinder list --display-name %s"%kwargs['volume_name']
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30)

  ret = re.search('(\S+)\s+\|\s+%s\s+'%kwargs['volume_name'],output)
  
  if ret and ret.group(1) == vol_state :
      return True
  else:
      return False

def create_cinder_volume(kwargs):

  handle = kwargs['handle']
  prompt = kwargs['prompt']
  test_obj = kwargs['test_obj']
  vol_name = kwargs['volume_name']
  vol_type = kwargs['volume_type']
  vol_size = kwargs['volume_size']

  cmd = "cinder create --display-name %s --volume-type %s %d"%(vol_name,vol_type,int(vol_size))
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30)
  ret = re.findall("\s+id\s*\|\s*(\S+)",output)
  return ret[0]

def attach_cinder_volume(test_obj,handle,prompt,instance_id,volume_id):

  cmd = "nova volume-attach %s %s auto"%(instance_id,volume_id)
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30)
  return output

def delete_cinder_volume(kwargs):

  handle = kwargs['handle']
  prompt = kwargs['prompt']
  test_obj = kwargs['test_obj']
  vol_name = kwargs['volume_name']

  cmd = "cinder list --display-name=%s"%vol_name
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30)
  ret = re.findall("^\|\s*(\S+)\s*\|",output,re.M)
  for v in ret:
     cmd = "cinder delete %s"%v
     output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30)


def add_glance_image(kwargs):

  handle = kwargs['handle']
  prompt = kwargs['prompt']
  test_obj = kwargs['test_obj']

  cmd = "glance image-create"

  cmd += " --name \"%s\""%kwargs['image_name']
  cmd += " --is-public true"
  cmd += " --container-format %s"%kwargs['container_format']
  cmd += " --disk-format %s"%kwargs['disk_format']
  cmd += " < %s"%kwargs['image']

  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,900)
  image_id = re.search('Added new image with ID:\s*(\S+)',output)
  if not image_id :
     return -1
  else:
     return image_id.group(1)

def get_network_id(test_obj,handle,prompt,network_name):

  cmd = "neutron net-list --name=%s"%network_name
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

  ret = re.search('\|\s*(\S+)\s*\| %s'%network_name,output)
  if ret:
    return ret.group(1)
  else:
    return -1

def delete_neutron_net(test_obj,handle,prompt,network_name):

  cmd = "neutron net-list --name=%s"%network_name
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
  
  ret = re.findall('\|\s*(\S+)\s*\| %s'%network_name,output)
  
  for n in ret:
    cmd = "neutron net-delete %s"%n
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

def create_neutron_net(test_obj,handle,prompt,network_name):

  cmd = "neutron net-create %s"%network_name
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
  
  cmd = "neutron net-list --name=%s"%network_name
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
  
  ret = re.search('\|\s*(\S+)\s*\| %s'%network_name,output)
  if ret:
    return ret.group(1)
  else:
    return -1

def create_neutron_subnet(test_obj,handle,prompt,net_name,subnet_name,ip_range):

  cmd = "neutron subnet-create --name=%s %s %s"%(net_name,subnet_name,ip_range)
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

def boot_nova_image(kwargs):

   handle = kwargs['handle']
   prompt = kwargs['prompt']
   test_obj = kwargs['test_obj']

   cmd = "nova boot"
   cmd += " --image %s" %kwargs['image_name']
   cmd += " --flavor %s" %kwargs['flavor']
   cmd += " %s" %kwargs['vm_name']
   cmd += " --nic net-id=%s"%kwargs['net_id']

   if kwargs.has_key('zone'):
     cmd += " --availability-zone nova:%s"%kwargs['zone']

   if kwargs.has_key('security-groups'):
     cmd += " --security-groups %s"%kwargs['security-groups']

   output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,120)

def live_migrate_vm(test_obj,handle,prompt,vm_id,new_host):

  cmd = "nova live-migration %s %s"%(vm_id,new_host)
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,120)

def get_vm_hostinfo(test_obj,handle,prompt,vm_name):

  cmd = 'nova show %s | grep hypervisor_hostname'%vm_name
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)
  current_hostname = re.search('\|\s*(\S+)\s*\|\s*(\S+)',output).group(2)
  print "###",current_hostname 
  return current_hostname.strip()

def get_vm_id(test_obj,handle,prompt,vm_name):

  cmd = "nova list"
  output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,60)

  vm_id = re.search('\|\s*(\S+)\s*\|\s*%s\s*'%vm_name,output).group(1)
  return vm_id

def get_tenant_id(kwargs):

    handle = kwargs['handle']
    prompt = kwargs['prompt']
    test_obj = kwargs['test_obj']
    tenant_name = kwargs['tenant_name']

    cmd = "keystone tenant-list | grep %s"%tenant_name
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30)
    
    ret = re.search('\|\s*(\S+)\s*\|\s*%s\s*\|'%tenant_name,output)
    if ret:
      return ret.group(1)
    else:
      return -1

def set_cinder_quota(kwargs):
    handle = kwargs['handle']
    prompt = kwargs['prompt']
    test_obj = kwargs['test_obj']
    tenant_name = kwargs['tenant_name']
    quota       = kwargs['quota']
    id          = kwargs['tenant_id']

    cmd = "cinder quota --gigabytes=%d %s"%(int(quota),id)
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30)


def get_build_branch(test_obj,handle,prompt):

    cmd = "dpkg --list | grep contrail-install-packages"
    output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30)
    return re.search('~(icehouse|havana|juno)\s+',output).group(1)

def wait_until_vm_status(kwargs):

    handle = kwargs['handle']
    prompt = kwargs['prompt']
    test_obj = kwargs['test_obj']

    vm_name = kwargs['vm_name']
    status = kwargs['status']
    power_state = kwargs['power_state']
    timeout = kwargs['timeout']

    vm_ready = False

    for i in xrange(1,timeout,30):
    
       cmd = "nova list"
       output = gen_lib.send_cmd(test_obj,handle,cmd,prompt,30)
       if re.search('%s\s*\|\s*%s\s*\|\s*%s\s*\|\s*%s\s*'%(vm_name,status,'(None|-)',power_state),output):
         vm_ready = True
         break
       time.sleep(30)
    return vm_ready   
     
