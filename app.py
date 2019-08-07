from flask import Flask, request, current_app, Response
from flask import render_template
from flask_socketio import SocketIO, disconnect, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
connected = False
clients = []
respondedClients = []
messegedClients = []

def send_ping(json='ping'):
    socketio.emit('ping_msg', str('ping'), namespace='/')

@socketio.on('connect')  # global namespace
def handle_connect():
    clients.append(request.sid)
    print("client added : "+','.join(clients))
    print('Client connected')

@socketio.on('pong_message')
def handle_pong(msg):
    '''
    Handelling response from client for PING message
    '''
    if msg == 'PONG' :
        print("received response from : " +request.sid)
        respondedClients.append(request.sid)

@socketio.on('disconnect', namespace='/')
def test_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getClients')
def get_clients():
    return Response(json.dumps(clients), status=200)

