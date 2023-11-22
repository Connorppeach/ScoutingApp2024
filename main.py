import os
from flask import Flask, render_template, session, request, send_from_directory
from flask_socketio import SocketIO, emit

webroot = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web/")
dataroot = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/")

def makeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getSubfolders(path):
    try:
        return os.listdir(path)
    except:
        return None

def openFile(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return None

def writeFile(path, data):
    # with open(path, 'x') as f:
    #     f.write(data)
    if not os.path.exists(path):
        with open(path, mode='a'): pass
    with open(path, 'w') as f:
        f.write(data)


app = Flask(__name__,
            static_url_path=webroot, 
            static_folder=webroot,
            template_folder=webroot)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/src/<path:file>')
def static_file(file):
    return app.send_static_file("src/"+file)



@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("src/favicon.ico")

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/matchscout')
def matchscout():
    return app.send_static_file("matchscout.html")

@app.route('/pitscout')
def pitscout():
    return app.send_static_file("pitscout.html")

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



@socketio.on('connect')
def connect():
    print('Client connected', request.sid)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)



@socketio.on('getMatches')
def getMatches():
    makeDir(dataroot)
    socketio.emit('MatchList', '•'.join(getSubfolders(dataroot)))

@socketio.on('getFilesInMatch')
def getFilesInMatch(path):
    socketio.emit('MatchFileList', '•'.join(getSubfolders(dataroot+path)))

@socketio.on('readFromFile')
def readFromFile(dirname, filename):
    socketio.emit('MatchFileContent', (dirname, filename, openFile(dataroot+dirname+"/"+filename)))

@socketio.on('writeToFile')
def writeToFile(dirname, filename, data):
    makeDir(dataroot)
    makeDir(dataroot+dirname)
    writeFile(dataroot+dirname+"/"+filename, data)

if __name__ == '__main__':
    socketio.run(app, port=4388, host='0.0.0.0')