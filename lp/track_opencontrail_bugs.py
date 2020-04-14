#!/usr/bin/env python
#
#################################################################################
#                                                                               #
#       25th August 2014                                                        #
#       track_opencontrail_bugs.py                                              #
#       Author: Vinay Mahuli                                                    #
#       This script is used to get the list of bugs without official tags       #
#                                                                               #
#       Usage: ./track_opencontrail_bugs.py		                        #
#                                                                               #
#                                                                               #
#################################################################################

from launchpadlib.launchpad import *

lp = Launchpad.login_with(
'testing', service_root='https://api.launchpad.net',
version='devel')
project = lp.projects['opencontrail']
bug_tasks = project.searchTasks(tags=[])
official_tags = project.official_bug_tags
len_off_tags = len(official_tags)
check_flag = 'true'
truth_table = list()

#Loop out with all the bugs in opencontrail
for task in bug_tasks:
    assignee = None
    owner = None
    if task.assignee:
        assignee = task.assignee.name
    if task.owner:
        owner = task.owner.name
    all_tags_in_bug = task.bug.tags
    for tag in all_tags_in_bug:
        if tag not in official_tags:
            flag = 'false'
        else:
            flag = 'true'
        truth_table.append(flag)

    #Check if the bug has official tag
    if check_flag not in truth_table:
        bug_string = '%s| %s| %s| %s| %s| %s| %s| https://bugs.launchpad.net/opencontrail/+bug/%s' % ( task.bug.id, task.bug.title, task.status, task.importance, assignee, owner, task.bug.tags, task.bug.id )
        print bug_string.encode('utf-8')
    del truth_table[:]
