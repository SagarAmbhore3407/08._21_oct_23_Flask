# app.py (update)
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/notify')
def notify():
    message = 'New update!'
    socketio.emit('message', message)
    return 'Notification sent!'

if __name__ == '__main__':
    socketio.run(app,allow_unsafe_werkzeug=True)
