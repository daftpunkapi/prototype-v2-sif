from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka import errors

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins='http://10.1.229.100:3000')

producer = KafkaProducer(
    bootstrap_servers='localhost:9092'
)

try:
    admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')
    admin_client.create_topics([
        NewTopic(name='cursor_positions', num_partitions=1, replication_factor=1),
        NewTopic(name='mouse_clicks', num_partitions=1, replication_factor=1)
    ])
except errors.TopicAlreadyExistsError:
    pass

@socketio.on('connect')
def handle_connect():
    print(f'A client has connected... {request.sid}')

@socketio.on('cursorMove')
def handle_cursor_move(data):
    print(data)
    # producer.send('cursor_positions', value=bytes(json.dumps(data), 'utf-8'))

@socketio.on('mouseClick')
def handle_mouse_click(data):
    print(data)
    producer.send('mouse_clicks', value=bytes(data, 'utf-8'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3001)
