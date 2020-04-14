#
# Collection of helper routines to provision k8s nested
#

import os
import time
import yaml
import uuid
from fabric import Connection
import keystoneauth1.identity
import keystoneauth1.session
import heatclient.client
from vnc_api.vnc_api import *
import templates

GBL_VROUTER_FQN = ['default-global-system-config',
                   'default-global-vrouter-config']
DFLT_CLUSTERS = [{
    'name': 'cls1',
    'network': {
        'name': 'k8net',
        'prefix': '1.1.1.0/24',
        'fabric_snat': True,
    },
    'master': 'k8m',
    'slave1': 'k8s1',
    'slave2': 'k8s2',
}]
BGP_ADDR_FAMILIES = ['inet-vpn']
BGP_RI = ['default-domain', 'default-project', 'ip-fabric', '__default__']

HEAT_TRIES = 60
HEAT_DELAY = 5
LLS_ENV = 'linklocalservices.yml'
PAP_ENV = 'portallocationpools.yml'
CMN_TMPL = 'common-tmpl.yml'
CMN_ENV = 'common-env.yml'
PRJ_TMPL = 'project-tmpl.yml'
PRJ_ENV = 'project-env.yml'
CLS_TMPL = 'cluster-tmpl.yml'
CLS_ENV = 'cluster-env.yml'
JUJU_CLS_TMPL = 'jujucluster-tmpl.yml'
JUJU_CLS_ENV = 'jujucluster-env.yml'


_cleanup_stack = []

def push_cleanup (fn, *args):
    _cleanup_stack.append((fn,args))

def run_cleanup ():
    if os.getenv('PROV_CLEANUP', True):
        print 'running cleanup'
        while _cleanup_stack:
            fn, args = _cleanup_stack.pop(-1)
            fn(*args)

def add_linklocal_service (vnc, lls, info):
    if not lls:
        lls = yaml.load(open(LLS_ENV, 'r'))['linklocal_services']

    # retain existing service entries, like metadata service
    obj1 = LinklocalServicesTypes()
    obj0 = vnc.global_vrouter_config_read(fq_name=GBL_VROUTER_FQN)
    saved_lls = obj0.get_linklocal_services()
    if saved_lls:
        push_cleanup(restore_linklocal_service, vnc, saved_lls)
        for svc in saved_lls.get_linklocal_service_entry():
            obj1.add_linklocal_service_entry(svc)
    else:
        push_cleanup(restore_linklocal_service, vnc,
                     LinklocalServicesType())

    # add new service entries
    for svc in lls:
        obj2 = LinklocalServiceEntryType()
        print 'Adding Linklocal Service: ' + svc['name']
        obj2.set_linklocal_service_name(svc['name'])
        obj2.set_linklocal_service_ip(svc['linklocal_ip'])
        obj2.set_linklocal_service_port(svc['linklocal_port'])
        obj2.set_ip_fabric_service_port(svc['fabric_port'])
        for ip in svc['fabric_ip']:
            obj2.add_ip_fabric_service_ip(ip)
        if svc['linklocal_port'] == 9091:
            info['vrouter_vip'] = svc['linklocal_ip']
        obj1.add_linklocal_service_entry(obj2)

    obj0.set_linklocal_services(obj1)
    return vnc.global_vrouter_config_update(obj0)

def restore_linklocal_service (vnc, lls):
    print 'Restoring Linklocal Services'
    obj0 = vnc.global_vrouter_config_read(fq_name=GBL_VROUTER_FQN)
    obj0.set_linklocal_services(lls)
    vnc.global_vrouter_config_update(obj0)

def add_port_translation_pool (vnc, pp):
    if not pp:
        pp = yaml.load(open(PAP_ENV, 'r'))['port_translation_pools']

    # retain existing port translation entries
    obj1 = PortTranslationPools()
    obj0 = vnc.global_vrouter_config_read(fq_name=GBL_VROUTER_FQN)
    saved_pp = obj0.get_port_translation_pools()
    if saved_pp:
        push_cleanup(restore_port_translation_pool, vnc, saved_pp)
        for pool in saved_pp.get_port_translation_pool():
            obj1.add_port_translation_pool(pool)
    else:
        push_cleanup(restore_port_translation_pool, vnc,
                     PortTranslationPools())

    # add new port translation entries
    for pool in pp:
        obj2 = PortTranslationPool()
        print 'Adding Port Translation Pool for: ' + pool['protocol']
        obj2.set_protocol(pool['protocol'])
        obj2.set_port_count(str(pool['port_count']))
        obj1.add_port_translation_pool(obj2)

    obj0.set_port_translation_pools(obj1)
    return vnc.global_vrouter_config_update(obj0)

def restore_port_translation_pool (vnc, pp):
    print 'Restoring Port Translation Pool'
    obj0 = vnc.global_vrouter_config_read(fq_name=GBL_VROUTER_FQN)
    obj0.set_port_translation_pools(pp)
    vnc.global_vrouter_config_update(obj0)

def get_vnc_handle (desc, cred, project=None):
    api_server = desc['test_configuration'].get('config_api_ip') or \
                 desc['contrail_configuration'].get('CONFIG_API_VIP')
    if not api_server:
        msg = 'specify config_api_ip under test_configuration '
        msg += 'or CONFIG_API_VIP under contrail_configuration'
        raise Exception(msg)
    print 'Connecting to VNC: ' + api_server
    tenant_name = project if project else cred['tenant']
    proto = cred['auth-url'].split('/')[0][:-1]
    ver = cred['auth-url'].split('/')[-1]
    host, port = cred['auth-url'].split('/')[2].split(':')
    if ver == 'v3':
        url = '/v3/auth/tokens'
    else:
        raise Exception('unknown keystone version %s' % ver)
    return VncApi(username=cred['user'], password=cred['passwd'],
                    tenant_name=tenant_name, api_server_host=api_server,
                    auth_host=host, auth_port=port, auth_protocol=proto,
                    auth_url=url)

def get_heat_handle (cred, project=None):
    project_name = project if project else cred['project']
    print 'keystone ' + project_name + ':' + cred['auth-url']
    session = keystoneauth1.session.Session(
                auth=keystoneauth1.identity.v3.Password(
                    auth_url=cred['auth-url'],
                    username=cred['user'],
                    password=cred['passwd'],
                    project_name=project_name,
                    user_domain_name=cred['user-domain'],
                    project_domain_name=cred['project-domain']),
                verify=False)
    print 'Connecting to heat'
    return heatclient.client.Client(
            1,
            session.get_endpoint(
                auth=session.auth,
                service_type='orchestration',
                interface='public'),
            token=session.get_token(),
            insecure=True)

def wait_for_stack (stack, ops):
    tries = HEAT_TRIES
    stack.get()
    while tries and ops not in stack.stack_status:
        print 'wait for stack...'
        time.sleep(HEAT_DELAY)
        stack.get()
        tries -=1
    tries = HEAT_TRIES
    while tries and 'PROGRESS' in stack.stack_status:
        print stack.stack_name + ' ' + stack.stack_status
        time.sleep(HEAT_DELAY)
        stack.get()
        tries -= 1
    print stack.stack_name + ' ' + stack.stack_status
    if 'FAILED' in stack.stack_status:
        raise Exception('Heat:%s (%s)' % (stack.stack_status_reason,
                                          stack.stack_status))
    if 'COMPLETE' not in stack.stack_status:
        raise Exception('Heat:Timeout')

def delete_stack (heat, stack):
    print 'Deleting stack: ' + stack.stack_name
    stack.delete()
    wait_for_stack(stack, 'DELETE')

def delete_bgp_router (vnc, r):
    print 'Deleting ' + r.name
    vnc.bgp_router_delete(id=r.uuid)

def add_bgp_router (vnc, tc, info):
    addr_fams = AddressFamilies(BGP_ADDR_FAMILIES)
    ri = vnc.routing_instance_read(fq_name=BGP_RI)

    if (not tc.get('ext_routers')) or (len(tc['ext_routers'].keys()) == 0):
        raise Exception('No ext_routers in test_configuration')
    if not tc.get('router_asn'):
        raise Exception('No router_asn in test_configuration')

    name = tc['ext_routers'].keys()[0]
    ip = tc['ext_routers'][name]
    asn = tc['router_asn']
    print 'Adding BGP router ' + name + ':' + ip
    obj = BgpRouter(name, ri,
            bgp_router_parameters=BgpRouterParams(vendor='mx',
                autonomous_system=int(asn),
                identifier=ip,
                address=ip,
                port=179,
                address_families=addr_fams))

    bgps = [vnc.bgp_router_read(id=r['uuid']) \
            for r in vnc.bgp_routers_list()['bgp-routers']]
    for bgp in bgps:
        obj.add_bgp_router(bgp, BgpPeeringAttributes(
                session=[BgpSession(
                    attributes=[BgpSessionAttributes(
                        address_families=addr_fams)])]))

    uuid = vnc.bgp_router_create(obj)
    obj = vnc.bgp_router_read(id=uuid)
    push_cleanup(delete_bgp_router, vnc, obj)

def setup_common_stack (heat, tc, info):
    '''
    this routine creates all the resources shared
    across the k8 clusters: image, flavor, public VN, FIP-pool
    '''
    tmpl = yaml.load(open(CMN_TMPL, 'r'))
    env = yaml.load(open(CMN_ENV, 'r'))
    params = env['parameters']
    k8s_nested = tc['k8s_nested'] or {}

    print 'Creating common resources'
    flr = k8s_nested.get('flavor')
    if flr:
        if flr.get('name'):
            params['flavor_name'] = flr['name']
        if flr.get('ram'):
            params['flavor_ram'] = flr['ram']
        if flr.get('vcpus'):
            params['flavor_vcpus'] = flr['vcpus']
        if flr.get('disk'):
            params['flavor_disk'] = flr['disk']

    img = k8s_nested.get('image')
    if img:
        if img.get('name'):
            params['image_name'] = img['name']
        if img.get('container'):
            params['image_container'] = img['container']
        if img.get('disk'):
            params['image_disk'] = img['disk']
        if img.get('location'):
            params['image_location'] = img['location']

    if not tc.get('public_virtual_network'):
        raise Exception('No public_virtual_network in test_configuration')
    if not tc.get('public_rt'):
        raise Exception('No public_rt in test_configuration')
    if not tc.get('router_asn'):
        raise Exception('No router_asn in test_configuration')
    if not tc.get('public_subnet'):
        raise Exception('No public_subnet in test_configuration')
    params['publicvn_name'] = tc['public_virtual_network']
    params['ipam_name'] = params['publicvn_name'] + 'ipam'
    params['fip_pool_name'] = params['publicvn_name'] + 'pool'
    params['publicvn_rt'] = tc['public_rt']
    params['publicvn_asn'] = tc['router_asn']
    (params['publicvn_prefix'],
        params['publicvn_prefix_len']) = tc['public_subnet'].split('/')
    if tc.get('fip_pool_name'):
        params['fip_pool_name'] = tc['fip_pool_name']

    ret = heat.stacks.create(stack_name='cmn', template=tmpl,
                             environment=env)
    st = heat.stacks.get(ret['stack']['id'])
    push_cleanup(delete_stack, heat, st)
    wait_for_stack(st, 'CREATE')
    for out in st.outputs:
        info[out['output_key']] = out['output_value']

def setup_project_stack (heat, vnc, cluster, info):
    tmpl = yaml.load(open(PRJ_TMPL, 'r'))
    env = yaml.load(open(PRJ_ENV, 'r'))

    #1. create projects per cluster
    name = cluster['name']
    env['parameters']['name'] = name
    print 'Creating project ' + name
    ret = heat.stacks.create(stack_name=name, template=tmpl,
                             environment=env)
    st = heat.stacks.get(ret['stack']['id'])
    push_cleanup(delete_stack, heat, st)
    wait_for_stack(st, 'CREATE')

    # 2. adds public FIP-pool to the project
    project_id = str(uuid.UUID(st.outputs[0]['output_value']))
    prj = vnc.project_read(id=project_id)
    prj.add_floating_ip_pool(
        vnc.floating_ip_pool_read(id=info['fippool']))
    vnc.project_update(prj)
    push_cleanup(delete_fip_pool_from_project, vnc, project_id,
                 info['fippool'])

    # 3. modifies default SG to allow all traffic
    secgrp = prj.get_security_groups()[0]['uuid']
    obj = vnc.security_group_read(id=secgrp)
    obj1 = obj.get_security_group_entries()
    for i in range(len(obj1.policy_rule)):
        obj1.policy_rule[i].src_addresses[0].security_group=u'local'
    obj.set_security_group_entries(obj1)
    vnc.security_group_update(obj)
    info['clusters'].update({name: {'project': project_id,
                                    'secgrp': secgrp}})

def delete_fip_pool_from_project (vnc, project, pool):
    prj = vnc.project_read(id=project)
    fip = vnc.floating_ip_pool_read(id=pool)
    print 'Deleting ' + fip.name + ' from ' + prj.name
    prj.del_floating_ip_pool(fip)
    vnc.project_update(prj)

def setup_cluster_stack (cfg, info, tc, cred):
    '''
    this routine creates the following resources per cluster
    1. k8 cluster VN
    2. master-VM:1, slave-VM:2
    3. assigns FIP to master-VM
    '''
    juju_deployment = False
    heat = get_heat_handle(cred, project=cfg['name'])
    if tc['k8s_nested'].get('deployer') == 'juju':
        juju_deployment = True
        tmpl = yaml.load(open(JUJU_CLS_TMPL, 'r'))
        env = yaml.load(open(JUJU_CLS_ENV, 'r'))
    else:
        tmpl = yaml.load(open(CLS_TMPL, 'r'))
        env = yaml.load(open(CLS_ENV, 'r'))
    params = env['parameters']
    outs = tmpl['outputs']
    prj = info['clusters'][cfg['name']]
    net = cfg.get('network')

    params['flavor'] = info['flavor']
    params['image'] = info['image']
    params['publicvn'] = info['publicvn']
    params['fippool'] = info['fippool']
    params['project'] = prj['project']
    params['secgrp'] = prj['secgrp']

    if net:
        if net.get('name'):
            params['net_name'] = net['name']
            params['ipam_name'] = net['name'] + 'ipam'
            outs['master_ip']['value']['get_attr'][2] = net['name']
            if juju_deployment:
                outs['juju_client_ip']['value']['get_attr'][2] = net['name']
        if net.has_key('fabric_snat'):
            params['fabric_snat'] = net['fabric_snat']
        if net.get('prefix'):
            (params['net_prefix'],
             params['net_prefix_len']) = net['prefix'].split('/')
    prj['cluster_network'] = params['net_name']
    if juju_deployment:
        if cfg.get('juju_client'):
            params['juju_client_name'] = cfg['juju_client']
            params['juju_client_intf'] = cfg['juju_client'] + 'intf'
        if cfg.get('controller'):
            params['controller_name'] = cfg['controller']
    if cfg.get('master'):
        params['master_name'] = cfg['master']
        params['master_intf'] = cfg['master'] + 'intf'
    if cfg.get('slave1'):
        params['slave1_name'] = cfg['slave1']
    if cfg.get('slave2'):
        params['slave2_name'] = cfg['slave2']

    stack_name = cfg['name'] + 'r'
    print "Creating cluster resources with stack " + stack_name
    ret = heat.stacks.create(stack_name=stack_name,
                             template=tmpl, environment=env)
    st = heat.stacks.get(ret['stack']['id'])
    push_cleanup(delete_stack, heat, st)
    wait_for_stack(st, 'CREATE')
    for out in st.outputs:
        prj[out['output_key']] = out['output_value']

def generate_and_copy_files (cluster, info, desc, cred):
    '''
    this routine generates the following files
    instances.yml - for provisioning k8 cluster using contrail-ansible
    contrail.yml - template for install contrail-kube-manager
    '''
    args = {}
    provider = desc['provider_config']['bms']
    if desc.get('global_configuration'):
        registry = desc['global_configuration']['CONTAINER_REGISTRY']
        insecure = desc['global_configuration']['REGISTRY_PRIVATE_INSECURE']
    elif desc.get('CONTAINER_REGISTRY'):
        registry = desc['CONTAINER_REGISTRY']
        insecure = desc['REGISTRY_PRIVATE_INSECURE']
    elif desc['contrail_configuration'].get('CONTAINER_REGISTRY'):
        registry = desc['contrail_configuration']['CONTAINER_REGISTRY']
        insecure = desc['contrail_configuration']['REGISTRY_PRIVATE_INSECURE']
    else:
        raise Exception('Note specified CONTRAIL_REGISTRY and ' + \
                        'REGISTRY_PRIVATE_INSECURE')
    cls = info['clusters'][cluster['name']]
    args['registry'] = registry
    args['registry_insecure'] = insecure
    args['bms_pwd'] = provider['ssh_pwd']
    args['bms_usr'] = provider['ssh_user']
    args['ntp'] = provider['ntpserver']
    args['master_ip'] = cls['master_ip']
    args['slave1_ip'] = cls['slave1_ip']
    args['slave2_ip'] = cls['slave2_ip']
    args['master_name'] = cluster['master']
    args['slave1_name'] = cluster['slave1']
    args['slave2_name'] = cluster['slave2']
    outfile = cluster['name'] + '_instances.yaml'
    print "Generating " + outfile
    with open(outfile, 'w') as fd:
        fd.write(templates.k8s.substitute(args))

    cfg_nodes = []
    ctrl_nodes = []
    cfgdb_nodes = []
    for (_, ins) in desc['instances'].items():
        if 'config' in ins['roles']:
            cfg_nodes.append(ins['ip'])
        if 'control' in ins['roles']:
            ctrl_nodes.append(ins['ip'])
        if 'config_database' in ins['roles']:
            cfgdb_nodes.append(ins['ip'])

    cluster_network = { 'domain': cls['network'][0],
                        'project': cls['network'][1],
                        'name': cls['network'][2] }
    cfg = desc['contrail_configuration']
    test = desc['test_configuration']
    if test.get('config_api_ip'):
        api_vip = test['config_api_ip']
    elif cfg.get('CONFIG_API_VIP'):
        api_vip = cfg['CONFIG_API_VIP']
    else:
        raise Exception('specify CONTRAIL_API_VIP')
    args = {}
    args['kubemgr_image'] = '%s/%s:%s' % (
                    cfg['CONTAINER_REGISTRY'],
                    'contrail-kubernetes-kube-manager',
                    cfg['CONTRAIL_VERSION'])
    args['cni_init_image'] = '%s/%s:%s' % (
                    cfg['CONTAINER_REGISTRY'],
                    'contrail-kubernetes-cni-init',
                    cfg['CONTRAIL_VERSION'])
    args['master_ip'] = cls['master_ip']
    args['auth_host'] = cfg['KEYSTONE_AUTH_HOST']
    args['auth_tenant'] = cred['tenant']
    args['auth_user'] = cred['user']
    args['auth_pwd'] = cred['passwd']
    args['ks_port'] = 35357
    args['ks_ver'] = cfg['KEYSTONE_AUTH_URL_VERSION']
    args['ctrl_nodes'] = ','.join(ctrl_nodes)
    args['cfg_nodes'] = ','.join(cfg_nodes)
    args['cfg_vip'] = api_vip
    args['rabbitmq_nodes'] = ','.join(cfgdb_nodes)
    args['rabbitmq_port'] = cfg['RABBITMQ_NODE_PORT']
    args['zk_nodes'] = ','.join(cfgdb_nodes)
    args['cluster_network'] = cluster_network
    args['cluster_project'] = {'domain': 'default-domain',
                               'project': cluster['name']}
    args['cluster_name'] = cluster['name']
    args['pod_subnet'] = cluster.get('pod_subnet', '10.32.0.0/12')
    args['fabric_subnet'] = cluster.get('fabric_subnet', '10.64.0.0/12')
    args['service_subnet'] = cluster.get('service_subnet', '10.96.0.0/12')
    args['fabric_fwd'] = cluster.get('fabric_fwd', "false")
    args['fabric_snat'] = cluster.get('fabric_snat', "false")
    args['fip_pool'] = cluster.get('fip_pool', "{}")
    args['vrouter_vip'] = info['vrouter_vip']
    outfile = cluster['name'] + '_contrail.yaml'
    print "Generating " + outfile
    with open(outfile, 'w') as fd:
        fd.write(templates.contrail.substitute(args))

    copy_files_to_master_vm(provider, cls,
        ((cluster['name'] + '_instances.yaml', 'instances.yaml'),
         (cluster['name'] + '_contrail.yaml', 'contrail.yaml')))

def copy_files_to_master_vm (provider, cls, files):
    host = provider['ssh_user'] + '@' + cls['master_ssh']
    print 'trying to connect to ' + host
    retries = 10
    delay = 60
    while retries:
        try:
            with Connection(host=host, connect_kwargs={'password':
                                       provider['ssh_pwd']}) as C:
                for src, dst in files:
                    C.put(src, dst)
        except Exception as e:
            print 'Failed: ' + str(e)
            retries -= 1
            print 'delay %d, retries %d' % (delay, retries)
            time.sleep(delay)
        else:
            print 'files copied to master vm'
            break

def copy_bundle_to_juju_client(tb, cluster, info, file = 'bundle_nested.yaml'):
    provider = tb['provider_config']['bms']
    cls = info['clusters'][cluster['name']]
    host = provider['ssh_user'] + '@' + cls['juju_client_ssh']
    print 'trying to connect to ' + host
    retries = 10
    delay = 60
    while retries:
        try:
            with Connection(host=host, connect_kwargs={'password':
                                       provider['ssh_pwd']}) as C:
                C.put(file, file)
        except Exception as e:
            print 'Failed: ' + str(e)
            retries -= 1
            print 'delay %d, retries %d' % (delay, retries)
            time.sleep(delay)
        else:
            print 'files copied to master vm'
            break

def prov_k8s_contrail_in_vm (cluster, info, tb):
    '''
    this routine provisions the k8s cluster
    '''
    repo = 'http://github.com/Juniper/contrail-ansible-deployer'
    provider = tb['provider_config']['bms']
    cls = info['clusters'][cluster['name']]
    with Connection(host=provider['ssh_user'] + '@' + cls['master_ssh'],
                    connect_kwargs={'password':provider['ssh_pwd']}) as C:
        C.run('yum install -y python-pip')
        C.run('git clone -b %s --single-branch %s' % (
             os.getenv('BRANCH', 'master'), repo))
        C.run('cp instances.yaml ~/contrail-ansible-deployer/config/')
        with C.cd('contrail-ansible-deployer'):
            C.run('ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/configure_instances.yml')
            C.run('ansible-playbook -i inventory/ playbooks/install_k8s.yml')
        print 'sleep 60'
        time.sleep(60)
        C.run('kubectl apply -f contrail.yaml')
        print 'sleep 30'
        time.sleep(300)
        C.run('kubectl get pods --all-namespaces -o wide')
        C.run('kubectl get nodes')

def prov_k8s_contrail_from_juju_client(cluster, info, tb):
    provider = tb['provider_config']['bms']
    cls = info['clusters'][cluster['name']]
    with Connection(host=provider['ssh_user'] + '@' + cls['juju_client_ssh'],
                    connect_kwargs={'password':provider['ssh_pwd']}) as C:
        C.run('apt-get update')
        C.run('sudo apt install snapd')
        C.run('sudo snap install juju --classic')
        C.run('juju add-cloud ')
        C.run('juju bootstrap mymanual manual-controller')
        C.run('juju add-machine ssh:root@'+cls['master_ip'])
        C.run('juju add-machine ssh:root@'+cls['slave1'])
        C.run('juju add-machine ssh:root@'+cls['slave2'])
        C.run('juju deploy bundle_nested.yaml --map-machines=existing')

def generate_test_input (tb, clusters, info):
    tb['deployment']['slave_orchestrator'] = 'kubernetes'
    for cls in clusters:
        cls_info = info['clusters'][cls['name']]
        cls['master_ip'] = str(cls_info['master_ip'])
        cls['slave1_ip'] = str(cls_info['slave1_ip'])
        cls['slave2_ip'] = str(cls_info['slave2_ip'])
        tb['instances'].update({cls['master']:{
                                   'provider': 'bms',
                                   'ip': str(cls_info['master_ssh']),
                                   'roles': {
                                      'k8s_master': None,
                                      'kubemanager': None
                                   }}})
    k8s_nested = tb['test_configuration']['k8s_nested'] or {}
    if not k8s_nested.get('clusters'):
        name = info['clusters'].keys()[0]
        cls_info = info['clusters'][name]
        clusters[0]['master_ip'] = str(cls_info['master_ip'])
        clusters[0]['slave1_ip'] = str(cls_info['slave1_ip'])
        clusters[0]['slave2_ip'] = str(cls_info['slave2_ip'])
        tb['test_configuration']['k8s_nested'] = {'clusters': clusters}
    yaml.dump(tb, open('contrail_test_input.yaml', 'w'),
              default_flow_style=False)
