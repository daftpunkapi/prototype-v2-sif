from flask import Flask, request, Response
from flask_cors import CORS
from flask_socketio import SocketIO
from kafka import KafkaProducer
import json 

# Remove unwanted log stream from console
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'dpapi55'

socketio = SocketIO(app, cors_allowed_origins='*')

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic_clicks = 'mouse_clicks'
topic_cursor = 'cursor_positions'

@socketio.on('connect')
def handle_connect():
    print(f'A client has connected')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected')

@socketio.on('cursorMove')
def handle_cursor_move(data):
    print(data)
    send_to_kafka(data, topic_cursor)

@socketio.on('mouseClick')
def handle_mouse_click(data):
    print(data)
    send_to_kafka(data,topic_clicks)

def send_to_kafka(data, topic):
    record = json.dumps(data)
    producer.send(topic, record.encode('utf-8'))

@app.route('/session_input', methods=['POST'])
def sessionId_input():
    body_params = request.json
    sessionId = body_params['sessionId']
    print("The session ID of the user is:", sessionId)
    response_data = {'message': 'Session ID received successfully'}
    response = Response(json.dumps(response_data), mimetype='application/json')
    return response


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3001)