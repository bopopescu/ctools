#!/usr/bin/env python
#
#################################################################################
#                                                                               #
#       25th August 2014                                                        #
#       search_bugs.py                                                          #
#       Version 1.0                                                             #
#                                                                               #
#       This script is used to get the list of bugs without official tags       #
#                                                                               #
#       Usage: ./search_bugs.py                                                 #
#                                                                               #
#                                                                               #
#################################################################################

from launchpadlib.launchpad import *
import ConfigParser
import os
import sys

lp = Launchpad.login_with( 'testing', service_root='https://api.launchpad.net', version='devel' )

print "Welcome " + lp.me.display_name
cwd = os.getcwd()

config = ConfigParser.SafeConfigParser()
config.read( cwd + '/' + 'launchpad.cfg' )

section =  'DEFAULT'

importance_cfg = config.get(section, 'importance')
if importance_cfg:
    importance_cfg = importance_cfg.split(',')
else:
    importance_cfg = []

tag_cfg = config.get(section, 'tag')
if tag_cfg:
    tag_cfg = tag_cfg.split(',')
else:
    tag_cfg = []

status_cfg = config.get(section, 'status')
if status_cfg:
    status_cfg = status_cfg.split(',')
else:
    status_cfg = []

assignee_cfg = config.get(section, 'assignee')
owner_cfg = config.get(section, 'owner')

debugFind = config.get(section, 'debug')

debugFlag = ''

if debugFind.__contains__('true'):
    debugFlag = True
if debugFind.__contains__('false'):
    debugFlag = False
    
project = lp.projects['juniperopenstack']
#project = lp.projects['juniperopenstack'].getSeries(name=series_cfg)

if debugFlag:
    print status_cfg
    print importance_cfg
    print tag_cfg
    print project

try:
    bug_tasks = project.searchTasks(status=status_cfg, tags=tag_cfg, importance=importance_cfg)
except:
    print "The specified series doesn't exist"
    sys.exit(1)
    
#Loop out with all the bugs in juniperopenstack
for task in bug_tasks:
    assignee = None
    owner = None
    milestone = None
    
    if task.assignee:
        assignee = task.assignee.name
    if task.owner:
        owner = task.owner.name
    if task.milestone:
        milestone = task.milestone.title
    if str(assignee).__contains__(assignee_cfg) and str(owner).__contains__(owner_cfg):
        bug_string = '%s| %s| %s| %s| %s| %s| %s| %s| %s| https://bugs.launchpad.net/juniperopenstack/+bug/%s' % ( task.bug.id, task.bug.title, task.status, task.importance, assignee, owner, task.bug.tags, milestone, task.bug_target_name, task.bug.id )
        print bug_string.encode('utf-8')
