import os
from sys import platform
import socketio as sioclient
from time import sleep
from flask import Flask, render_template, session, request, send_from_directory
from flask_socketio import test_client, emit
from flask_socketio import SocketIO

import jsonpack
import oprs

webroot = os.getcwd() + "/web/"
dataroot = os.getcwd() + "/data/"

# Windows is weird, and flask expects linux-styled directories, even in windows.
if platform in ['nt', 'win32', 'win64']:
    webroot = webroot.split(':')[1].replace('\\', '/')
    dataroot = dataroot.split(':')[1].replace('\\', '/')

Username = 'Username'
selectedEvent = ''
selectedPosition = 'red-1'
curMatch = ''
curPitTeam = ''

def makeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

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

def writeFile(path, data):
    if not os.path.exists(path):
        with open(path, mode='a'): pass
    with open(path, 'w') as f:
        f.write(data)

def findFiles(folder, term):
    returnFiles = []
    files = getSubfolders(folder)
    for file in files:
        if term in file:
            returnFiles.append(file)
    return returnFiles

def getTeams(event):
    if not os.path.exists(dataroot+event):
        return []
    if not os.path.exists(dataroot+event+"/matches.jsonpack"):
        return []
    # try:
    teams = []
    data = jsonpack.unpack(openFile(dataroot+event+"/matches.jsonpack"))['alliances']
    for match in data:
        for redbot in match['red']:
            bot = int(redbot)
            if not bot in teams:
                teams.append(bot)
        for bluebot in match['blue']:
            bot = int(bluebot)
            if not bot in teams:
                teams.append(bot)
    teams = list(set(teams))
    teams.sort()
    result = []
    for team in teams:
        result.append(str(team))
    return result
    # except:
    #     return []

app = Flask(__name__,
            static_url_path=webroot, 
            static_folder=webroot,
            template_folder=webroot)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# For all the /web/src paths
@app.route('/src/<path:file>')
def static_file(file):
    return app.send_static_file("src/"+file)

# Dynamic pages
@app.route('/data/team/<path:team>')
def frcTeam(team):
    return app.send_static_file("team.html")

@app.route('/data/match/<path:match>')
def match(match):
    return app.send_static_file("match.html")




@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("src/favicon.ico")

@app.route('/')
@app.route('/data')
def index():
    return app.send_static_file("index.html")

@app.route('/data/teams')
def teams():
    return app.send_static_file("teams.html")

@app.route('/data/matches')
def matches():
    return app.send_static_file("matches.html")


@app.route('/data/predictor')
def predictor():
    return app.send_static_file("predictor.html")

@app.route('/data/selector')
def selector():
    return app.send_static_file("selector.html")

@app.route('/scout/match')
def matchscout():
    return app.send_static_file("matchscout.html")

@app.route('/scout/pit')
def pitscout():
    return app.send_static_file("pitscout.html")


@app.route('/scout/practice')
def practice():
    return app.send_static_file("practice.html")

@app.route('/qrgen')
def qrgen():
    return app.send_static_file("qrgen.html")

@app.route('/fileupload')
def fileupload():
    return app.send_static_file("fileupload.html")

@app.route('/qrscan')
def qrscan():
    return app.send_static_file("qrscan.html")

@app.route('/tba')
def tba():
    return app.send_static_file("TBA.html")



# Log stuff
@socketio.on('connect')
def connect():
    print('Client connected', request.sid)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)



# Controlling the Username from the browser
@socketio.on('getUsername')
def getUsername():
    global Username
    socketio.emit('username', Username)

@socketio.on('setUsername')
def setUsername(data):
    global Username
    Username = data
    socketio.emit('username', Username)



# Controlling the Selected Event from the browser
@socketio.on('getSelectedEvent')
def getSelectedEvent():
    global selectedEvent
    socketio.emit('selectedEvent', selectedEvent)

@socketio.on('setSelectedEvent')
def setSelectedEvent(data):
    global selectedEvent
    global curMatch
    global curPitTeam
    selectedEvent = data
    curMatch = ''
    curPitTeam = ''
    socketio.emit('selectedEvent', selectedEvent)


# Controlling the position from the browser (ie 'blue-2')
@socketio.on('getMatchPosition')
def getPosition():
    global selectedPosition
    socketio.emit('matchPosition', selectedPosition)

@socketio.on('setMatchPosition')
def setPosition(data):
    global selectedPosition
    selectedPosition = data
    socketio.emit('matchPosition', selectedPosition)



@socketio.on('getCurMatch')
def getCurMatch():
    global curMatch
    socketio.emit('curMatch', curMatch)

@socketio.on('setCurMatch')
def setCurMatch(data):
    global curMatch
    curMatch = data
    socketio.emit('curMatch', curMatch)



@socketio.on('getCurPitTeam')
def getCurPitTeam():
    global curPitTeam
    socketio.emit('curPitTeam', curPitTeam)

@socketio.on('setCurPitTeam')
def setCurPitTeam(data):
    global curPitTeam
    curPitTeam = data
    socketio.emit('curPitTeam', curPitTeam)



# Listing folders & files from the browser
# getFolders just returns the folders in the data folder
@socketio.on('getFolders')
def get():
    makeDir(dataroot)
    socketio.emit('folderList', '•'.join(getSubfolders(dataroot)))

# getEvents lists the folders with a "matches.jsonpack" in them, VALID events
@socketio.on('getEvents')
def getEvents():
    makeDir(dataroot)
    eventnames = []
    folders = getSubfolders(dataroot)
    for folder in folders:
        if os.path.exists(dataroot+folder+"/matches.jsonpack"):
            eventnames.append(folder)
    socketio.emit('eventList', ('•'.join(eventnames), selectedEvent))

# List the files in a folder
@socketio.on('getFilesInEvent')
def getFilesInEvent(path):
    socketio.emit('eventFileList', '•'.join(getSubfolders(dataroot+path)))

# Get data from a EventFolder/EventFile
@socketio.on('readFromFile')
def readFromFile(dirname, filename):
    data = openFile(dataroot+dirname+"/"+filename)
    print(f'read from {dirname}/{filename} ({len(data)} bytes)')
    socketio.emit('eventFileContent', (dirname, filename, data))


@socketio.on('writeToFile')
def writeToFile(dirname, filename, data):
    makeDir(dataroot)
    makeDir(dataroot+dirname)
    writeFile(dataroot+dirname+"/"+filename, data)
    print(f'Recieved file {dirname}/{filename} ({len(data)} bytes)')



@socketio.on('getTeams')
def getTeamList(eventName):
    teamList = getTeams(eventName)
    socketio.emit('teamList', '•'.join(teamList))

@socketio.on('getMultipleFiles')
def getMultipleFiles(eventName, files):
    data = []
    folder = dataroot+eventName+'/'
    for file in files:
        filedata = ''
        try:
            filedata = jsonpack.unpack(openFile(folder+file))
        except:
            pass
        data.append({
            'key': file,
            'data': filedata
        })
    teamList = getTeams(eventName)
    socketio.emit('multipleFiles', data)

@socketio.on('gePitScoutingData')
def gePitScoutingData(eventName, teamName):
    filename = dataroot+eventName+'/pitscout-'+teamName+'.jsonpack'
    socketio.emit('pitScoutingData', openFile(filename))

@socketio.on('getProcessedData')
def getProcessedData(eventName):
    if eventName == '': socketio.emit('processedData', ([], False)); return
    data, pinvInaccuracy = oprs.getProcessedData(eventName)
    print(data)
    socketio.emit('processedData', (jsonpack.pack(data), pinvInaccuracy))
    


# Because of CORS, the browser cannot connect to another scouting laptop
@socketio.on('sendViaWifi')
def sendViaWifi(ip, dirname, files):
    address = f'ws://{ip}:4388'
    with sioclient.SimpleClient() as sio:
        sio.connect(address)
        for file in files:
            data = openFile(dataroot+dirname+"/"+file)
            sio.emit('writeToFile', (dirname, file, data))
            print(f'Sent {dirname}/{file} to {address}')
            sleep(0.2)


if __name__ == '__main__':
    socketio.run(app, port=4388, host='0.0.0.0')
