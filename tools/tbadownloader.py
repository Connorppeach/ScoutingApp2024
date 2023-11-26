import pandas as pd
import numpy as np

import csv
import requests
import json
import time

#This script downloads all the data for a year from TBA and compiles it into a csv
#Useful for regressional analysis

TBAip = "https://www.thebluealliance.com/api/v3"
authkey = "tjEKSZojAU2pgbs2mBt06SKyOakVhLutj3NwuxLTxPKQPLih11aCIwRIVFXKzY4e"

headers =  {'X-TBA-Auth-Key': authkey}

events = requests.get(TBAip+"/events/2023", headers=headers).json()

length = len(events)

with open('./TBAmatches.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    header = []
    header.append('event_key')
    header.append('match_key')
    header.append('color')
    header.append('score')
    header.append('winning_alliance')
    header.append('team1')
    header.append('team2')
    header.append('team3')

    header.append('activationBonusAchieved')
    header.append('autoBridgeState')
    header.append('autoChargeStationPoints')
    header.append('autoChargeStationRobot1')
    header.append('autoChargeStationRobot2')
    header.append('autoChargeStationRobot3')
    header.append('autoDocked')
    header.append('autoGamePieceCount')
    header.append('autoGamePiecePoints')
    header.append('autoMobilityPoints')
    header.append('autoPoints')
    header.append('coopGamePieceCount')
    header.append('coopertitionCriteriaMet')
    header.append('endGameBridgeState')
    header.append('endGameChargeStationPoints')
    header.append('endGameChargeStationRobot1')
    header.append('endGameChargeStationRobot2')
    header.append('endGameChargeStationRobot3')
    header.append('endGameParkPoints')
    header.append('foulCount')
    header.append('foulPoints')
    header.append('linkPoints')
    header.append('mobilityRobot1')
    header.append('mobilityRobot2')
    header.append('mobilityRobot3')
    header.append('rp')
    header.append('sustainabilityBonusAchieved')
    header.append('teleopGamePieceCount')
    header.append('teleopGamePiecePoints')
    header.append('teleopPoints')
    header.append('totalChargeStationPoints')
    header.append('totalPoints')

    writer.writerow(header)
    for i in range(0, length, 1):
        event = events[i]
        key = event['key']
        time.sleep(0.1)
        matches = requests.get(TBAip+f"/event/{event['key']}/matches", headers=headers).json()
        for match in matches:
            try:
                row = []
                row.append(key)
                row.append(match['key'])
                row.append('blue')
                row.append(match['alliances']['blue']['score'])
                row.append(match['winning_alliance']=='blue')
                row.append(match['alliances']['blue']['team_keys'][0])
                row.append(match['alliances']['blue']['team_keys'][1])
                row.append(match['alliances']['blue']['team_keys'][2])
                
                bluescore = match['score_breakdown']['blue']

                row.append(bluescore['activationBonusAchieved'])
                row.append(bluescore['autoBridgeState'])
                row.append(bluescore['autoChargeStationPoints'])
                row.append(bluescore['autoChargeStationRobot1'])
                row.append(bluescore['autoChargeStationRobot2'])
                row.append(bluescore['autoChargeStationRobot3'])
                row.append(bluescore['autoDocked'])
                row.append(bluescore['autoGamePieceCount'])
                row.append(bluescore['autoGamePiecePoints'])
                row.append(bluescore['autoMobilityPoints'])
                row.append(bluescore['autoPoints'])
                row.append(bluescore['coopGamePieceCount'])
                row.append(bluescore['coopertitionCriteriaMet'])
                row.append(bluescore['endGameBridgeState'])
                row.append(bluescore['endGameChargeStationPoints'])
                row.append(bluescore['endGameChargeStationRobot1'])
                row.append(bluescore['endGameChargeStationRobot2'])
                row.append(bluescore['endGameChargeStationRobot3'])
                row.append(bluescore['endGameParkPoints'])
                row.append(bluescore['foulCount'])
                row.append(bluescore['foulPoints'])
                row.append(bluescore['linkPoints'])
                row.append(bluescore['mobilityRobot1'])
                row.append(bluescore['mobilityRobot2'])
                row.append(bluescore['mobilityRobot3'])
                row.append(bluescore['rp'])
                row.append(bluescore['sustainabilityBonusAchieved'])
                row.append(bluescore['teleopGamePieceCount'])
                row.append(bluescore['teleopGamePiecePoints'])
                row.append(bluescore['teleopPoints'])
                row.append(bluescore['totalChargeStationPoints'])
                row.append(bluescore['totalPoints'])
                
                #print(row)
                writer.writerow(row)
            except:
                pass
            try:
                row = []
                row.append(key)
                row.append(match['key'])
                row.append('red')
                row.append(match['alliances']['red']['score'])
                row.append(match['winning_alliance']=='red')
                row.append(match['alliances']['red']['team_keys'][0])
                row.append(match['alliances']['red']['team_keys'][1])
                row.append(match['alliances']['red']['team_keys'][2])
                
                redscore = match['score_breakdown']['red']

                row.append(redscore['activationBonusAchieved'])
                row.append(redscore['autoBridgeState'])
                row.append(redscore['autoChargeStationPoints'])
                row.append(redscore['autoChargeStationRobot1'])
                row.append(redscore['autoChargeStationRobot2'])
                row.append(redscore['autoChargeStationRobot3'])
                row.append(redscore['autoDocked'])
                row.append(redscore['autoGamePieceCount'])
                row.append(redscore['autoGamePiecePoints'])
                row.append(redscore['autoMobilityPoints'])
                row.append(redscore['autoPoints'])
                row.append(redscore['coopGamePieceCount'])
                row.append(redscore['coopertitionCriteriaMet'])
                row.append(redscore['endGameBridgeState'])
                row.append(redscore['endGameChargeStationPoints'])
                row.append(redscore['endGameChargeStationRobot1'])
                row.append(redscore['endGameChargeStationRobot2'])
                row.append(redscore['endGameChargeStationRobot3'])
                row.append(redscore['endGameParkPoints'])
                row.append(redscore['foulCount'])
                row.append(redscore['foulPoints'])
                row.append(redscore['linkPoints'])
                row.append(redscore['mobilityRobot1'])
                row.append(redscore['mobilityRobot2'])
                row.append(redscore['mobilityRobot3'])
                row.append(redscore['rp'])
                row.append(redscore['sustainabilityBonusAchieved'])
                row.append(redscore['teleopGamePieceCount'])
                row.append(redscore['teleopGamePiecePoints'])
                row.append(redscore['teleopPoints'])
                row.append(redscore['totalChargeStationPoints'])
                row.append(redscore['totalPoints'])
                
            
                #print(row)
                writer.writerow(row)
            except:
                pass
        print(f'Downloading matchdata ({round(((i/length)*100), 3)}%)', end='\r')
print(f'Downloading matchdata (100%)    ')

tbadata = pd.read_csv(r'TBAmatches.csv')

teamdata = {'team': [],
        'matches': [],
        'points': [],
        'wins': [],
        'activationBonusAchieved': [],
        'autoBridgeLevel': [],
        'autoChargeStationPoints': [],
        'autoChargeStationRobot': [],
        'autoDocked': [],
        'autoGamePieceCount': [],
        'autoGamePiecePoints': [],
        'autoMobilityPoints': [],
        'autoPoints': [],
        'coopGamePieceCount': [],
        'coopertitionCriteriaMet': [],
        'endGameBridgeLevel': [],
        'endGameChargeStationPoints': [],
        'endGameChargeStationRobotParked': [],
        'endGameChargeStationRobotDocked': [],
        'endGameParkPoints': [],
        'foulCount': [],
        'foulPoints': [],
        'linkPoints': [],
        'mobilityRobot': [],
        'rp': [],
        'sustainabilityBonusAchieved': [],
        'teleopGamePieceCount': [],
        'teleopGamePiecePoints': [],
        'teleopPoints': [],
        'totalChargeStationPoints': []}

def findIndex(name):
    for i in range(0, len(teamdata['team'])-1, 1):
        if teamdata['team'][i] == name:
            return i
    return None

def zeroTeamData():
    keys = list(teamdata.keys())
    for key in keys:
        teamdata[key].append(0)

def removeTeam(i):
    keys = list(teamdata.keys())
    for key in keys:
        teamdata[key].pop(i)

def setTeam(i, dindex, robotnum):
    teamdata['matches'][i]                         += 1
    teamdata['points'][i]                     += tbadata['score'][dindex]
    teamdata['wins'][i]                            += bool(tbadata['winning_alliance'][dindex])
    teamdata['activationBonusAchieved'][i]         += bool(tbadata['activationBonusAchieved'][dindex])
    teamdata['autoBridgeLevel'][i]                 += bool(tbadata['autoBridgeState'][dindex]=="Level")
    teamdata['autoChargeStationPoints'][i]         += tbadata['autoChargeStationPoints'][dindex]
    teamdata['autoChargeStationRobot'][i]          += bool(tbadata['autoChargeStationRobot'+str(robotnum)][dindex]=="Docked")
    teamdata['autoDocked'][i]                      += bool(tbadata['autoDocked'][dindex])
    teamdata['autoGamePieceCount'][i]              += tbadata['autoGamePieceCount'][dindex]
    teamdata['autoGamePiecePoints'][i]             += tbadata['autoGamePiecePoints'][dindex]
    teamdata['autoMobilityPoints'][i]              += tbadata['autoMobilityPoints'][dindex]
    teamdata['autoPoints'][i]                      += tbadata['autoPoints'][dindex]
    teamdata['coopGamePieceCount'][i]              += tbadata['coopGamePieceCount'][dindex]
    teamdata['coopertitionCriteriaMet'][i]         += bool(tbadata['coopertitionCriteriaMet'][dindex])
    teamdata['endGameBridgeLevel'][i]              += bool(tbadata['endGameBridgeState'][dindex]=="Level")
    teamdata['endGameChargeStationPoints'][i]      += tbadata['endGameChargeStationPoints'][dindex]
    teamdata['endGameChargeStationRobotParked'][i] += bool(tbadata['endGameChargeStationRobot'+str(robotnum)][dindex]=="Park")
    teamdata['endGameChargeStationRobotDocked'][i] += bool(tbadata['endGameChargeStationRobot'+str(robotnum)][dindex]=="Docked")
    teamdata['endGameParkPoints'][i]               += tbadata['endGameParkPoints'][dindex]
    teamdata['foulCount'][i]                       += tbadata['foulCount'][dindex]
    teamdata['foulPoints'][i]                      += tbadata['foulPoints'][dindex]
    teamdata['linkPoints'][i]                      += tbadata['linkPoints'][dindex]
    teamdata['mobilityRobot'][i]                   += bool(tbadata['mobilityRobot'+str(robotnum)][dindex]=="Yes")
    teamdata['rp'][i]                              += tbadata['rp'][dindex]
    teamdata['sustainabilityBonusAchieved'][i]     += bool(tbadata['sustainabilityBonusAchieved'][dindex])
    teamdata['teleopGamePieceCount'][i]            += tbadata['teleopGamePieceCount'][dindex]
    teamdata['teleopGamePiecePoints'][i]           += tbadata['teleopGamePiecePoints'][dindex]
    teamdata['teleopPoints'][i]                    += tbadata['teleopPoints'][dindex]
    teamdata['totalChargeStationPoints'][i]        += tbadata['totalChargeStationPoints'][dindex]

length = len(tbadata['team1'])

for i in range(0, length*3, 1):
    robotnum = (i%3)+1
    gamenum = (i-(i%3))/3
    tname = tbadata['team'+str(robotnum)][gamenum]
    tindex = findIndex(tname)
    if tindex == None:
        tindex = len(teamdata['team'])
        zeroTeamData()

        teamdata['team'][tindex] = tname
    setTeam(tindex, gamenum, robotnum)
    print(f'Processing teamdata ({round(((i/(length*3))*100), 3)}%)', end='\r')
print(f'Processing teamdata (100%)    ')

length = len(teamdata['team'])

def removeData():
    length = len(teamdata['team'])
    for i in range(0, length, 1):
        matches = teamdata['matches'][i]
        if matches <= 5:
            removeTeam(i)
            removeData()
            break
removeData()

length = len(teamdata['team'])

for i in range(0, length, 1):
    matches = teamdata['matches'][i]
    teamdata['points'][i]                          = round((teamdata['points'][i]/matches), 3)
    teamdata['wins'][i]                            = round((teamdata['wins'][i]/matches), 3)
    teamdata['activationBonusAchieved'][i]         = round((teamdata['activationBonusAchieved'][i]/matches), 3)
    teamdata['autoBridgeLevel'][i]                 = round((teamdata['autoBridgeLevel'][i]/matches), 3)
    teamdata['autoChargeStationPoints'][i]         = round((teamdata['autoChargeStationPoints'][i]/matches), 3)
    teamdata['autoChargeStationRobot'][i]          = round((teamdata['autoChargeStationRobot'][i]/matches), 3)
    teamdata['autoDocked'][i]                      = round((teamdata['autoDocked'][i]/matches), 3)
    teamdata['autoGamePieceCount'][i]              = round((teamdata['autoGamePieceCount'][i]/matches), 3)
    teamdata['autoGamePiecePoints'][i]             = round((teamdata['autoGamePiecePoints'][i]/matches), 3)
    teamdata['autoMobilityPoints'][i]              = round((teamdata['autoMobilityPoints'][i]/matches), 3)
    teamdata['autoPoints'][i]                      = round((teamdata['autoPoints'][i]/matches), 3)
    teamdata['coopGamePieceCount'][i]              = round((teamdata['coopGamePieceCount'][i]/matches), 3)
    teamdata['coopertitionCriteriaMet'][i]         = round((teamdata['coopertitionCriteriaMet'][i]/matches), 3)
    teamdata['endGameBridgeLevel'][i]              = round((teamdata['endGameBridgeLevel'][i]/matches), 3)
    teamdata['endGameChargeStationPoints'][i]      = round((teamdata['endGameChargeStationPoints'][i]/matches), 3)
    teamdata['endGameChargeStationRobotParked'][i] = round((teamdata['endGameChargeStationRobotParked'][i]/matches), 3)
    teamdata['endGameChargeStationRobotDocked'][i] = round((teamdata['endGameChargeStationRobotDocked'][i]/matches), 3)
    teamdata['endGameParkPoints'][i]               = round((teamdata['endGameParkPoints'][i]/matches), 3)
    teamdata['foulCount'][i]                       = round((teamdata['foulCount'][i]/matches), 3)
    teamdata['foulPoints'][i]                      = round((teamdata['foulPoints'][i]/matches), 3)
    teamdata['linkPoints'][i]                      = round((teamdata['linkPoints'][i]/matches), 3)
    teamdata['mobilityRobot'][i]                   = round((teamdata['mobilityRobot'][i]/matches), 3)
    teamdata['rp'][i]                              = round((teamdata['rp'][i]/matches), 3)
    teamdata['sustainabilityBonusAchieved'][i]     = round((teamdata['sustainabilityBonusAchieved'][i]/matches), 3)
    teamdata['teleopGamePieceCount'][i]            = round((teamdata['teleopGamePieceCount'][i]/matches), 3)
    teamdata['teleopGamePiecePoints'][i]           = round((teamdata['teleopGamePiecePoints'][i]/matches), 3)
    teamdata['teleopPoints'][i]                    = round((teamdata['teleopPoints'][i]/matches), 3)
    teamdata['totalChargeStationPoints'][i]        = round((teamdata['totalChargeStationPoints'][i]/matches), 3)
    print(f'Cleaning teamdata ({round(((i/length)*100), 3)}%)', end='\r')
print(f'Cleaning teamdata (100%)    ')

pd.DataFrame(teamdata).to_csv('TBAteams.csv')
