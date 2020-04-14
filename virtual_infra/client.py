import os
import shlex
from keystoneauth1 import identity, session
from keystoneclient import client
from novaclient import client as nova_client
from glanceclient import Client as glance_client
from vnc_api.vnc_api import *
import logging
import fcntl
import subprocess

OS_AUTH_URL = os.getenv('OS_AUTH_URL', 'http://127.0.0.1:5000/v2.0')
OS_USERNAME = os.getenv('OS_USERNAME', 'admin')
OS_PASSWORD = os.getenv('OS_PASSWORD', 'contrail123')
ADMIN_TENANT = os.getenv('OS_TENANT_NAME') or os.getenv('OS_PROJECT_NAME') or 'admin'
OS_USER_DOMAIN_NAME = os.getenv('OS_USER_DOMAIN_NAME', 'Default')
OS_PROJECT_DOMAIN_NAME = os.getenv('OS_PROJECT_DOMAIN_NAME', 'Default')
OS_DOMAIN_NAME = os.getenv('OS_DOMAIN_NAME', 'Default')
if OS_DOMAIN_NAME == 'Default':
   CONTRAIL_DOMAIN_NAME = 'default-domain'
CONTRAIL_API_PORT = '8082'
ADMIN_ROLE = 'admin'
log = True

BASE_URL = "http://10.84.5.120/images/soumilk/vm_images"
IMAGE_LOCATION = {"vmx-re":         "vmx_re_image_18_1.qcow2.gz",
                  "vmx-fpc":        "vmx_fpc_image_18_1.qcow2",
                  "centos-7.4":     "CentOS-7-x86_64-GenericCloud.qcow2",
                  "centos-7.5":     "centos-7.5_3.10.0-862.3.2.qcow2.gz",
                  "centos-7.6":     "centos-7.6.qcow2",
                  "centos-7.6-3.10.0-957.27.2":     "centos-7.6.qcow2-3.10.0-957.27.2",
                  "redhat-7.5":     "rhel-server-7.5-update-4-x86_64-kvm.qcow2",
                  "ubuntu-16.04.3": "ub-16-04-3.qcow2",
                  "ubuntu-16.04.5": "ubuntu-16.04-server-cloudimg-amd64-disk1.img.gz",
		  "ubuntu-18.04.2": "ubuntu-18.04-server-cloudimg-amd64.qcow2",
                  "vqfx-18.1R3-S2-re": "jinstall-vqfx-10-f-18.1R3-S2.5.qcow2.gz",
                  "vqfx-pfe":       "vqfx_cosim_01.img.gz",
                  "bms":            "centos-7.5.qcow2.gz",
                  "appformix":      "centos-7.5_3.10.0-862.3.2.qcow2.gz",
                  "rhel-7.5":       "rhel-server-7.5-update-4-x86_64-kvm.qcow2"
                 }
DEFAULT_PARAMS = "--container-format bare --disk-format qcow2"
IMAGE_PROPERTIES = {'bms': "--property hw_vif_model=e1000 --property hw_disk_bus=ide",
                    'vqfx-18.1R3-S2-re': "--property hw_vif_model=e1000 --property hw_disk_bus=ide",
                    'vqfx-pfe': "--property hw_vif_model=e1000 --property hw_disk_bus=ide",
                    'vmx-fpc': "--property hw_vif_model=virtio --property hw_disk_bus=ide",
                    'vmx-re': "--property hw_vif_model=virtio --property hw_disk_bus=ide"
                   }
FLAVORS = {'controller_flavor': (32768, 300, 10),
           'openstack_flavor': (16384, 100, 8),
           'control_flavor': (4096, 40, 4),
           'analytics_flavor': (4096, 40, 4),
           'config_flavor': (4096, 40, 4),
           'compute_flavor': (16384, 100, 8),
           'csn_flavor': (4096, 20, 2),
           'command_flavor': (4096, 20, 2),
           'k8s_master_flavor': (4096, 20, 2),
           'vqfx_flavor': (4096, 16, 2),
           'bms_flavor': (1024, 10, 1),
           'vmx-fpc_flavor': (16384, 40, 7),
           'vmx-re_flavor': (4096, 40, 1),
           'appformix_flavor': (16384, 100, 8),
           'helm-kube-master_flavor': (48000, 300, 30)
          }
FLAVOR_PROPERTIES = {'vmx-re_flavor': {"hw:cpu_policy": "dedicated",
                         "aggregate_instance_extra_specs:global-grouppinned": "true"}}

class Lock:
    def __init__(self, filename):
        self.filename = filename
        self.handle = open(filename, 'w')

    def acquire(self):
        fcntl.flock(self.handle, fcntl.LOCK_EX)

    def release(self):
        fcntl.flock(self.handle, fcntl.LOCK_UN)

    def __del__(self):
        self.handle.close()

class Client(object):
    def __init__(self, project_name, api_server_ip):
        self.project_name = project_name
        self.version = self.get_version()
        self.session = self.get_session()
        self.keystone = self.get_client()
        self.api_server_ip = api_server_ip

    def get_version(self):
        pattern = 'http[s]?://(?P<ip>\S+):(?P<port>\d+)/*(?P<version>\S*)'
        version = re.match(pattern, OS_AUTH_URL).group('version')
        return '3' if 'v3' in version else '2'

    def get_session(self):
        if self.version == '2':
           auth = identity.v2.Password(auth_url=OS_AUTH_URL,
                                       username=OS_USERNAME,
                                       password=OS_PASSWORD,
                                       tenant_name=self.project_name)
        elif self.version == '3':
           auth = identity.v3.Password(auth_url=OS_AUTH_URL,
                                       username=OS_USERNAME,
                                       password=OS_PASSWORD,
                                       project_name=self.project_name,
                                       user_domain_name=OS_USER_DOMAIN_NAME,
                                       project_domain_name=OS_PROJECT_DOMAIN_NAME)
        return session.Session(auth=auth, verify=False)

    def get_client(self):
        return client.Client(version=self.version, session=self.session,
                             auth_url=OS_AUTH_URL)

    @property
    def vnc_api_h(self):
        if not getattr(self, '_vnc_api_h', None):
            self._vnc_api_h = VncApi(api_server_host=self.api_server_ip,
                                     api_server_port=CONTRAIL_API_PORT,
                                     auth_token=self.session.get_token())
        return self._vnc_api_h

    @property
    def nova_h(self):
        if not getattr(self, '_nova_h', None):
            self._nova_h = nova_client.Client('2', session=self.session)
        return self._nova_h

    @property
    def glance_h(self):
        if not getattr(self, '_glance_h', None):
            self._glance_h = glance_client('2', session=self.session)
        return self._glance_h

    def get_user(self, username):
        users = self.keystone.users.list()
        for user in users:
            if user.name == username:
                return user
        raise Exception('User %s not found'%username)

    def get_role(self, rolename):
        roles = self.keystone.roles.list()
        for role in roles:
            if role.name == rolename:
                return role
        raise Exception('role %s not found'%rolename)

    def find_domain(self, name):
        return self.keystone.domains.find(name=name)

    def create_tenant(self, name):
        if self.version == '3':
            domain=self.find_domain(OS_PROJECT_DOMAIN_NAME)
            tenant = self.keystone.projects.create(name=name, domain=domain)
            self.keystone.roles.grant(self.get_role(ADMIN_ROLE),
                                      user=self.get_user(OS_USERNAME),
                                      project=tenant.id)
        else:
            tenant = self.keystone.tenants.create(name)
            self.keystone.roles.add_user_role(tenant=tenant.id,
                                              user=self.get_user(OS_USERNAME),
                                              role=self.get_role(ADMIN_ROLE))
        return tenant

    def delete_tenant(self, name):
        if self.version == '3':
            obj = self.keystone.projects.find(name=name)
            self.keystone.projects.delete(obj)
        else:
            obj = self.keystone.tenants.find(name=name)
            self.keystone.tenants.delete(obj)

    def _parse_image_params(self, params):
        kwargs = dict()
        key = None
        for elem in shlex.split(params):
            if elem.startswith('-'):
                key = elem.strip('-').replace('-', '_')
            else:
                if key == 'property':
                    kwargs.update(dict([elem.split('=')]))
                else:
                    kwargs[key] = elem
        return kwargs

    def create_image(self, name, filename, params=''):
        if not os.path.isfile(filename):
            raise Exception('File %s not found'%filename)
        params = "%s %s %s"%(DEFAULT_PARAMS,
                             IMAGE_PROPERTIES.get(name, ''),
                             params)
        kwargs = self._parse_image_params(params)
        image = self.glance_h.images.create(name=name, visibility='public', **kwargs)
        self.upload_image(image['id'], filename)
        return image

    def upload_image(self, uuid, filename):
        self.glance_h.images.upload(uuid, open(filename, 'rb'))

    def download_image(self, name):
        def run_cmd(cmd):
            return subprocess.check_output(cmd, shell=True).strip()
        dnld_location = '/tmp/'+IMAGE_LOCATION[name]
        run_cmd('rm -f %s'%dnld_location)
        cmd = 'wget %s/%s -O %s'%(BASE_URL,
                                  IMAGE_LOCATION[name],
                                  dnld_location)
        output = run_cmd(cmd)
        if not os.path.exists(dnld_location):
            raise Exception('Unable to download image %s'%name)
        if dnld_location.endswith('.gz'):
            cmd = 'gunzip -f %s'%dnld_location
            run_cmd(cmd)
            dnld_location, extension = os.path.splitext(dnld_location)
        return dnld_location

    def check_and_create_image(self, name):
        f = '/tmp/%s.image.lock'%name
        lock = Lock(f)
        try:
            lock.acquire()
            for image in self.glance_h.images.list():
                if image.name == name:
                    break
            else:
                filename = self.download_image(name)
                image = self.create_image(name, filename)
        finally:
            lock.release() 
        return image

    def create_flavor(self, name):
        ram, disk, vcpu = FLAVORS.get(name)
        flavor = self.nova_h.flavors.create(name=name,
                                            vcpus=vcpu,
                                            ram=ram,
                                            disk=disk)
        if name in FLAVOR_PROPERTIES:
            flavor.set_keys(FLAVOR_PROPERTIES[name])
        return flavor

    def check_and_create_flavor(self, name):
        f = '/tmp/%s.flavor.lock'%name
        lock = Lock(f)
        try:
            lock.acquire()
            for flavor in self.nova_h.flavors.list():
                if flavor.name == name:
                    break
            else:
                flavor = self.create_flavor(name)
        finally:
            lock.release()
        return flavor

    def create_network(self, name, cidr, properties=None):
        network, mask = cidr.split('/')
        fq_name = [CONTRAIL_DOMAIN_NAME, self.project_name, name]
        ipam_subnet_type = IpamSubnetType(subnet=SubnetType(network, int(mask)),
                                          addr_from_start=True)
        vn_obj = VirtualNetwork(name, parent_type='project', fq_name=fq_name)
        if properties:
            if 'gateway' in properties:
                if properties['gateway'] is None:
                    dhcp_opt = DhcpOptionType(dhcp_option_name='3',
                                              dhcp_option_value='0.0.0.0')
                    dhcp_opts = DhcpOptionsListType(dhcp_option=[dhcp_opt])
                    ipam_subnet_type.dhcp_option_list = dhcp_opts
                else:
                    ipam_subnet_type.default_gateway = properties['gateway']
            if properties.get('enable_dhcp') == False:
                ipam_subnet_type.set_enable_dhcp(False)
            if properties.get('flood_unknown_unicast') == True:
                vn_obj.flood_unknown_unicast = True
            vn_prop = VirtualNetworkType()
            if properties.get('forwarding_mode'):
                vn_prop.set_forwarding_mode(properties.get('forwarding_mode'))
                if properties['forwarding_mode'] == 'l2':
                    dhcp_opt = DhcpOptionType(dhcp_option_name='6',
                                              dhcp_option_value='0.0.0.0')
                    dhcp_opts = ipam_subnet_type.get_dhcp_option_list() or \
                        DhcpOptionsListType(dhcp_option=[])
                    dhcp_opts.add_dhcp_option(dhcp_opt)
                    ipam_subnet_type.dhcp_option_list = dhcp_opts
            vn_obj.set_virtual_network_properties(vn_prop)
        vn_obj.add_network_ipam(NetworkIpam(), VnSubnetsType([ipam_subnet_type]))
        self.vnc_api_h.virtual_network_create(vn_obj)
        return vn_obj

    def delete_network(self, name):
        fq_name = [CONTRAIL_DOMAIN_NAME, self.project_name, name]
        try:
            self.vnc_api_h.virtual_network_delete(fq_name=fq_name)
        except NoIdError:
            pass

    def create_port(self, name, vn_obj, aap_ip=None, irt_obj=None):
        fq_name = [CONTRAIL_DOMAIN_NAME, self.project_name, name]
        port_obj = VirtualMachineInterface(name, parent_type='project',
                                           fq_name=fq_name)
        if aap_ip:
            ip = SubnetType(ip_prefix=aap_ip, ip_prefix_len=32)
            aap = AllowedAddressPair(ip=ip, address_mode='active-standby')
            aaps = AllowedAddressPairs(allowed_address_pair=[aap])
            port_obj.set_virtual_machine_interface_allowed_address_pairs(aaps)
        port_obj.add_virtual_network(vn_obj)
        if irt_obj:
            port_obj.add_interface_route_table(irt_obj)
        self.vnc_api_h.virtual_machine_interface_create(port_obj)

        iip_obj = InstanceIp(name=name)
        iip_obj.add_virtual_network(vn_obj)
        iip_obj.add_virtual_machine_interface(port_obj)
        self.vnc_api_h.instance_ip_create(iip_obj)
        return (port_obj, iip_obj)

    def delete_port(self, name):
        fq_name = [CONTRAIL_DOMAIN_NAME, self.project_name, name]
        try:
            self.vnc_api_h.instance_ip_delete(fq_name=[name])
        except NoIdError:
            pass
        try:
            self.vnc_api_h.virtual_machine_interface_delete(fq_name=fq_name)
        except NoIdError:
            pass

    def get_address(self, name):
        obj = self.vnc_api_h.instance_ip_read(fq_name=[name])
        return obj.get_instance_ip_address()

    def get_mac_address(self, name):
        fq_name = [CONTRAIL_DOMAIN_NAME, self.project_name, name]
        obj = self.vnc_api_h.virtual_machine_interface_read(fq_name=fq_name)
        mac = obj.get_virtual_machine_interface_mac_addresses()
        return mac.mac_address[0]

    def get_gateway(self, name):
        fq_name = [CONTRAIL_DOMAIN_NAME, self.project_name, name]
        obj = self.vnc_api_h.virtual_network_read(fq_name=fq_name)
        ipam = obj.get_network_ipam_refs()[0]
        return ipam['attr'].get_ipam_subnets()[0].default_gateway

    def create_irt(self, name, cidrs):
        fq_name = [CONTRAIL_DOMAIN_NAME, self.project_name, name]
        routes = list()
        for cidr in cidrs:
            attr = CommunityAttributes(['no-reoriginate', 'no-export'])
            rt = RouteType(prefix = cidr,
                           community_attributes=attr)
            routes.append(rt)
        intf_route_table = InterfaceRouteTable(
            name, fq_name=fq_name,
            parent_type='project',
            interface_route_table_routes=RouteTableType(routes))
        self.vnc_api_h.interface_route_table_create(intf_route_table)
        return intf_route_table

    def delete_irt(self, name):
        fq_name = [CONTRAIL_DOMAIN_NAME, self.project_name, name]
        try:
            self.vnc_api_h.interface_route_table_delete(fq_name=fq_name)
        except NoIdError:
            pass

    def create_fip(self, name, fip_pool_fqname, port_obj, iip_obj, project_obj):
        fq_name = fip_pool_fqname.split(':') + [name]
        fip_obj = FloatingIp(name=name, parent_type='floating-ip-pool', fq_name=fq_name)
        fip_obj.add_virtual_machine_interface(port_obj)
        fip_obj.add_project(project_obj)
        self.vnc_api_h.floating_ip_create(fip_obj)
        return fip_obj

    def delete_fip(self, name, fip_pool_fqname):
        fq_name = fip_pool_fqname.split(":") + [name]
        try:
            self.vnc_api_h.floating_ip_delete(fq_name=fq_name)
        except:
            pass

    def get_fip_address(self, **kwargs):
        obj = self.vnc_api_h.floating_ip_read(**kwargs)
        return obj.get_floating_ip_address()

    def launch_vm(self, name, ports, flavor, image,
                  personality=None, metadata=None, user_data=None):
        nics = [{'port-id': port} for port in ports]
        files = None
        if personality:
            files = {k: open(v, 'r') for k,v in personality.iteritems()}
        if user_data:
            with open(user_data) as f:
                user_data = f.readlines()
            user_data = ''.join(user_data)
        if metadata:
            for k in metadata.keys():
                metadata[k] = str(metadata[k])
        vm_obj = self.nova_h.servers.create(name=name, flavor=flavor,
                                            image=image, nics=nics,
                                            meta=metadata, files=files,
                                            userdata=user_data,
                                            config_drive=True if files else None)
        print 'Launched VM %s'%name
        return vm_obj

    def delete_vm(self, name):
        for i in range(1, 4):
            try:
                vms = self.list_vms()
                for vm in vms:
                    if vm.name == name:
                        vm.delete()
                        return
            except:
                if i == 3:
                    raise
        print 'VM Delete: VM %s not found'%name

    def list_vms(self):
        return self.nova_h.servers.list()

    def get_project(self, **kwargs):
        return self.vnc_api_h.project_read(**kwargs)

    @property
    def project_id(self):
        if not getattr(self, '_project_id', None):
            project_obj = self.get_project(
                fq_name=[CONTRAIL_DOMAIN_NAME, self.project_name])
            self._project_id = project_obj.uuid.replace('-','')
        return self._project_id
