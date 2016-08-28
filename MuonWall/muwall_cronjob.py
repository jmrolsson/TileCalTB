#! /usr/bin/env python
import os
import time
import datetime
from os import system,popen

with open("logBook.txt") as f:
  for sLine in f:
    pass
arr=sLine.split()

with open("logBookMuonWall.txt") as f:
  for sLine in f:
    pass
arr1=sLine.split()

output = popen('ps axuw | grep muon_wall_controller.py | grep -v grep | wc -l').read()
if int(output)>0:
  print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),arr[3]," Another muon_wall_controller.py is running, exiting"

elif arr[3]!=arr1[3]:

  print "++++++++++++++++++++++++++"
  print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),"From",arr1[3],"to",arr[3]
  os.system("echo /home/table/TileMoveTable/muon_wall_controller.py "+arr[3])
  print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),arr[3]," Done"
  print "--------------------------"
  print
  print

else:

  print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),arr[3]," Nothing to do"
