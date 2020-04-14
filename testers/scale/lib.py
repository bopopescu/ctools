import sys
import time
import commands
import struct
import string
import socket
import random
from netaddr import *
from multiprocessing import Process, Queue
from datetime import datetime

def stripCtrl(str):
  result = ""
  for i in range(len(str)):
     #if (str[i] != '\r') and (str[i] != '\x08'):
     if (str[i] != '\x08'):
        result = result+str[i]
  return result

def Print(str,DEBUG=True):
   if DEBUG:
     print time.ctime()+"\n"+stripCtrl(str)
     sys.stdout.flush()

def list_all_vms(ostack_admin_obj):

   vms = ostack_admin_obj.nova_client.servers.list()
   for vm in vms :
     print vm.id,vm.name,vm.status

def delete_vm(ostack_admin_obj,vm_id):

   ostack_admin_obj.nova_client.servers.delete(vm_id)

def delete_vms(ostack_admin_obj,vm_id_list):

   print "List of VMs to be deleted...",vm_id_list
   for vm_id in vm_id_list:
       delete_vm(ostack_admin_obj,vm_id)

def delete_test_vms(ostack_admin_obj):

   vms = ostack_admin_obj.nova_client.servers.list()
   vm_id_list = []
   for vm in vms :
      if vm.name not in ['livemnfs']:
         vm_id_list.append(vm.id)

   delete_vms(ostack_admin_obj,vm_id_list)

   time.sleep(60)

def add_glance_image(ostack_admin_obj,image_name,image_format,disk_format,image_location):

     glance_kwargs = {'PRECMD': '',
                                'IMGLOCATION' : image_location,
                                'IMGNAME' : image_name,
                                'IMGFORMAT' : image_format,
                                'DISKFORMAT' : disk_format,
                                'IMGFILE_OPT' : ''}

     cmd = "source /etc/contrail/openstackrc; {PRECMD}"\
                 " glance image-create --name {IMGNAME}"\
                 " --is-public True --container-format {IMGFORMAT}"\
                 " --disk-format {DISKFORMAT} --location {IMGLOCATION} {IMGFILE_OPT}"
     print cmd.format(**glance_kwargs)
     commands.getoutput(cmd.format(**glance_kwargs))

def random_string(prefix):
    return prefix+''.join(random.choice(string.hexdigits) for _ in range(4))

def create_tenant(ostack_admin_obj,tenant_name):
   
    tenant_id = ostack_admin_obj.keystone_client.tenants.create(tenant_name).id
    return tenant_id

def create_n_process(target, n_process, kwargs_list, timeout=None, callback=None):
    process = list()
    events = list()
    for i in range(n_process):
        process.append(Process(target=target, kwargs=kwargs_list[i]))

    start_time = datetime.now()
    print 'Time at start ', str(start_time)

    start_process(process)
    if callback:
        callback_process(callback, process, kwargs_list)
    join_process(process, timeout)
    success = get_success_percentile(process)

    end_time = datetime.now()
    print 'Time at End ', str(end_time)

    return (success, end_time-start_time)

def start_process(processes):
    for process in processes:
        process.start()

def callback_process(callback, processes, kwargs_list):
    for i in xrange(len(processes)):
        callback(processes[i], kwargs_list[i])

def join_process(processes, timeout):
    for process in processes:
        process.join(timeout=timeout)
        process.terminate()

def get_success_percentile(processes):
    success = 0
    for process in processes:
        if process.exitcode == 0:
            success += 1
    return (success * 100)/len(processes)


def delete_test_tenants(ostack_admin_obj):

    tenant_list = ostack_admin_obj.keystone_client.tenants.list()
    for tenant in tenant_list :
      if tenant.name not in ['admin','demo','invisible_to_admin','service'] :
        tenant_id = tenant.id
        ostack_admin_obj.keystone_client.tenants.delete(tenant_id)

def delete_test_network(ostack_admin_obj):

    net_list = ostack_admin_obj.neutron_client.list_networks()['networks']
    subnet_list = ostack_admin_obj.neutron_client.list_subnets()['subnets']
    port_list = ostack_admin_obj.neutron_client.list_ports()['ports']

    print "net-list:",net_list
    print "subnet-list:",subnet_list
    print "port-list:",port_list

    for net in net_list :
       if net['name'] not in ['__link_local__','ip-fabric','livemnfs','default-virtual-network']:
         net_id = net['id']
         for subnet in subnet_list :
           if subnet['network_id'] == net_id :
             subnet_id = subnet['id']
             for port in port_list:
                if port['network_id'] == net_id:
                  Print("deleting port:%s"%port['id'])
                  ostack_admin_obj.neutron_client.delete_port(port['id'])
                  port_list.remove(port)
             Print("deleting subnet:%s"%subnet_id)
             ostack_admin_obj.neutron_client.delete_subnet(subnet_id)
             subnet_list.remove(subnet)
         Print("deleting net:%s"%net_id)
         ostack_admin_obj.neutron_client.delete_network(net_id)
           
           

def create_network(ostack_admin_obj,vn_name, mask=24, external=False):
        ''' Create Network via Neutron client call '''

        alloc_addr_list,address,cidr = get_randmon_cidr(ostack_admin_obj.id.alloc_addr_list,mask=mask)
        ostack_admin_obj.id.alloc_addr_list = alloc_addr_list
        vn_dict = {'name': vn_name}
        if external:
            vn_dict['router:external'] = True
        response = ostack_admin_obj.neutron_client.create_network({'network': vn_dict})

        ''' Store VN uuid and subnet uuid dicts '''
        net_id = response['network']['id']
        if external:
            ostack_admin_obj.ext_vn_uuid = net_id
        else:
            ostack_admin_obj.id.vn_uuid[vn_name] = net_id
        ostack_admin_obj.neutron_client.create_subnet({'subnet':
                                    {'cidr': cidr,
                                     'name': vn_name,
                                     'ip_version': 4,
                                     'network_id': net_id
                                    }})

def create_port(ostack_admin_obj, vn_name, port_name):
        ''' Create port using Neutron api '''
        port_dict = {'network_id': ostack_admin_obj.id.vn_uuid[vn_name]}
        response = ostack_admin_obj.neutron_client.create_port({'port': port_dict})
        ''' Store Port UUID's '''
        ostack_admin_obj.id.port_id[port_name] = response['port']['id']
        return ostack_admin_obj.id.port_id[port_name]

def create_security_group(ostack_admin_obj, sg_name):
        ''' Create Security Group '''
        sg_dict = {'name': sg_name}
        res = ostack_admin_obj.neutron_client.create_security_group({'security_group': sg_dict})
        ostack_admin_obj.id.sg_id[sg_name] = res['security_group']['id']

def create_sg_rule(ostack_admin_obj, sg_name, min, max, cidr='0.0.0.0/0',
                       direction='ingress', proto='tcp'):
        sg_id = ostack_admin_obj.id.sg_id[sg_name]
        rule_dict = {'security_group_id': sg_id, 'direction': direction,
                     'remote_ip_prefix': cidr, 'protocol': proto,
                     'port_range_min': min, 'port_range_max': max}
        response = ostack_admin_obj.neutron_client.create_security_group_rule(
                         {'security_group_rule': rule_dict})
        if sg_name not in ostack_admin_obj.id.rule_id:
            ostack_admin_obj.id.rule_id[sg_name] = list()
        ostack_admin_obj.id.rule_id[sg_name].append(response['security_group_rule']['id'])

def create_router(ostack_admin_obj, router_name):
        ''' Create Logical Router '''
        router_dict = {'name': router_name, 'admin_state_up': True}
        response = ostack_admin_obj.neutron_client.create_router({'router': router_dict})
        ostack_admin_obj.id.router_id[router_name] = response['router']['id']

def create_floatingip(ostack_admin_obj, ext_vn_uuid):
        ''' Create Floating IP '''
        fip_dict = {'floating_network_id': ext_vn_uuid}
        response = ostack_admin_obj.neutron.create_floatingip({'floatingip': fip_dict})
        ostack_admin_obj.id.fip_id.append(response['floatingip']['id'])

def create_vm(ostack_admin_obj, vm_name, image_id, port_name=None,
                  vn_name=None,flavor=5, compute_host=None, zone='nova'):
        ''' Create virtual machine '''
        nics = []
        launch_on = None
        port_id = None

        if port_name in ostack_admin_obj.id.port_id:
            port_id = ostack_admin_obj.id.port_id[port_name]
        if port_id is not None:
            nics = [{'port-id': port_id}]
        else:
            nics = [{'net-id': ostack_admin_obj.id.vn_uuid[vn_name]}]

        if compute_host:
            launch_on = zone + ':' + compute_host
        else:
            launch_on = 'nova'

        print vm_name,flavor,image_id,nics,launch_on

        try:
          response = ostack_admin_obj.nova_client.servers.create(name=vm_name,
                                            flavor=flavor,
                                            image=image_id,
                                            nics=nics,
                                            availability_zone=launch_on,
                                            max_count=1)
          ostack_admin_obj.id.vm_id[vm_name] = response.id
          print response
          print vm_name
          print ostack_admin_obj.id.vm_id   
        except:
          lib.Print("exception seen for vm : %s"%vm_name)

        return response, vm_name,ostack_admin_obj.id.vm_id

def delete_all_routers(ostack_admin_obj):
    
    routers_list = ostack_admin_obj.neutron_client.list_routers()['routers']
    for router in routers_list :
      router_id = router['id']
      ostack_admin_obj.neutron_client.delete_router(router_id)

def delete_all_sg(ostack_admin_obj):

    sg_list = ostack_admin_obj.neutron_client.list_security_groups()['security_groups']

    for sg in sg_list :
      if sg['name'] not in ['default'] :
        sg_id = sg['id']
        ostack_admin_obj.neutron_client.delete_security_group(sg_id)


def get_randmon_cidr(alloc_addr_list,mask=16):

    CLASSES='ABC'
    ip_class = random.choice(CLASSES)

    if ip_class == "A":
         first_octet = random.randint(1,126)

    if ip_class == "B":
         first_octet = random.randint(128,191)

    if ip_class == "C":
         first_octet = random.randint(192,223)

    second_octet = random.randint(0,254)
    third_octet = random.randint(0,254)
    fourth_octet = random.randint(0,254)
    address = "%i.%i.%i.%i" %(first_octet,second_octet,third_octet,fourth_octet)

    if address.startswith('169.254') or address in alloc_addr_list:
        alloc_addr_list,address,cidr = get_randmon_cidr(alloc_addr_list)
    else:
        alloc_addr_list.append(address)

    first_octet = address.split('.')[0]

    if first_octet <= 126 and first_octet >= 1:
       mask =  random.randint(8,30)

    if first_octet >=127 and first_octet <= 191:
       mask =  random.randint(16,30)

    if first_octet >=192 and first_octet <= 223:
       mask =  random.randint(24,30)

    cidr = address+'/'+str(mask)

    return alloc_addr_list,address,cidr

