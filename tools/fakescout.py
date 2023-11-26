import random
import requests
import json
import os

import oprs
import jsonpack

eventCode = '2022code'

# Move this script into the root dir, then grab an event code from TBA and paste it to the eventCode var above

TBAip = "https://www.thebluealliance.com/api/v3"
headers = {"User-Agent": "Mozilla/5.0", "X-TBA-Auth-Key": "fzQY0pv6qwfwuII5Xx2bmP57BBSuE0maxKailYlrI0e1EdfKCq6F3Th9FFDqpW7f"}

matches = requests.get(TBAip+"/event/"+eventCode+"/matches", headers=headers).json()

dataroot = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/")
eventroot = dataroot+eventCode+"/"

def makeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def writeFile(path, data):
    if not os.path.exists(path):
        with open(path, mode='a'): pass
    with open(path, 'w') as f:
        f.write(data)

def getOPR(key):
    for opr in oprs:
        if opr['key'] == key:
            return opr['OPR']

def randPerformance(opr, minOPR, maxOPR):
    # x = uniform(minOPR, maxOPR)
    # x = (x-minOPR)/maxOPR
    # x = round((x*2)-1,0)
    return int(random.randint(-1, 1))

makeDir(dataroot)
makeDir(eventroot)

simpleMatches = []

for match in matches:
    if match['comp_level'] != 'qm': continue
    simpleMatches.append({
        'key': match['key'],
        'blue': match['alliances']['blue']['team_keys'],
        'red': match['alliances']['red']['team_keys'],
        'bluescore': match["alliances"]["blue"]["score"],
        'redscore': match["alliances"]["red"]["score"],
        'winningAlliance': match['winning_alliance']
    })

oprs = oprs.calc(simpleMatches)

minOPR = 100
maxOPR = -1

for team in oprs:
    if team['OPR'] < minOPR:
        minOPR = team['OPR']
    if team['OPR'] > maxOPR:
        maxOPR = team['OPR']
    
    data = jsonpack.pack({
        'name': 'Scouter1',
        'notes': f'Team {team["key"]} does seem to have made a robot'
    })
    filename = f'pitscout-{team["key"]}.jsonpack'
    writeFile(eventroot+filename, data)

maxOPR = maxOPR-minOPR

for match in simpleMatches:
    for i, team in enumerate(match['blue']):
        data = jsonpack.pack({
            'name': 'Scouter'+str(i+2),
            'alliance': 'blue',
            'position': i+1,
            'team': team,
            'win': match['winningAlliance'] == 'blue',
            'blueScore': match['bluescore'],
            'redScore': match['redscore'],
            'performance': randPerformance(getOPR(team), minOPR, maxOPR),
            'notes': f'Team {team} does seem to have played in this match'
        })
        filename = f'matchscout-{match["key"]}-blue-{i+1}.jsonpack'
        writeFile(eventroot+filename, data)
    for i, team in enumerate(match['red']):
        data = jsonpack.pack({
            'name': 'Scouter'+str(i+5),
            'alliance': 'red',
            'position': i+1,
            'team': team,
            'win': match['winningAlliance'] == 'red',
            'blueScore': match['bluescore'],
            'redScore': match['redscore'],
            'performance': randPerformance(getOPR(team), minOPR, maxOPR),
            'notes': f'Team {team} does seem to have played in this match'
        })
        filename = f'matchscout-{match["key"]}-red-{i+1}.jsonpack'
        writeFile(eventroot+filename, data)


