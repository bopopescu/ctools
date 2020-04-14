#!/usr/bin/env python
#
#################################################################################
#                                                                               #
#       21st November 2014                                                      #
#       add_tag.py                                                              #
#       Author: Vinay Mahuli                                                    #
#       This script is used to add tags to list of bugs without official tags   #
#                                                                               #
#       Usage: ./add_tags.py --bug_list=$PWD/bug_list.txt                       #
#                                                                               #
#################################################################################

from launchpadlib.launchpad import *
from getopt import getopt
import os
import re
import smtplib
import subprocess
import sys
import time

valid = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789- ')
def test(s):
    return set(s).issubset(valid)

def main():
    # This should be replaced with argparse instead of getopt, when
    # we upgrade the server to python 3.2 or later.
    gerrit_args = ['tag=', 'bug_list=']
    args, unused = getopt(sys.argv[1:], '', gerrit_args)

    tag = bug_list = None
    for argname, argv in args:
        if argname == '--bug_list':
            bug_list = argv

    file = open(bug_list, 'r')
    for details in file:
        for argname, argv in args:
            if argname == '--tag':
                tag = argv
        split_details = details.split()
        bug_number = split_details[0]
        bug_number = bug_number.rstrip()
        try:
            tag = split_details[1] 
            tag = tag.rstrip()
        except IndexError:
            tag = tag
            print (tag)

        if not test(tag):
            print "Supported characters in tag " + tag + " for bug number " + bug_number + " are alphanumeric characters and hyphen !!"

        if test(tag):
            lpconn = Launchpad.login_with('testing', service_root='https://api.launchpad.net', version='devel')
            print ( "Applying tag " + tag + " on " + bug_number + "...")  
            time.sleep(2)
            for task in lpconn.bugs[bug_number].bug_tasks:
                lp_bug = task.bug
                lp_bug.tags = lp_bug.tags + ["%s" % tag ]
                lp_bug.tags.append("%s" % tag)
                lp_bug.lp_save()

    return 0;

if __name__ == '__main__':
    sys.exit(main())
