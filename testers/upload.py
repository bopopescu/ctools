import sys
import os
import argparse
import ConfigParser
import re
from fabric.api import env, run , local,cd
from fabric.operations import get, put
from fabric.contrib.files import exists,append
from fabric.context_managers import settings, hide

def parse_pkg(pkg):
    splitted = pkg.split('/')
    branch = splitted[2]
    try:
        p = re.compile('packages-(.*)~')
        m = p.search(pkg)
        build = m.group(1)
        return (branch,build)
    except Exception as e:
        p = re.compile('packages_(.*)~')
        m = p.search(pkg)
        build = m.group(1)
        return (branch,build)
        

def upload(directory,file_name,path,ip,user,password):
    fname = file_name
    path = '%s/%s/%s'%(path,directory[0],directory[1])
    web_server = ip
    web_server_username = user
    web_server_password = password
    try:
        build_url = os.environ.get('BUILD_URL')
    except Exception as e:
        print 'build url not found'
    try:
        with hide('everything'):
            with settings(host_string=web_server,
                          user=web_server_username,
                          password=web_server_password,
                          warn_only=True, abort_on_prompts=False):
                if not exists(path):
                    run('mkdir -p %s' % (path))
                with cd (path):
                    run('touch %s'%(fname))
                    try: 
                        append(fname,build_url)
                    except Exception as e:
                        append(fname,'FAILED')
                        
    except Exception as e:
        pass
        
def _parse_args( args_str):
    '''
    Eg. python upload.py 
                                    --web_server_ip 127.0.0.1
                                    --web_server_user bhushana
                                    --web_server_password c0ntrail!23
                                    --web_server_path <Path> 
    '''

    # Source any specified config/ini file
    # Turn off help, so we print all options in response to -h
    conf_parser = argparse.ArgumentParser(add_help=False)

    conf_parser.add_argument("-c", "--conf_file",
                             help="Specify config file", metavar="FILE")
    args, remaining_argv = conf_parser.parse_known_args(args_str.split())

    defaults = {
        'web_server_ip': '10.204.216.50',
        'web_server_user': 'bhushana',
        'web_server_password': 'c0ntrail!23',
        'web_server_path': '/home/bhushana/Documents/technical/sanity/daily',
    }

    if args.conf_file:
        config = ConfigParser.SafeConfigParser()
        config.read([args.conf_file])
        defaults.update(dict(config.items("DEFAULTS")))

    # Override with CLI options
    # Don't surpress add_help here so it will handle -h
    parser = argparse.ArgumentParser(
        # Inherit options from config_parser
        parents=[conf_parser],
        # print script description with -h/--help
        description=__doc__,
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.set_defaults(**defaults)

    parser.add_argument(
        "--web_server_ip", help="web server ip")
    parser.add_argument(
        "--web_server_user", help="web server user")
    parser.add_argument("--web_server_password", help="web server password")
    parser.add_argument(
        "--web_server_path", 
        help="Web server path")
    parser.add_argument(
        "--pkg_name", required=True,help="Package name")
    parser.add_argument(
        "--jenkins_id",required=True, help="Jenkins id")

    return parser.parse_args(remaining_argv)

# end _parse_args

def main(args_str = None ):
    if not args_str:
        args_str = ' '.join(sys.argv[1:])
    _args = _parse_args(args_str)

    try:
        directory = parse_pkg(_args.pkg_name)
        upload(directory,_args.jenkins_id,_args.web_server_path,
                _args.web_server_ip,_args.web_server_user,
                _args.web_server_password)
    except Exception as e:
        print 'Exception :%s'%e 

if __name__ == "__main__":
    main()
