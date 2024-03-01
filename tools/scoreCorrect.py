import random
import requests
import json
import os
import sys

import jsonpack

### MAKE SURE TO MAKE A BACKUP OF SCOUTED MATCHES!

# Move this script into the root dir, then grab an event code from TBA and run 'python3 ./fakescout.py [event code]'

eventCode = "2024flwp"

TBAip = "https://www.thebluealliance.com/api/v3"
headers = {"User-Agent": "Mozilla/5.0", "X-TBA-Auth-Key": "fzQY0pv6qwfwuII5Xx2bmP57BBSuE0maxKailYlrI0e1EdfKCq6F3Th9FFDqpW7f"}

matches = requests.get(TBAip+"/event/"+eventCode+"/matches", headers=headers).json()

dataroot = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/")
eventroot = dataroot+eventCode+"/"

def getSubfolders(path):
    try:
        return os.listdir(path)
    except:
        return None

matchFiles = getSubfolders(eventroot)

def openFile(path):
    if not os.path.exists(path):
        return ''
    try:
        with open(path) as f:
            return f.read()
    except:
        return ''

def writeFile(path, data):
    if not os.path.exists(path):
        with open(path, mode='a'): pass
    with open(path, 'w') as f:
        f.write(data)

def correctScore(filename, blueScore, redScore):
  if not filename in matchFiles:
    return
  data = jsonpack.unpack(openFile(eventroot+filename))
  data['redScore'] = redScore
  data['blueScore'] = blueScore
  writeFile(eventroot+filename, jsonpack.pack(data))
  
index = 1

for a in range(len(matches)):
  teamIndex = 1
  blueScore = matches[a]['alliances']['blue']['score']
  redScore = matches[a]['alliances']['red']['score']
  
  if blueScore == -1 or redScore == -1:
    continue
  
  for b in range(3):
    filename = "matchscout" + "-" + eventCode + "_qm" + str(index) + "-red-" + str(teamIndex) + ".jsonpack"
    correctScore(filename, redScore, blueScore)
    teamIndex += 1
  teamIndex = 1
  for b in range(3):
    filename = "matchscout" + "-" + eventCode + "_qm" + str(index) + "-blue-" + str(teamIndex) + ".jsonpack"
    correctScore(filename, redScore, blueScore)
    teamIndex += 1
  
  index += 1