#!/usr/bin/python
import sys
import re
import commands

#chassis_1 = sys.argv[1] 
#chassis_2 = sys.argv[1] 

chassis_1 = [0,1,2,3]
chassis_2 = [4]

cmd = "rados bench -p volumes 30 write -t 300 --no-cleanup"
objects_list = commands.getoutput(cmd)

cmd = "rados -p volumes ls"
objects_list = commands.getoutput(cmd)

objects_list = re.findall('benchmark_data\S+',objects_list)

status = True

for object in objects_list[:5000]:

  cmd = "ceph osd map volumes %s"%object
  object_output = commands.getoutput(cmd)
  ret = re.search('\[(\d+),(\d+)]',object_output)
  group1 = ret.group(1)
  group2 = ret.group(2)

  if group1 in chassis_1 and group2 in chassis_1 :
    status = status and False
  if group1 in chassis_2 and group2 in chassis_2 :
    status = status and False
  print object,status

print "TOTAL_OBJECT:%d,TEST_STATUS:%s"%(len(objects_list),status)
