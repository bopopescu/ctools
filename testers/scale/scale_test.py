import time
import string
import random
import argparse
import commands
import exceptions
import traceback
import sys
import os
import lib
import MySQLdb

from multiprocessing import Process, Queue
     
from novaclient import exceptions as nova_exceptions
from keystoneclient.v2_0 import client as kclient
from novaclient import client as nova_client
from neutronclient.neutron import client as neutron_client

from copy_reg import pickle
from types import MethodType

OS_USERNAME    = os.environ['OS_USERNAME']
OS_PASSWORD    = os.environ['OS_PASSWORD']
OS_TENANT_NAME = os.environ['OS_TENANT_NAME']
OS_AUTH_URL    = os.environ['OS_AUTH_URL']

def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

pickle(MethodType, _pickle_method, _unpickle_method)

def retry(tries=12, delay=5):
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, result = tries, False
            while mtries > 0:
                lib.Print("Try count: %d"%mtries)
                mtries -= 1
                try:
                    result = f(*args, **kwargs)
                except:
                    if not mtries:
                        raise
                if result is True:
                    break
                time.sleep(delay)
            if not result:
                return False
            else:
                return (tries - mtries)*delay
        return f_retry
    return deco_retry


def random_string(prefix):
    return prefix+''.join(random.choice(string.hexdigits) for _ in range(4))


# A Class of UUIDs
class UUID(object):
    def __init__(self):
        self.vn_uuid = dict()
        self.port_id = dict()
        self.sg_id = dict()
        self.rule_id = dict()
        self.router_id = dict()
        self.policy_id = dict()
        self.fip_id = list()
        self.vm_id = dict()
        self.vn_obj = dict()
        self.sg_obj = dict()
        self.fip_pool_obj = None
        self.vm_obj = dict()
        self.st_obj = dict()
        self.si_obj = dict()
        self.policy_obj = dict()
        self.alloc_addr_list = []

class Openstack(object):

  def __init__(self,auth_url,username,password,tenant,auth_token=None):

     self.keystone_client = kclient.Client(username=username,
                                   password=password,
                                   tenant_name=tenant,
                                   auth_url=auth_url)

     if not auth_token:
       auth_token = self.keystone_client.auth_token

     self.nova_client = nova_client.Client('2',  auth_url=auth_url,
                                       username=username,
                                       api_key=password,
                                       project_id=tenant,
                                       auth_token=auth_token,
                                       insecure=True)
     ''' Get neutron client handle '''
     self.neutron_client = neutron_client.Client('2.0',
                                             auth_url=auth_url,
                                             username=username,
                                             password=password,
                                             tenant_name=tenant,
                                             insecure=True)

     self.id = UUID()

def parse_cli(args):
    '''Define and Parse arguments for the script'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username',
                        action='store',
                        default='admin',
                        help='Tenant user name [admin]')
    parser.add_argument('--image_id',
                        action='store',
                        default='imageid',
                        help='glance image-id')
    parser.add_argument('--n_tenants',
                        action='store',
                        default='1', type=int,
                        help='No of tenants to create [1]')
    parser.add_argument('--timeout',
                        action='store',
                        default='3600', type=int,
                        help='Max wait time in secs [1 hr]')
    parser.add_argument('--n_vns',
                        action='store',
                        default='1', type=int,
                        help='No of Vns to create per tenant [1]')
    parser.add_argument('--n_ports',
                        action='store',
                        default='1', type=int,
                        help='No of Ports to create per VN [0]')
    parser.add_argument('--n_sgs',
                        action='store',
                        default='1', type=int,
                        help='No of Security Groups to create per tenant [0]')
    parser.add_argument('--n_sg_rules',
                        action='store',
                        default='1', type=int,
                        help='No of Security Group Rules to create per SG [0]')
    parser.add_argument('--n_routers',
                        action='store',
                        default='1', type=int,
                        help='No of Routers to create per tenant [0]')
    parser.add_argument('--n_vms',
                        action='store',
                        default='1', type=int,
                        help='No of VMs to create per VN [0]')
    parser.add_argument('--n_fips',
                        action='store',
                        default='1', type=int,
                        help='No of Floating-IPs to create per tenant [0]')

    parser.add_argument('--keystone_ip',
                        action='store',
                        default='127.0.0.1',
                        help='Keystone IP [127.0.0.1]')

    parser.add_argument('--sm_node_ip',
                        action='store',
                        default='127.0.0.1',
                        help='SM node IP to fetch qcow image [127.0.0.1]')

    parser.add_argument('--mysql_passwd',
                        action='store',
                        default=None,
                        help="Root password for mysql, reqd in case of n_vms")
    parser.add_argument('--cleanup',
                        action='store',
                        default=1,
                        help="do cleanup at the end of test")

    pargs = parser.parse_args(args)
    return pargs

class DB(object):
    def __init__(self, user, password, host, database):

        self.db = MySQLdb.connect(user=user, passwd=password,
                                  host=host, db=database)
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

    def query_db(self, query):
        self.db.rollback()
        self.cursor.execute(query)
        return self.cursor.fetchall()

def get_mysql_token():

    fptr = open("/etc/contrail/mysql.token","r")
    return fptr.readline().strip()

class TestObj:

    def __init__ (self, args):
       self.args = args
       self.ostack_admin_obj = Openstack(OS_AUTH_URL,OS_USERNAME,OS_PASSWORD,OS_TENANT_NAME)

       if self.args.mysql_passwd == None :
          self.args.mysql_passwd = get_mysql_token()

       self.db = DB(user='root', password=self.args.mysql_passwd,
                         host=self.args.keystone_ip, database='nova')
    def read_from_queue(self, process, kwargs):
         try:
             self.tenants_list.append(kwargs['queue'].get(
                               timeout=self.args.timeout))
         except Empty:
             process.terminate()

    def get_name(self, tenant_name,prefix, index):
        return random_string(tenant_name + '-' + str(prefix) + str(index))

    def get_user_id(self, username):
        users = self.ostack_admin_obj.keystone_client.users.list()
        for user in users:
            if user.name == username:
                return user.id
        return None

    def get_role_id(self, role_name):
        roles = self.ostack_admin_obj.keystone_client.roles.list()
        for role in roles:
            if role.name == role_name:
                return role.id
        return None

    def create(self,queue):

        tenant_name = lib.random_string('Project')   
        self.tenant_id = lib.create_tenant(self.ostack_admin_obj,tenant_name)
        self.userid = self.get_user_id(self.args.username)
        role='admin'
        self.roleid = self.get_role_id(role)
        self.ostack_admin_obj.keystone_client.roles.add_user_role(tenant=self.tenant_id,
                                          user=self.userid,
                                          role=self.roleid)

        # Create VN
        for vn_index in range(0, self.args.n_vns):
            vn_name = self.get_name(tenant_name,'VN', vn_index)
            lib.Print("Creating VN : %s"%vn_name)
            lib.create_network(self.ostack_admin_obj,vn_name=vn_name)

        # Create Ports
        for vn_name in self.ostack_admin_obj.id.vn_uuid.keys():
            for port_index in range(0, self.args.n_ports):
                port_name = vn_name+'-Port'+str(port_index)
                lib.Print("Creating Port: %s"%port_name)
                lib.create_port(self.ostack_admin_obj,vn_name, port_name)


        # Create Security Group
        for sg_index in range(0, self.args.n_sgs):
            sg_name = self.get_name(tenant_name,'SG', sg_index)
            lib.create_security_group(self.ostack_admin_obj,sg_name)


        # Create Security Group Rules
        for sg_name in self.ostack_admin_obj.id.sg_id.keys():
            alloc_addr_list,address,cidr = lib.get_randmon_cidr(self.ostack_admin_obj.id.alloc_addr_list,mask=29)
            self.ostack_admin_obj.id.alloc_addr_list = alloc_addr_list
            for rule_index in range(0, self.args.n_sg_rules):
                lib.create_sg_rule(self.ostack_admin_obj,sg_name, rule_index+1000,
                                            rule_index+1000, cidr)

        # Create Router
        for rtr_index in range(0,self.args.n_routers):
            router_name = self.get_name(tenant_name,'RTR', rtr_index)
            lib.create_router(self.ostack_admin_obj,router_name)


        # Create Floating IP
        #for fip_index in range(0,self.args.n_fips):
        #    lib.create_floatingip(self.ostack_admin_obj,self.ostack_admin_obj.ext_vn_uuid)


        # Create virtual machines
        for vn_name in self.ostack_admin_obj.id.vn_uuid.keys():
            for vm_index in range(0, self.args.n_vms):
                vm_name = vn_name+'-VM'+random_string(str(vm_index))
                port_name = vn_name+'-Port'+str(vm_index)
                lib.Print('creating vm : %s,%s,%s'%(vm_name,vn_name,port_name))
                lib.create_vm(self.ostack_admin_obj,image_id=self.args.image_id,
                                       vm_name=vm_name, port_name=port_name,
                                       vn_name=vn_name,flavor=4)

        lib.Print("VM ids:%s"%self.ostack_admin_obj.id.vm_id)
        exit_value = self.verify_vms()

        queue.put(exit_value)

    @retry(60,60)
    def get_vm_states(self):

        print "List of pending VMs:",self.vm_ids
        for vm_id in self.vm_ids :
           query = 'select vm_state from instances where uuid="%s"'%vm_id
           lib.Print(query)
           result_dict = self.db.query_db(query)[0]
           lib.Print(str(result_dict))
           if result_dict['vm_state'] == 'active':
             lib.Print("VM is UP.instance_id :%s"%vm_id)
             self.vm_ids.remove(vm_id)
           else:
             lib.Print("VM is not UP.instance_id :%s"%vm_id)

        if len(self.vm_ids) == 0 :
           return True
        else:
           return False

       
    def verify_vms(self):

       self.vm_ids = self.ostack_admin_obj.id.vm_id.values()
       self.get_vm_states()

       if len(self.vm_ids) == 0 :
          lib.Print("PASS : ALL %d VMs came up correctly"%len(self.ostack_admin_obj.id.vm_id.values()))
          return 1
       else:
          lib.Print("ERROR : Some VMs did not come up correctly.Expected Active VM Count : %d,Actual ACtive VM Count: %d"%(len(self.ostack_admin_obj.id.vm_id.values()),(len(self.ostack_admin_obj.id.vm_id.values())-len(self.vm_ids))))
          return -1  

    def setUp(self):

        kwargs_list = list()
        queues = list()
        self.tenants_list = list()

        self.timeout = 3600

        num_of_vn = self.args.n_vns
        num_of_vms = self.args.n_vms

        for index in range(self.args.n_tenants):
            queues.append(Queue())
            kwargs_list.append({'queue': queues[index]})

        (success, timediff) = lib.create_n_process(self.create,
                                               self.args.n_tenants,
                                               kwargs_list,
                                               self.timeout,
                                               callback=self.read_from_queue)
        lib.Print('Time to create all tenants:%s'%str(timediff))

        lib.Print("####List of VMs running...")
        lib.list_all_vms(self.ostack_admin_obj)
        lib.Print("###########################")

        lib.Print("Return value :%d"%success)
        return success

    def upload_glance_image(self):

       if self.args.image_id != "imageid":
         return self.args.image_id

       try:
          image = self.ostack_admin_obj.nova_client.images.find(name='ubuntu')
          self.ostack_admin_obj.nova_client.images.delete(image.id)  
       except nova_exceptions.NotFound:
          pass

       try:
          lib.add_glance_image(self.ostack_admin_obj,'ubuntu','ovf','raw','http://%s/contrail/images/livemnfs.qcow2'%self.args.sm_node_ip) 
          image = self.ostack_admin_obj.nova_client.images.find(name='ubuntu')
          image_id = image.id
          self.args.image_id = image_id
       except:
          traceback.print_exc()

       return image_id


def cleanup(test_obj):

    lib.Print("calling cleanup...")
    lib.delete_test_vms(test_obj.ostack_admin_obj)
    lib.delete_test_tenants(test_obj.ostack_admin_obj)
    lib.delete_test_network(test_obj.ostack_admin_obj)
    lib.delete_all_sg(test_obj.ostack_admin_obj)
    lib.delete_all_routers(test_obj.ostack_admin_obj)



if __name__ == "__main__" :

    pargs = parse_cli(sys.argv[1:])

    test_obj = TestObj(pargs)
    
    cleanup(test_obj)

    test_obj.upload_glance_image()

    ret = test_obj.setUp()

    fp = open("/tmp/last_cmd_status","w")
    if ret == 100 :
      fp.write("0")
    else:
      fp.write("1")
    fp.close()


    if test_obj.args.cleanup :
       cleanup(test_obj)          
    


