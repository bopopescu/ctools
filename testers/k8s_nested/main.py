#!/usr/bin/env python
#
# Script to provision kubernetes nested cluster on Openstack
# See testbed-sample.yml for example input file
#

import os
import sys
import platform
import yaml
import templates

def setup_pip_pkgs ():
    print 'Installing platform independent packages'
    if os.system('pip install fabric'):
        raise Exception('fabric install failed')
    os.system('rm -rf /usr/lib/python2.7/site-packages/ipaddress*')
    if os.system('pip install python-openstackclient python-heatclient'):
        raise Exception('openstack client installation failed')

def setup_centos ():
    print 'Installing platform [centos] packages'
    buildid = os.getenv('BUILDID')
    branch = os.getenv('BRANCH')
    release = branch if branch == 'master' else branch[1:]
    content = templates.yum_repo.substitute(
                os='centos',
                buildid=buildid,
                branch=branch,
                release=release)
    with open('/etc/yum.repos.d/Contrail.repo', 'w') as fd:
        fd.write(content)
    os.system('yum repolist')
    os.system('rm -rf /usr/lib64/python2.7/site-packages/pycrypto*')
    if os.system('yum install -y python-contrail'):
        raise Exception('python-contrail installation failed')
    print 'Package installation successful'

platform_setup_fns = {
    'CentOS': setup_centos,
}

def main (args):
    if len(args) != 2:
        print 'Usage: %s testbed.yml' % args[0]
        return 1

    tb = yaml.load(open(args[1], 'r'))
    tc = tb.get('test_configuration')
    if not tc:
        print 'Nothing to do, test_configuration absent'
        return 0
    if not tc.has_key('k8s_nested'):
        print 'Nothing to do, not a kubernetes-nested setup'
        return 0

    setup_pip_pkgs()
    if 'linux' not in sys.platform:
        print 'Unsupported OS: ' + sys.platform
        return 2
    target = platform.linux_distribution()[0]
    for distro, platform_fn in platform_setup_fns.items():
        if distro in target:
            try:
                platform_fn()
                break
            except Exception as e:
                print 'Failed in pre-provision: ' + str(e)
                return 3
    else:
        print 'Unsupported Linux Distro: ' + target
        return 2

    # TODO: check if these params should be cli options or
    #       can be obtained from testbed.yml
    cred = {
        'user': os.getenv('OS_USERNAME', 'admin'),
        'passwd': os.getenv('OS_PASSWORD', 'contrail123'),
        'tenant': os.getenv('OS_TENANT_NAME', 'admin'),
        'project': os.getenv('OS_PROJECT_NAME', 'admin'),
        'user-domain': os.getenv('OS_USER_DOMAIN_NAME', 'default'),
        'project-domain': os.getenv('OS_PROJECT_DOMAIN_NAME', 'default'),
        'auth-url': os.getenv('OS_AUTH_URL')
    }

    import prov
    prov_info = { 'clusters': {} }
    k8s_nested = tc['k8s_nested'] or {}
    try:
        vnc = prov.get_vnc_handle(tb, cred)
        heat = prov.get_heat_handle(cred)
        prov.add_linklocal_service(vnc,
                    k8s_nested.get('linklocal_serviecs'),
                    prov_info)
        prov.add_port_translation_pool(vnc,
                    k8s_nested.get('port_translation_pools'))
        prov.add_bgp_router(vnc, tc, prov_info)
        prov.setup_common_stack(heat, tc, prov_info)
        clusters = k8s_nested.get('clusters') or prov.DFLT_CLUSTERS
        #TODO: parallelize
        for cluster in clusters:
            prov.setup_project_stack(heat, vnc, cluster, prov_info)
            prov.setup_cluster_stack(cluster, prov_info, tc, cred)
            if k8s_nested.get('deployer') == 'juju':
                prov.copy_bundle_to_juju_client(tb, cluster,prov_info)
                prov.prov_k8s_contrail_from_juju_client(cluster, prov_info, tb)
            else:
                prov.generate_and_copy_files(cluster, prov_info, tb, cred)
                prov.prov_k8s_contrail_in_vm(cluster, prov_info, tb)
        prov.generate_test_input(tb, clusters, prov_info)
    except Exception as e:
        print 'Failed:' + str(e)
        if int(os.getenv('K8_NESTED_CLEANUP_ON_FAIL', '1')):
            prov.run_cleanup()
        return 255
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
