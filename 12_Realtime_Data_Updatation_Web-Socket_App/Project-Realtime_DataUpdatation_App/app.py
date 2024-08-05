from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket event to handle client connections
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Function to send data to the client in a background thread
def background_thread():
    count = 0
    while True:
        time.sleep(5)  # Update the message every 5 seconds
        count += 5
        data = {'message': f'Updates Number from the server.. ==> {count**2}'}
        socketio.emit('update_data', data)

# Start the background thread when the application is run
if __name__ == '__main__':
    thread = Thread(target=background_thread)
    thread.daemon = True
    thread.start()
    socketio.run(app, debug=True, use_reloader=False,allow_unsafe_werkzeug=True)
