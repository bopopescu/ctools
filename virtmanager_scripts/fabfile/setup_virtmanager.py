import os
import sys
import fabric
from fabric.api import run,put,env,parallel, cd
from fabric.operations import get, put
from fabric.context_managers import settings, hide
import re
import random, time

#env.hosts  = ['nodei12', 'nodei13','nodei14','nodei15']
env.user = 'root'
env.password = 'c0ntrail123'

env.no_keys = True

@parallel
def copy_virt_manager_script():
    if not fabric.contrib.files.exists('/root/tmp'):
        run('mkdir -p /root/tmp')
    if not fabric.contrib.files.exists("/root/tmp/InstallVirtManager.sh"):
        put('/cs-shared-test/cf/bin/InstallVirtManager.sh', '/root/tmp')

@parallel
def copy_image(image_source, image_dest='/root/tmp/', image_name=None):

    dest_folder = os.path.dirname(image_dest)
    rand_number = random.randint(1,10000)
    temp_file = "tmp_%s" % (rand_number)
    run('mkdir -p %s' % (dest_folder))
    with cd(dest_folder):
        src_file = os.path.basename(image_source)
        if image_source.endswith('.gz'):
            src_file_name = src_file.split('.gz')[0]
            temp_file = '%s.gz' % (temp_file)
        else:
            src_file_name = src_file
        image_name = image_name or src_file_name

        run('rm -f %s %s' % (image_name, src_file))
        run('wget %s -O %s' % (image_source, temp_file))
        if image_source.endswith('.gz'):
            run('gunzip -f %s' % (temp_file))
            temp_file = temp_file.split('.gz')[0]
        run('mv %s %s' % (temp_file, image_name))


@parallel
def make_copy_of_image(num_of_copy):
    for i in range (int(num_of_copy)):
        image_name = 'image'
        image_name = '%s%s.img'%(image_name,str(i))
        run('cp /root/tmp/std_ubuntu.img /root/tmp/%s'%image_name)

def create_vm(name , image , ram = '4096',network = {} , vcpus = '2', disk_format=None):
    '''
        network arg is a dict of the format below.
        You can specify any key that virt-manager accepts:
        network = [ {'bridge': 'br0', 'mac': 'xx:yy:zz:aa:bb:cc'}]
    '''
    if not network :
        network = [ { 'bridge': 'br0'}]

    if disk_format:
        disk_string = 'path=%s,format=%s' % (image, disk_format)
    else:
        disk_string = image

    full_network_arg = ''
    for net in network:
        network_arg = ' --network '
        for (key,value) in net.iteritems():
            network_arg += '%s=%s,' % (key, value)
        full_network_arg += network_arg
    
    cmd = 'virt-install --name %s \
        --ram %s \
        --disk %s \
        %s\
        --vcpus %s \
        --import --noautoconsole' %(name,ram,disk_string,full_network_arg,vcpus)

    run (cmd)

def create_vms_from_testbed(contrail_fab_path='/opt/contrail/utils'):
    sys.path.insert(0, contrail_fab_path)
    from fabfile.testbeds import testbed 
    vm_node_details = testbed.vm_node_details
    for (key, vm_node_detail) in vm_node_details.iteritems():
        if key == 'default':
            continue
        vm_detail = vm_node_details['default'].copy()
        vm_detail.update(vm_node_detail)
        with settings(host_string=vm_detail['server']):
            with settings(warn_only=True):
                delete_vm(vm_detail['name'])
            disk_file_name = '%s.img' % (vm_detail['name'])
            copy_image(vm_detail['image_source'], 
                       vm_detail['image_dest'], disk_file_name)
            create_vm(vm_detail['name'],
                      '%s/%s' % (vm_detail['image_dest'], disk_file_name),
                      vm_detail['ram'],
                      vm_detail['network'],
                      vm_detail['vcpus'],
                      vm_detail['disk_format'])
        for i in range(0,3):
            try:
                with settings(host_string=key):
                    change_host_name_of_vm(vm_detail['name'])
                break
            except :
                time.sleep(30)
        # end for

def delete_vm( vm_id ):
    cmd = "virsh destroy %s;virsh undefine %s"%(vm_id,vm_id)
    run(cmd)

def delete_all_vms():
    output = run('virsh list')
    vms = parse_virsh_list_output(output)
    for vm in vms:
        vm_id = vm[1]
        print vm_id
        cmd = "virsh destroy %s;virsh undefine %s"%(vm_id,vm_id)
        run(cmd)

def parse_virsh_list_output(output):
    ret = []
    output = output.split('\r\n')
    values = output[2:]
    for v in values:
        ret.append((v.split()) )
    return ret

@parallel
def delete_images():
    cmd = 'rm -rf /root/tmp/*.img'
    run(cmd)
        

def create_file( f , text):
    try:
        with open (f , "w") as fl:
            fl.write(text)
    except Exception as e:
            self.logger.exception("Got exception while creating %s as %s"%(f,e))

def generate_etc_hostname(hostname):
    text = "%s"%hostname
    file_name = "hostname"
    create_file(file_name , text)

def generate_etc_hosts(hostname):
    file_name = "hosts"
    text = "127.0.0.1       localhost\n127.0.1.1       \
            %s.englab.juniper.net    %s \n\n"%(hostname,hostname)
    create_file(file_name , text)
    
def change_host_name_of_vm(hostname):
    host = hostname
    generate_etc_hostname(host)
    generate_etc_hosts(host)
    #run("cp /etc/hostname /etc/hostname.old")
    run("cp /etc/hosts /etc/hosts.old")
    put("hostname", "/etc/")
    put("hosts", "/etc/")
    run("reboot")

def change_libvirt_type(ty = 'qemu'):
    virt_file = run("cd /etc/nova;grep -r 'libvirt_type' *")
    f = virt_file.split(":")[0]
    f = "/etc/nova/%s"%f
    if fabric.contrib.files.contains(f, 'libvirt_type'):
        fabric.contrib.files.sed(f, 'libvirt_type.*=.*', 'libvirt_type=qemu',backup='.bak')
    else:
        fabric.contrib.files.append(f, 'libvirt_type=qemu')
    run("cat %s"%f)
    run ("service nova-compute restart") 

def chnage_head_less_mode(mode = 'true'):
    f = '/etc/contrail/contrail-vrouter-agent.conf'
    if fabric.contrib.files.contains(f, 'headless_mode='):
        fabric.contrib.files.sed(f, '.*headless_mode=.*', 'headless_mode=true',backup='.bak')
    run ("service supervisor-vrouter restart") 

def service_start_stop(service = 'supervisor-vrouter',action = 'stop'):
    run ("service %s %s"%(service,action)) 

@parallel
def run_virtmanager_manager_script():
    output = run('/root/tmp/InstallVirtManager.sh')

@parallel
def reboot_server():
    run('reboot') 

@parallel
def setup_bridge_interface():

    run('rm -rf /etc/network/interfaces')
    put( 'interfaces' , '/etc/network/')
    run('/etc/init.d/networking restart')


if __name__ == "__main__":
    copy_virt()
