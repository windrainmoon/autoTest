from app_src import socketio
from . import dataExtract
from flask import render_template
from flask_socketio import send, emit


@dataExtract.route('/')
def index():
    return render_template('dataExtract/index.html')


@socketio.on('message', namespace='/default')
def handle_message(msg):
    print('received message: ' + msg)


@socketio.on('client_event')
def client_msg(msg):
    emit('server_response', {'data': msg['data']}, broadcast=True)


@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})
