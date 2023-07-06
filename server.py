from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
from kafka import KafkaProducer
import json 
from model.prediction import risk_predict

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
    IP_country_code = body_params['IP_country_code']
    paste_count = body_params['paste_count']
    print("The session ID of the user is : ", sessionId)
    risk = risk_predict(sessionId,IP_country_code,paste_count)
    print("The risk factor for this session ID is : ", risk)
    risk = risk.tolist()
    response = json.dumps(risk)
    return response


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3001)