import os
import sys
import time
import uuid
import yaml
import argparse
import logging
from client import *
from output import Output
from netaddr import *

FIP_POOL_FQNAME = os.getenv('FIP_POOL_FQNAME', 'default-domain:admin:public:default')
API_SERVER_IP = os.getenv('API_SERVER_IP', '127.0.0.1')
MYDIR = os.path.dirname(os.path.abspath(__file__))

class Topology(object):
    def __init__(self, fip_pool_fqname, api_server_ip, project_name, image, instances, networks, irts=None, aaps=None):
        self.fip_pool_fqname = fip_pool_fqname
        self.api_server_ip = api_server_ip
        self.project_name = project_name
        self.image = image
        self.instances = instances
        self.networks = networks
        self.irts = irts or dict()
        self.aaps = aaps or dict()
        self.vn_objs = dict()
        self.port_objs = dict()
        self.iip_objs = dict()
        self.fip_objs = dict()
        self.vm_objs = dict()
        self.irt_objs = dict()

    def launch_and_verify(self):
        try:
            self.launch_topo()
            self.verify_active()
        except Exception as e:
            print 'Topology creation Failed. %s'%e
            self.delete_topo()
            raise

    @property
    def client_h(self):
        if not getattr(self, '_client_h', None):
            self._client_h = Client(self.project_name, self.api_server_ip)
        return self._client_h

    def setup(self):
        admin_client = Client(ADMIN_TENANT, self.api_server_ip)
        tenant = admin_client.create_tenant(self.project_name)
        self.tenant_obj = admin_client.get_project(id=str(uuid.UUID(tenant.id)))

    def wait_till_project_objs_delete(self):
        retry = 0
        max_retry = 20
        while True:
            tenant_obj = self.client_h.get_project(
                fq_name=[CONTRAIL_DOMAIN_NAME, self.project_name])
            vns = tenant_obj.get_virtual_networks()
            vmis = tenant_obj.get_virtual_machine_interfaces()
            sgs = tenant_obj.get_security_groups()
            irts = tenant_obj.get_interface_route_tables()
            nps = tenant_obj.get_network_policys()
            if vns or vmis or irts or nps or (sgs and len(sgs) > 1):
                if retry < max_retry:
                    retry += 1
                    time.sleep(15)
                    continue
                return False
            return True

    def teardown(self):
        assert self.wait_till_project_objs_delete(), 'Project %s still has objs'%self.project_name
        admin_client = Client(ADMIN_TENANT, self.api_server_ip)
        admin_client.delete_tenant(self.project_name)

    def create_networks(self):
        for vn_name, vn_prop in self.networks.iteritems():
            self.vn_objs[vn_name] = self.client_h.create_network(
                vn_name,
                cidr=vn_prop['cidr'],
                properties=vn_prop)

    def delete_networks(self):
        for vn_name in self.networks.iterkeys():
            self.client_h.delete_network(vn_name)

    def is_valid_cidr(self, cidr):
        try:
            IPNetwork(cidr)
            return True
        except AddrFormatError:
            return False

    def create_irts(self):
        for irt_name, networks in self.irts.iteritems():
            cidrs = list()
            for network in networks:
                if self.is_valid_cidr(network):
                    cidr = str(IPNetwork(network))
                else:
                    cidr = self.networks[network]['cidr']
                cidrs.append(cidr)
            self.irt_objs[irt_name] = self.client_h.create_irt(irt_name, cidrs)

    def delete_irts(self):
        for irt_name, networks in self.irts.iteritems():
            self.client_h.delete_irt(irt_name)

    def create_pfe_ports(self, instance, inst_name):
        inst_name = inst_name + '-pfe'
        for idx, port in enumerate(instance['ports'][:2]):
            network = port['network']
            port_name = inst_name + '-port%s'%idx
            (port_obj, iip_obj) = self.client_h.create_port(
                port_name, self.vn_objs[network])
            self.port_objs[port_name] = port_obj
            self.iip_objs[port_name] = iip_obj

    def create_ports(self):
        for instance in self.instances:
            for index in range(0, instance.get('count', 1)):
                inst_name = self.get_instance_name(instance, index)
                if instance['type'] in ['leaf', 'spine']:
                    self.create_pfe_ports(instance, inst_name)
                for idx, port in enumerate(instance['ports']):
                    network = port['network']
                    aap_ip = None
                    if port.get('aap'):
                        aap_ip = self.aaps[port['aap']]
                    irt_obj = None
                    if port.get('irt'):
                        irt_obj = self.irt_objs[port['irt']]
                    port_name = inst_name + '-port%s'%idx
                    (port_obj, iip_obj) = self.client_h.create_port(
                        port_name, self.vn_objs[network],
                        aap_ip=aap_ip, irt_obj=irt_obj)
                    self.port_objs[port_name] = port_obj
                    self.iip_objs[port_name] = iip_obj

    def delete_pfe_ports(self, instance, inst_name):
        inst_name = inst_name + '-pfe'
        for idx, port in enumerate(instance['ports'][:2]):
            port_name = inst_name + '-port%s'%idx
            self.client_h.delete_port(port_name)

    def delete_ports(self):
        for instance in self.instances:
            for index in range(0, instance.get('count', 1)):
                inst_name = self.get_instance_name(instance, index)
                if instance['type'] in ['leaf', 'spine']:
                    self.delete_pfe_ports(instance, inst_name)
                for idx, port in enumerate(instance['ports']):
                    port_name = inst_name + '-port%s'%idx
                    self.client_h.delete_port(port_name)

    def create_fips(self):
        for instance in self.instances:
            for index in range(0, instance.get('count', 1)):
                inst_name = self.get_instance_name(instance, index)
                fip_name = inst_name + '-fip'
                for idx, port in enumerate(instance['ports']):
                    network = port['network']
                    if network != 'management':
                        continue
                    port_name = inst_name + '-port%s'%idx
                    fip_obj = self.client_h.create_fip(fip_name,
                        self.fip_pool_fqname,
                        self.port_objs[port_name],
                        self.iip_objs[port_name],
                        self.tenant_obj)
                    self.fip_objs[fip_name] = fip_obj

    def delete_fips(self):
        for instance in self.instances:
            for index in range(0, instance.get('count', 1)):
                inst_name = self.get_instance_name(instance, index)
                fip_name = inst_name + '-fip'
                self.client_h.delete_fip(fip_name, self.fip_pool_fqname)

    def get_flavor(self, instance):
        flavor_name = instance.get('flavor')
        if not flavor_name:
            if instance['type'] in ['leaf', 'spine']:
                flavor_name = 'vqfx_flavor'
            else:
                flavor_name = instance['type']+'_flavor'
        return self.client_h.check_and_create_flavor(flavor_name)

    def get_image(self, instance, pfe=False):
        image_name = instance.get('image')
        if not image_name:
            if instance['type'] in ['leaf', 'spine']:
                image_name = 'vqfx-18.1R3-S2-re'
            elif instance['type'] in ['bms', 'appformix']:
                image_name = instance['type']
            else:
                image_name = self.image
        image_name = 'vqfx-pfe' if pfe else image_name
        return self.client_h.check_and_create_image(image_name)

    def create_pfe_vm(self, instance, inst_name):
        inst_name = inst_name + '-pfe'
        port_ids = list()
        flavor = self.get_flavor(instance)
        image = self.get_image(instance, pfe=True)
        for idx, port in enumerate(instance['ports'][:2]):
            port_name = inst_name + '-port%s'%idx
            port_ids.append(self.port_objs[port_name].uuid)
        vm_obj = self.client_h.launch_vm(inst_name, port_ids, flavor, image)
        self.vm_objs[inst_name] = vm_obj

    def create_vms(self):
        for instance in self.instances:
            flavor = self.get_flavor(instance)
            image = self.get_image(instance)
            user_data = None
            personality = dict()
            if instance.get('user_data'):
                user_data = MYDIR + '/' + instance['user_data']
            if instance.get('personality'):
                for k, v in instance['personality'].iteritems():
                    personality[k] = MYDIR + '/' + instance['personality']
            for index in range(0, instance.get('count', 1)):
                port_ids = list()
                inst_name = self.get_instance_name(instance, index)
                if instance['type'] in ['leaf', 'spine']:
                    self.create_pfe_vm(instance, inst_name)
                for idx, port in enumerate(instance['ports']):
                    port_name = inst_name + '-port%s'%idx
                    port_ids.append(self.port_objs[port_name].uuid)
                vm_obj = self.client_h.launch_vm(inst_name, port_ids, flavor, image,
                                                 user_data=user_data,
                                                 personality=personality,
                                                 metadata=instance.get('metadata'))
                self.vm_objs[inst_name] = vm_obj

    def delete_pfe_vm(self, instance, inst_name):
        inst_name = inst_name + '-pfe'
        self.client_h.delete_vm(inst_name)

    def delete_vms(self):
        for instance in self.instances:
            for index in range(0, instance.get('count', 1)):
                inst_name = self.get_instance_name(instance, index)
                if instance['type'] in ['leaf', 'spine']:
                    self.delete_pfe_vm(instance, inst_name)
                self.client_h.delete_vm(inst_name)

    def get_instance_name(self, instance, index):
        return '-'.join([instance['name'], str(index), self.client_h.project_id])

    def launch_topo(self):
        self.setup()
        self.create_networks()
        self.create_irts()
        self.create_ports()
        self.create_fips()
        self.create_vms()

    def verify_active(self):
        retry = 0
        max_retry = 30
        while True:
            for vm in self.vm_objs.itervalues():
                vm.get()
                if vm.status.upper() == 'ERROR':
                    raise Exception('VM %s(%s) is in ERROR state'%(vm.name, vm.id))
                if vm.status.upper() != 'ACTIVE' or \
                   int(vm.__dict__['OS-EXT-STS:power_state']) != 1:
                    break
            else:
                print 'All the VMs are launched successfully'
                return True
            if retry < max_retry:
                retry += 1
                time.sleep(30)
            else:
                print 'All the VMs are not launched successfully even after 15 mins'

    def delete_topo(self):
        self.delete_vms()
        self.delete_fips()
        self.delete_ports()
        self.delete_irts()
        self.delete_networks()
        self.teardown()

    def get_instance_info(self):
        instances = dict()
        for instance in self.instances:
            for index in range(0, instance.get('count', 1)):
                fip = None
                inst = {'name': instance['name']}
                inst_name = self.get_instance_name(instance, index)
                fip_name = inst_name + '-fip'
                if fip_name in self.fip_objs:
                    fip = self.client_h.get_fip_address(
                        fq_name=self.fip_objs[fip_name].get_fq_name())
                    inst['fip'] = fip
                for idx, port in enumerate(instance['ports']):
                    network = port['network']
                    port_name = inst_name + '-port%s'%idx
                    address = self.client_h.get_address(port_name)
                    mac = self.client_h.get_mac_address(port_name)
                    port_info = {'ip': address, 'mac': mac}
                    if instance['type'] in ['leaf', 'spine'] and idx > 2:
                        port_info['interface'] = 'xe-0/0/%s'%(int(idx)-3)
                    if port.get('aap'):
                        aap_name = port['aap']
                        port_info['aap_ip'] = self.aaps[aap_name]
                    port_info['gw'] = self.client_h.get_gateway(network)
                    inst[network] = port_info
                instances.update({inst_name: inst})
        print yaml.safe_dump(instances, default_flow_style=False)
        with open('ocontent.yaml', 'w') as fd:
            yaml.safe_dump(instances, fd, default_flow_style=False)
        return instances

def read_yaml(filename):
    with open(filename, 'r') as fd:
        yargs = yaml.load(fd)
    return yargs

def write_yaml(content, filename):
    with open(filename, 'w') as fd:
        yaml.safe_dump(content, fd, default_flow_style=False)

def create_topology(topology, oper, project_name, image):
    yargs = read_yaml(topology)
    pobj = Topology(yargs.get('fip_pool_fqname') or FIP_POOL_FQNAME,
                    yargs.get('api_server_ip') or API_SERVER_IP,
                    project_name,
                    image,
                    yargs['instances'],
                    yargs['networks'],
                    aaps = yargs.get('allowed_address_pairs'),
                    irts = yargs.get('interface_route_tables'))
    if oper.lower().startswith('del'):
        pobj.delete_topo()
    elif oper.lower() == 'add':
        pobj.launch_and_verify()
        output = pobj.get_instance_info()
#        filename = filename or '/tmp/%s-outputs.yaml'%project_name
#        with open(filename, 'w') as fd:
#            yaml.safe_dump(output, fd, default_flow_style=False)
        return output
    else:
        raise Exception()

def write_all_yml(topology, configs, instances_info, filename,
                  version, sku, branch, report_path, appformix_version):
    tcontent = read_yaml(topology)
    ccontent = read_yaml(configs)
    output = Output(tcontent['instances'], tcontent['networks'],
                    instances_info,
                    ccontent.get('global_configuration'),
                    ccontent.get('contrail_configuration'),
                    ccontent.get('test_configuration'),
                    ccontent.get('deployment'),
                    ccontent.get('provider_config'),
                    ccontent.get('orchestrator_configuration'),
                    version, sku, branch, report_path,
                    appformix_version)
    ocontent = output.generate_all_yml()
    write_yaml(ocontent, filename)

def parse_cli(args):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--topology', required=True, metavar="FILE",
                        help='location of the topology file')
    parser.add_argument('-c', '--configs', metavar="FILE",
                        help='location of the configuration file')
    parser.add_argument('-p', '--project', required=True,
                        help='isolated project within which the contrail cluster will be launched')
    parser.add_argument('-i', '--image', default=os.getenv('OSIMAGE'),
                        help='OS to use for contrail services (eg. centos-7.5)')
    parser.add_argument('-v', '--version', default=os.getenv('VERSION'),
                        help='contrail version eg: ocata-main-244')
    parser.add_argument('-a', '--appformix_version', default=os.getenv('APPFORMIX_VERSION'),
                        help='appformix version eg: 2.18.1')
    parser.add_argument('-s', '--sku', default=os.getenv('SKU'),
                        help='openstack sku eg: ocata')
    parser.add_argument('-b', '--branch', default=os.getenv('BRANCH'),
                        help='contrail branch')
    parser.add_argument('-r', '--report_path', default=os.getenv('WEBSERVER_REPORT_PATH'),
                        help='path in webserver to upload the reports to')
    parser.add_argument('-o', '--oper', default='add',
                        help='operation to perform (add/delete)')
    parser.add_argument('-f', '--filename',
                        help='where to store the generated all.yml')
    pargs = parser.parse_args(args)
    return pargs

if __name__ == '__main__':
    pargs = parse_cli(sys.argv[1:])
    instance_info = create_topology(pargs.topology, pargs.oper,
                                    pargs.project, pargs.image)
    if instance_info and pargs.oper.lower() == 'add' and pargs.filename:
        write_all_yml(pargs.topology, pargs.configs, instance_info,
                      pargs.filename, pargs.version, pargs.sku,
                      pargs.branch, pargs.report_path, pargs.appformix_version)

