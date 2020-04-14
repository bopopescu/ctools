import sys
import json
import argparse
import requests
import os
import time

GO_SERVER_PORT=9091
DEFAULT_HEADERS = {'Content-type': 'application/json; charset="UTF-8"'}

class Go(object):
    def __init__(self, address, username, password):
        self.username = username
        self.address = address
        self.password = password
        self.url = "https://%s:%s"%(self.address, GO_SERVER_PORT)
        self.headers = dict(DEFAULT_HEADERS)

    def get_auth_token(self):
        authn_body = {'auth': {'identity': {'methods': ['password'],
                      'password': {'user': {'domain': {'id': 'default'},
                      'name': self.username, 'password': self.password}}},
                      "scope": {"project": {"name": "admin",
                      "domain": {"name": "Default"}}}}}
        url = self.url + '/keystone/v3/auth/tokens'
        resp = requests.post(url, data=json.dumps(authn_body),
                             headers=DEFAULT_HEADERS, verify=False)
        if resp.status_code == 401:
            raise Exception('Unable to authenticate to %s using body %s'%(
                            url, authn_body))
        self.headers.update({'X-Auth-Token': resp.headers['X-Subject-Token']})

    def get_cluster_id(self):
        self.get_auth_token()
        url = self.url + '/contrail-clusters?detail=true'
        resp = requests.get(url, headers=self.headers, verify=False)
        resp_dict = json.loads(resp.text)
        self.cluster_id = resp_dict['contrail-clusters'][0]['contrail-cluster']['uuid']

    def wait_till_cluster_up(self):
        self.get_cluster_id()
        url = self.url + '/contrail-cluster/%s'%(self.cluster_id)
        max_retries = 160
        retries = 0
        while True:
            resp = requests.get(url, headers=self.headers, verify=False)
            if resp.status_code == 401:
                self.get_auth_token()
                continue
            resp_dict = json.loads(resp.text)
            status = resp_dict['contrail-cluster']['provisioning_state']
            if status.lower() in ['created', 'updated']:
                print 'Cluster is Up'
                break
            if 'create_failed' == status.lower():
                print 'Provision failed'
                raise Exception('Provision failed')
            if retries == max_retries:
                raise Exception('Cluster not up after %d mins' % max_retries)
            retries +=1
            time.sleep(60)

def parse_cli(args):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-u', '--username', required=True,
                        help='admin username of command deployer')
    parser.add_argument('-p', '--password', required=True,
                        help='admin password of command deployer')
    parser.add_argument('-a', '--address', required=True,
                        help='address of the command deployer')
    pargs = parser.parse_args(args)
    return pargs

if __name__ == '__main__':
    pargs = parse_cli(sys.argv[1:])
    obj = Go(pargs.address, pargs.username, pargs.password)
    obj.wait_till_cluster_up()
