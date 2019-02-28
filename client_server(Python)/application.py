from flask_socketio import SocketIO, emit
from flask import Flask, request, redirect, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
from server import MySocket
from forms import RegisterForm, MessageForm

import os
os.system('netsh wlan set hostednetwork mode=allow ssid=ferid key=12345678')
os.system('netsh wlan start hostednetwork')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()
socket = MySocket()

class RandomThread(Thread):
    def __init__(self):
        super(RandomThread, self).__init__()

    def messageReciever(self):
        socket.construct()
        while not thread_stop_event.isSet():
            print("Waiting for message...")
            message = socket.getData()
            if not message:
                socket.construct()
            else:
                socketio.emit('newmessage', {'message': message.decode("utf-8")}, namespace='/test')
                print('Mesage from Client: ' + message.decode("utf-8"))
                sleep(0.3)

    def run(self):
        self.messageReciever()

@socketio.on('connect', namespace='/test')
def on_connect():
    print('connection established')

@socketio.on('disconnect', namespace='/test')
def socket_disconnect():
    print('Client disconnected')


###################################
 
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    form = MessageForm(request.form)
    if request.method == 'POST' and form.validate():
        message = form.message.data
        socket.sendData(message)
        return render_template('chat.html')
    return render_template('chat.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        password = form.password.data

        try:
            os.system('netsh wlan set hostednetwork mode=allow ssid=' + name + ' key=' + password)
            os.system('netsh wlan start hostednetwork')
            
            global thread
            if not thread.isAlive():
                thread = RandomThread()
                thread.start()
        except Exception as e:
            print('Could not created HotSpot' + str(e))

        return redirect(url_for('chat'))
    return render_template('home.html', form=form)


if __name__ == '__main__':
    socketio.run(app)
