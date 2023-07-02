import redis
import json
from confluent_kafka import Consumer


r = redis.Redis(
  host='redis-17789.c240.us-east-1-3.ec2.cloud.redislabs.com',
  port=17789,
  password='h45ka0mIdaTW3YK4RdKUDmtngakqun5Z')

# Test the connection
try:
    response = r.ping()
    if response:
        print('Successfully connected to Redis')
except redis.exceptions.ConnectionError as e:
    print(f'Failed to connect to Redis: {e}')

c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'feature_group_upsert6','auto.offset.reset':'earliest'})
c.subscribe(['feature_clicks_upsert'])


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
        avg_count_5s = data['avg_count_5s']
        avg_count_10s = data['avg_count_10s']
        avg_count_30s = data['avg_count_30s']

       

        # Construct the key and value for Redis storage
        redis_key = session_id
        redis_value = json.dumps({
            'avg_count_5s': avg_count_5s,
            'avg_count_10s': avg_count_10s,
            'avg_count_30s': avg_count_30s
        })

        # Store the data in Redis
        r.set(redis_key, redis_value)


if __name__ == '__main__':
    main()

# import mysql.connector

# Connect to the MySQL database
# cnx = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='sw23',
#     database='flink'
# )

# cursor = cnx.cursor()
        # Send message data to Redis
        # r.hset('feature_clicks_data', data.sessionId, data)
        # print('Message data sent to Redis')

# def main():
#     while True:
#         msg = c.poll(1.0)  # timeout
#         if msg is None:
#             continue
#         if msg.error():
#             print('Error: {}'.format(msg.error()))
#             continue
#         data = msg.value().decode('utf-8')
#         # print(data)

        # Upsert the data into the MySQL table
        # upsert_query = "INSERT INTO flink_final (sessionId, avg_count_5s, avg_count_10s, avg_count_30s) " \
        #             "VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE " \
        #             "avg_count_5s=VALUES(avg_count_5s), avg_count_10s=VALUES(avg_count_10s), " \
        #             "avg_count_30s=VALUES(avg_count_30s)"

        # upsert_data = (session_id, avg_count_5s, avg_count_10s, avg_count_30s)
        # cursor.execute(upsert_query, upsert_data)

