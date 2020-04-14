#!/usr/bin/env python
#
#################################################################################
#                                                                               #
#                      20th Sept 2016                                           #
#                      juniperopenstack_bugs.py.py                              #
#                                                                               #
#       This script is used to get the list of bugs in contrail                 #
#                                                                               #
#       Usage: ./juniperopenstack_bugs.py         		                          #
#                                                                               #
#                                                                               #
#################################################################################

from launchpadlib import launchpad
from launchpadlib import uris
import sys
import os

BASE_DIR = '/home/vmahuli/lp'
GERRIT_CACHE_DIR = os.path.expanduser(
        os.environ.get('GERRIT_CACHE_DIR',
                   '~/.launchpadlib/cache'))
GERRIT_CREDENTIALS = os.path.expanduser(
        os.environ.get('GERRIT_CREDENTIALS',
                   '~/.launchpadlib/creds'))
lp = launchpad.Launchpad.login_with('Gerrit User Sync', uris.LPNET_SERVICE_ROOT, GERRIT_CACHE_DIR,credentials_file=GERRIT_CREDENTIALS, version='devel')

trunk = lp.projects['juniperopenstack']
r31 = lp.projects['juniperopenstack/r3.1']
r302x = lp.projects['juniperopenstack/r3.0.2.x']
r30 = lp.projects['juniperopenstack/r3.0']
r222x = lp.projects['juniperopenstack/r2.22.x']
r221x = lp.projects['juniperopenstack/r2.21.x']
r220x = lp.projects['juniperopenstack/r2.20.x']
r220 = lp.projects['juniperopenstack/r2.20']
r21 = lp.projects['juniperopenstack/r2.1']
r20 = lp.projects['juniperopenstack/r2.0']
r130 = lp.projects['juniperopenstack/r1.30']
r11 = lp.projects['juniperopenstack/r1.1']
r106 = lp.projects['juniperopenstack/r1.06']
r105 = lp.projects['juniperopenstack/r1.05']

releases = [ 'trunk', 'r31', 'r302x', 'r30', 'r222x', 'r221x', 'r220x', 'r220', 'r21', 'r20', 'r130', 'r11', 'r106', 'r105' ]

#Loop out with all the bugs in juniperopenstack
for release in releases:
    rel = eval(release)
    bug_tasks = rel.searchTasks(tags=[])
    for task in bug_tasks:
        milestone = None
        date_fix_committed = None
        if task.milestone:
            milestone = task.milestone.name
        if task.date_fix_committed:
            date_fix_committed = str(task.date_fix_committed.date().year) + '-' + str(task.date_fix_committed.date().month) + '-' + str(task.date_fix_committed.date().day)
        if task.bug_target_name == 'juniperopenstack':
            series = task.bug_target_name.replace('juniperopenstack', 'trunk')
        else:
            series = task.bug_target_name.lstrip('juniperopenstack')
            series = series.lstrip('/')
        #Check if the bug has official tag

        if release == "trunk":
            bug_string = '%s| %s-%s-%s| %s| %s| %s| %s ' % ( task.bug.id, task.date_created.date().year, task.date_created.date().month, task.date_created.date().day, series , task.status, date_fix_committed, milestone )
        else:
            date_created = 'None'
            bug_string = '%s| %s| %s| %s| %s| %s ' % ( task.bug.id, date_created, series, task.status, date_fix_committed, milestone )
        print bug_string.encode('utf-8')
