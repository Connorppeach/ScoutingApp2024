import requests
import json
import numpy as np
import os
from decimal import Decimal

import jsonpack

# Code is based on https://github.com/Riteka/FRCBoardProj-OPR-DPR-CCWM/blob/master/API%20Version.py

np.set_printoptions(edgeitems=200)

headers = {"User-Agent": "Mozilla/5.0", "X-TBA-Auth-Key": "fzQY0pv6qwfwuII5Xx2bmP57BBSuE0maxKailYlrI0e1EdfKCq6F3Th9FFDqpW7f"}

def fetch_json(link):
    return requests.get(link, headers=headers).json()


def find_num_of_teams(json_file): 	
    allteams = []
    for match in json_file:
        #teamcount += 1
        for x in range(0,3):
            allteams.append(match["red"][x][3:])
        for y in range(0,3):
            allteams.append(match["blue"][y][3:])
    teams = list(set(allteams))
    teams.sort()
    return (len(teams))
    



def find_num_of_alliances(json_file): 
    alliancecount = len(json_file) * 2
    return(alliancecount)



def teams_least_to_greatest(matches): 
    allteams = []
    for match in matches:
        #teamcount += 1
        for x in range(0,3):
            allteams.append(int(match["red"][x][3:]))
        for y in range(0,3):
            allteams.append(int(match["blue"][y][3:]))
    teams = list(set(allteams))
    teams.sort()
    return (teams)
    


def initmatrix(num_of_teams, num_of_alliances, json_file, teams, OPR_DPR):
    M_array = np.zeros( ((num_of_alliances), num_of_teams), dtype = int ) #initializing a matrix of 0's with num_alliances rows and num_alliance columns
    s_array = np.zeros( (num_of_alliances, 1) ) #initializing the alliance score matrix
    row_num = 0
    
    if (OPR_DPR == 'OPR'):
        for match in json_file:
            for x in range(0,3):			#x is to access the different teams within the red alliance in the specific match
                z = int(match["red"][x][3:])
                index = teams.index(z)
                M_array[row_num][index] = 1
            s_array[row_num] = match["redscore"]
            row_num += 1

            for y in range(0,3):		#y is to access the different teams within the blue alliance in the specific match
                r = int(match["blue"][y][3:])
                index = teams.index(r)
                M_array[row_num][index] = 1
            s_array[row_num] = match["bluescore"]
            row_num += 1

    if (OPR_DPR == "DPR"):
        for match in json_file:
            for x in range(0,3):			#x is to access the different teams within the red alliance in the specific match
                z = int(match["red"][x][3:])
                index = teams.index(z)
                M_array[row_num][index] = 1
            s_array[row_num] = match["bluescore"]
            row_num += 1

            for y in range(0,3):		#y is to access the different teams within the blue alliance in the specific match
                r = int(match["blue"][y][3:])
                index = teams.index(r)
                M_array[row_num][index] = 1
            s_array[row_num] = match["redscore"]
            row_num += 1

    return([M_array, s_array])


def isSquare (matrix): 
    return all (len(row)==len(matrix) for row in matrix) #this function is just to check if the matrix is square or not


def OPR_or_DPR_Calc(initmatrixresults): 
#since the number of matches (represents the number of equations) is greater than the number of teams in the event (represents the variables), overdetermined
    M_array = initmatrixresults[0]		#since the initmatrix() function is being passed in, the individual parts of the list that initmatrix() returns, represents M_array and the s_array
    s_array = initmatrixresults[1]
    
    transposed = M_array.transpose()
    transposed_copy = transposed
    left_side = transposed.dot(M_array)
    #print(isSquare(left_side))
    #print(np.linalg.det(left_side))			#this just gives the determinant of the matrix for debugging
    pinvInaccuracy = False
    try:
        inverse_left = np.linalg.inv(left_side)
    except:
        inverse_left = np.linalg.pinv(left_side)
        pinvInaccuracy = True

    inverse_left_copy = inverse_left

    right_side = transposed_copy.dot(s_array)
    final_right_side = inverse_left_copy.dot(right_side)

    return(final_right_side, pinvInaccuracy)


def calc(json):
    #matches_json = fetch_json('https://www.thebluealliance.com/api/v3/event/%s/matches' % (event_key))
    num_of_teams = find_num_of_teams(json)
    num_of_alliances = find_num_of_alliances(json)
    
    teams = teams_least_to_greatest(json)
    #print(teams)
    OPR_matrix                     = initmatrix(num_of_teams, num_of_alliances, json, teams, "OPR")
    OPR_results, pinvInaccuracyOPR = OPR_or_DPR_Calc(OPR_matrix)
    DPR_matrix                     = initmatrix(num_of_teams, num_of_alliances, json, teams, "DPR")
    DPR_results, pinvInaccuracyDPR = OPR_or_DPR_Calc(DPR_matrix)

    # When the matrix is inverted in OPR_or_DPR_Calc, it can give an error if not enough matches are scouted
    # To let the scouters see their results better, the func pinv won't have this error
    # But the pinv function isn't always accurate, So the two funcs can be switched between
    # And its better to make a var that represents this error.
    pinvInaccuracy = (pinvInaccuracyOPR | pinvInaccuracyDPR)

    result = []
    for i, _ in enumerate(OPR_results):
        OPR = round(float(OPR_results[i]),2)
        DPR = round(float(DPR_results[i]),2)
        CCWM = round((OPR - DPR),2)
        team = "frc" + str(teams[i])
        result.append({
            'key': team,
            'OPR': OPR,
            'DPR': DPR,
            'CCWM': CCWM
        })
    return result, pinvInaccuracy











def getSubfolders(path):
    try:
        return os.listdir(path)
    except:
        return None

def openFile(path):
    if not os.path.exists(path):
        return ''
    try:
        with open(path) as f:
            return f.read()
    except:
        return ''

def makeObject(parent, key):
    try:
        if parent[key] == None:
            parent[key] = {}
    except:
        parent[key] = {}
    return parent

def makeArray(parent, key):
    try:
        if parent[key] == None:
            parent[key] = []
    except:
        parent[key] = []
    return parent

def makeNumber(parent, key):
    try:
        if parent[key] == None:
            parent[key] = 0
    except:
        parent[key] = 0
    return parent

#Get the MODE of a list, but also avrage the results
def avgMode(scoreList):
    scores = []
    counts = []
    for score in scoreList:
        if not score in scores:
            scores.append(score)
            counts.append(1)
        else:
            counts[scores.index(score)] += 1
    maxCount = max(counts)
    maxs = [scores[i] for i, x in enumerate(counts) if x == maxCount]
    return round(sum(maxs)/len(maxs))


dataroot = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/")

def getProcessedData(eventName):
    tmpMatchData = {}
    files = []
    teamResults = {}
    matchlist = openFile(dataroot+eventName+'/matches.jsonpack')
    
    if matchlist == '': return
    matchlist = jsonpack.unpack(matchlist)
    for file in getSubfolders(dataroot+eventName):
        if file.split('-')[0] != 'matchscout':
            continue
        files.append(file)

        match = file.split('-')[1]
        alliance = file.split('-')[2]

        matchdata = matchlist[int(match.split('qm')[1])-1]
        scoutdata = jsonpack.unpack(openFile(dataroot+eventName+'/'+file))
        key = file.split('-')[1]

        makeObject(tmpMatchData, key)
        makeArray(tmpMatchData[key], 'blue')
        makeArray(tmpMatchData[key], 'red')
        makeArray(tmpMatchData[key], 'bluewins')
        makeArray(tmpMatchData[key], 'blueScores')
        makeArray(tmpMatchData[key], 'redScores')

        tmpMatchData[key]['blue'] = matchdata['blue']
        tmpMatchData[key]['red'] = matchdata['red']

        tmpMatchData[key]['blueScores'].append(scoutdata['blueScore'])
        tmpMatchData[key]['redScores'].append(scoutdata['redScore'])
        
        if alliance == 'blue':
            tmpMatchData[key]['bluewins'].append(scoutdata['win'])
        else:
            tmpMatchData[key]['bluewins'].append(not scoutdata['win'])

        team = scoutdata['team']
        makeObject(teamResults, team)
        makeNumber(teamResults[team], 'autoPerformance')
        teamResults[team]['autoPerformance'] += int(scoutdata['autoPerformance'])
        makeNumber(teamResults[team], 'teleopPerformance')
        teamResults[team]['teleopPerformance'] += int(scoutdata['teleopPerformance'])
        makeNumber(teamResults[team], 'overallPerformance')
        teamResults[team]['overallPerformance'] += int(scoutdata['overallPerformance'])
        makeNumber(teamResults[team], 'endState')
        teamResults[team]['endState'] += int(scoutdata['endState'])
        makeNumber(teamResults[team], 'scoreArea')
        teamResults[team]['scoreArea'] += int(scoutdata['scoreArea'])

    #print(tmpMatchData)
    oprData = []
    for file in files:
        match = file.split('-')[1]
        alliance = file.split('-')[2]
        position = file.split('-')[3]

        matchData = tmpMatchData[match]

        exists = False
        for opr in oprData:
            if opr['key'] == match:
                exists = True

        if not exists:

            bluescore = avgMode(matchData['blueScores'])
            redscore = avgMode(matchData['redScores'])
            bluewin = avgMode(matchData['bluewins'])==1

            for team in matchData['blue']:
                makeObject(teamResults, team)
                makeArray(teamResults[team], 'scores')
                makeArray(teamResults[team], 'wins')
                teamResults[team]['scores'].append(bluescore)
                teamResults[team]['wins'].append(bluewin)
            for team in matchData['red']:
                makeObject(teamResults, team)
                makeArray(teamResults[team], 'scores')
                makeArray(teamResults[team], 'wins')
                teamResults[team]['scores'].append(redscore)
                teamResults[team]['wins'].append(not bluewin)

            oprData.append({
                'key': match,
                'blue': matchData['blue'],
                'red': matchData['red'],
                'bluescore': bluescore,
                'redscore': redscore
            })
    oprData, pinvInaccuracy = calc(oprData)

    
    for teamOPR in oprData:
        key = teamOPR['key']
        teamResult = teamResults[key]

        makeNumber(teamOPR, 'avgScore')
        if teamResult['scores'] == []:
            teamOPR['avgScore'] = 0
        else:
            x = sum(teamResult['scores'])/len(teamResult['scores'])
            teamOPR['avgScore'] = round(x, 2)

        makeNumber(teamOPR, 'winPercent')
        if teamResult['wins'] == []:
            teamOPR['winPercent'] = 0
        else:
            x = sum(teamResult['wins'])/len(teamResult['wins'])
            teamOPR['winPercent'] = round(x*100, 2)



        makeNumber(teamOPR, 'autoPerformance')
        try:
            teamOPR['autoPerformance'] = teamResult['autoPerformance']
        except:
            teamOPR['autoPerformance'] = 0

        makeNumber(teamOPR, 'teleopPerformance')
        try:
            teamOPR['teleopPerformance'] = teamResult['teleopPerformance']
        except:
            teamOPR['teleopPerformance'] = 0

        makeNumber(teamOPR, 'overallPerformance')
        try:
            teamOPR['overallPerformance'] = teamResult['overallPerformance']
        except:
            teamOPR['overallPerformance'] = 0

        makeNumber(teamOPR, 'endState')
        try:
            teamOPR['endState'] = teamResult['endState']
        except:
            teamOPR['endState'] = 0

        makeNumber(teamOPR, 'scoreArea')
        try:
            teamOPR['scoreArea'] = teamResult['scoreArea']
        except:
            teamOPR['scoreArea'] = 0


    return oprData, pinvInaccuracy