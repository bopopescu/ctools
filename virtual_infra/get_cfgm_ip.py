import yaml
import argparse
import sys
import os

def parse_cli(args):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input-file', required=True, metavar="FILE",
                        help='location of the all.yml file')
    pargs = parser.parse_args(args)
    return pargs

def read_yaml(filename):
    with open(filename, 'r') as fd:
        yargs = yaml.load(fd)
    return yargs

if __name__ == '__main__':
    pargs = parse_cli(sys.argv[1:])
    tcontent = read_yaml(pargs.input_file)
    for name, instance in tcontent['instances'].iteritems():
        if 'config' in instance['roles']:
            print instance.get('fip') or instance.get('ip')
            break
