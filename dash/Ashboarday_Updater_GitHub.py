#-------------------------------------------------------
#
# Ashboarday GitHub Updater
# 
# Place in repository and run directly or set Action to run periodically.
# Takes direction from local json file "ashboaday.u.json" to read each listed folder
# and send the latest date to the dashboard's API to update its data.
#
# Jerry Auld, Otago Computing, 2021-06-01
#
#-------------------------------------------------------

import pathlib
import os
from datetime import datetime
import json
import urllib.request

#---------------  FUNCTIONS  ---------------------------

def getLatestDate(folder):
  # returns the latest date found in the folder's files as an ISO date string.
  latedate = datetime.now()
  fcount = 0
  fsize = 0
  files = [ file.path for file in os.scandir(folder) if not file.is_dir() ]
  for f in files:
    fcount += 1
    # thisdate = os.path.getmtime(f)
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(f)
    thisdate = datetime.fromtimestamp(mtime)
    fsize += size
    if thisdate < latedate:
      latedate = thisdate
      
  if fcount == 0:
    return "2009-01-01", fcount, fsize
  else:
    return latedate.strftime("%Y-%m-%d"), fcount, fsize

#-----------------  MAIN   -----------------------------


print("Python :: Running the Ashboarday Updater.")

# Get our guidance file:
print(os.getcwd())
if os.path.exists('.dash/ashboarday.u.json'):
  
  with open('.dash/ashboarday.u.json') as f:
    jsondata = json.load(f)

  dashapi = jsondata['Target']
  nodes = jsondata['Nodes']
  
  for node in nodes:
    result = getLatestDate(node['Scrape'])
    print("For Node "+node['NID']+" :: Latest date: "+result[0]+". File count: "+str(result[1])+". Folder size: "+str(result[2]))
    dashreply = urllib.request.urlopen(dashapi+"?i=" + node["NID"] + "&t=" + result[0] + "&s=" + str(result[2]) + "&f=" + str(result[1])).read()
    print("Dashboard response: "+str(dashreply,'utf-8'))
  
  f.close
else:
  print("ERROR: json guidance file is not found. Please place in the same folder as this script.")

# All subdirectories in the current directory, not recursive.
# [f for f in p.iterdir() if f.is_dir()]

# subfolders = [ f.path for f in os.scandir('./') if f.is_dir() ]
# print(subfolders)

#-------------------------------------------------------