#!/usr/bin/env python
#
#################################################################################
#                                                                               #
#       26th July 2016                                                          #
#       update_bug_status_and_imp.py                                            #
#       Author: Vinay Mahuli                                                    #
#       This script is used to update bug status and importance immediately     #
#       after we cut a new branch and move all the open bugs for a particular   #
#       milestone on say mainline to the new branch                             #
#                                                                               #
#       Usage: ./update_bug_status_and_imp.py                                   #
#                                                                               #
#################################################################################

from getopt import getopt
import os
import re
import smtplib
import subprocess
import sys
import time
from launchpadlib import launchpad
from launchpadlib import uris

from xml.dom.minidom import Document
import xmlrpclib
import smtplib
from email.message import Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

getBranch = { 'Juniper Openstack r1.06':'R1.06',
              'Juniper Openstack r1.05':'R1.05',
              'Juniper Openstack r1.04':'R1.04',
              'Juniper Openstack r1.1':'R1.10',
              'Juniper Openstack r1.30':'R1.30',
              'Juniper Openstack r2.0':'R2.0',
              'Juniper Openstack r2.1':'R2.1',
              'Juniper Openstack r2.20':'R2.20',
              'Juniper Openstack r2.20.x':'R2.20.x',
              'Juniper Openstack r2.21.x':'R2.21.x',
              'Juniper Openstack r2.22.x':'R2.22.x',
              'Juniper Openstack r3.0':'R3.0',
              'Juniper Openstack r3.1':'R3.1',
              'Juniper Openstack r3.0.2.x':'R3.0.2.x',
              'Juniper Openstack trunk':'main',
              'Juniper Openstack':'main',
              'OpenContrail':'main',
              'OpenContrail trunk':'main'
            }

getSeries = { 'R1.06':'juniperopenstack/r1.06',
              'R1.05':'juniperopenstack/r1.05',
              'R1.04':'juniperopenstack/r1.04',
              'R1.10':'juniperopenstack/r1.1',
              'R1.30':'juniperopenstack/r1.30',
              'R2.0':'juniperopenstack/r2.0',
              'R2.1':'juniperopenstack/r2.1',
              'R2.20':'juniperopenstack/r2.20',
              'R2.22-dev':'juniperopenstack/r2.20',
              'R2.20.x':'juniperopenstack/r2.20.x',
              'R2.21.x':'juniperopenstack/r2.21.x',
              'R2.22.x':'juniperopenstack/r2.22.x',
              'R3.0':'juniperopenstack/r3.0',
              'R3.1':'juniperopenstack/r3.1',
              'R3.0.2.x':'juniperopenstack/r3.0.2.x',
              'main':'juniperopenstack/trunk'
            }

gerrit_args = ['bug_list=']
args, unused = getopt(sys.argv[1:], '', gerrit_args)

bug_list = status = assignee = None
for argname, argv in args:
    if argname == '--bug_list':
        bug_list = argv

BASE_DIR = '/home/vmahuli/lp'
GERRIT_CACHE_DIR = os.path.expanduser(
         os.environ.get('GERRIT_CACHE_DIR',
                    '~/.launchpadlib/cache'))
GERRIT_CREDENTIALS = os.path.expanduser(
         os.environ.get('GERRIT_CREDENTIALS',
                    '~/.launchpadlib/creds'))
lpconn = launchpad.Launchpad.login_with('Gerrit User Sync', uris.LPNET_SERVICE_ROOT, GERRIT_CACHE_DIR,credentials_file=GERRIT_CREDENTIALS, version='devel')

file = open("bug_list", "r")
for details in file:
    split_details = details.split()
    bug_number = split_details[0]
    bug_number = bug_number.rstrip()

    print ( "Updating status and importance " + "...")
    for task in lpconn.bugs[bug_number].bug_tasks:
        if getBranch[task.bug_target_display_name] == "main":
            assigned_eng = None
            status = None
            if task.assignee:
                assigned_eng = task.assignee.name
                assignee_link = task.assignee_link
            if task.importance:
                importance = task.importance
            bug_string = '%s| %s| %s| %s' % ( task.bug.id, task.importance, assigned_eng, getBranch[task.bug_target_display_name])
            print bug_string.encode('utf-8')
        if getBranch[task.bug_target_display_name] == "R3.1":
            if assigned_eng:
                task.assignee_link = assignee_link
            task.importance = importance
            task.lp_save()
            if assigned_eng:
                bug_string = '%s| %s| %s| %s' % ( task.bug.id, task.importance, task.assignee_link, getBranch[task.bug_target_display_name])
            else:
                bug_string = '%s| %s| %s| %s' % ( task.bug.id, task.importance, assigned_eng, getBranch[task.bug_target_display_name])
            print bug_string.encode('utf-8')
