#!/usr/bin/env python
import sys
import requests
from argparse import ArgumentParser
import time
import json
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def url_generate(hostname, port, host, service):
    return 'https://%s:%s/v1/actions/process-check-result?service=%s!%s' % (hostname, port, host, service)


def parse_result(result):
    return {
        'OK': 0,
        'INFO': 0,
        'WARNING': 1,
        'CRITICAL': 2,
    }.get(result, 3)


def extract_host(data):
    return data['data']['series'][0]['tags']['host']


def extract_service(data):
    return data['id']


def gen_payload(data):
    return json.dumps({
        'exit_status': parse_result(data['level']),
        'plugin_output': data['message']
    })


def modify_host(host, substr):
    return(re.sub(substr, '', host))


def main():
    argp = ArgumentParser(
        description='Sends kapacitor event to icinga2 api'
    )
    argp.add_argument('-V', '--version', action='version', version='0.2')
    argp.add_argument('-v', '--verbose',
                      action='count',
                      default=0,
                      help='increase output verbosity (use up to 3 times)')
    argp.add_argument('-H', '--host', type=str,
                      default='icinga2',
                      help='Icinga2 server IP or hostname')
    argp.add_argument('-p', '--port', type=int, default=5665,
                      help='Icinga2 api port')
    argp.add_argument('-m', '--modify', type=str, default='',
                      help='delete substring from hostname')
    argp.add_argument('-u', '--user', type=str, default='root',
                      help='icinga2 api user name')
    argp.add_argument('-P', '--password', type=str, default='icinga',
                      help='icinga2 api user password')
    try:
        args = vars(argp.parse_args())
    except SystemExit:
        sys.exit(3)
    kapacitor_data = json.loads(sys.stdin.read())
    try:
        r = requests.post(url_generate(args['host'],
                          args['port'],
                          modify_host(extract_host(kapacitor_data),
                            args['modify']),
                          extract_service(kapacitor_data)),
                          data=gen_payload(kapacitor_data),
                          auth=(args['user'], args['password']),
                          verify=False,
                          headers={'Accept': 'application/json'})
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(3)


if __name__ == '__main__':
    main()
