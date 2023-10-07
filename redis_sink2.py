import redis
import json
from confluent_kafka import Consumer


r = redis.Redis(
  host='INSERT_YOUR_HOST',
  port=17789,
  password='INSERT_YOUR_KEY')

# Test the connection
try:
    response = r.ping()
    if response:
        print('Successfully connected to Redis')
except redis.exceptions.ConnectionError as e:
    print(f'Failed to connect to Redis: {e}')

c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'feature_cursor_group','auto.offset.reset':'earliest'})
c.subscribe(['feature_cursor'])


def main():
    while True:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        if msg.value() is None:
            continue
        data = msg.value().decode('utf-8')
        data = json.loads(data)
        print(data)

        # Extract the values from the message
        session_id = data['sessionId']
        avg_vel = data['avg_vel']
        tot_dist = data['tot_dist']

        # Construct the key and value for Redis storage
        table_name = 'cursor_table'  # Specify the table name
        redis_key = f'{table_name}:{session_id}'  # Include the table name in the key
        redis_value = json.dumps({
            'avg_vel': avg_vel,
            'tot_dist':tot_dist
        })

        # Store the data in Redis
        r.set(redis_key, redis_value)


if __name__ == '__main__':
    main()

