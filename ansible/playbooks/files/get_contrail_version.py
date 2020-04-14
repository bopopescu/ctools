#!/usr/bin/python

# This script tries to replicate how the report was stored in contrail-test
# reporting structure. We may need to revisit contrail-test to store the
# report based on tags rather than version

import os
import re
import argparse
import sys

def parse_cli(args):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--output', default='/tmp/contrail_version',
                        help='output filename to store contrail version')
    return parser.parse_args(args)

pargs = parse_cli(sys.argv[1:])

config_api_container_id = None
cmd = "docker images | grep controller-config-api | awk '{print $3}'"
config_api_image_id = os.popen(cmd).read().strip()

if config_api_image_id:
    cmd = "docker ps | grep %s"%(config_api_image_id)
    config_api_container_id = os.popen(cmd).read()
    if config_api_container_id:
        config_api_container_id = config_api_container_id.split(' ')[0]

if not config_api_container_id:
    cmd = "docker images | grep controller-config-api | awk '{print $1}'"
    config_api_image_id = os.popen(cmd).read().strip()

    cmd = "docker ps | grep %s"%(config_api_image_id)
    config_api_container_id = os.popen(cmd).read()
    if config_api_container_id:
        config_api_container_id = config_api_container_id.split(' ')[0]

if not config_api_container_id:
    assert False, "Could not get contrail version"

cmd = "docker exec %s contrail-version | grep contrail-utils "%(
        config_api_container_id)
contrail_version = os.popen(cmd).read().split()[1]

version_pattern = '\s*((\d+\.)+(\d+\-)\d+)\..*'
if re.match(version_pattern, contrail_version):
    version = re.match(version_pattern, contrail_version).group(1)
    print version
    with open(pargs.output, "w") as f:
        f.write(str(version).strip())
else:
    assert False, "Could not get contrail version"
