from confluent_kafka import Consumer

c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})
c.subscribe(['mouse_clicks'])

# for message in c:
#     print(message.value)

def main():
    while True:
        msg=c.poll(1.0) #timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data=msg.value().decode('utf-8')
        print(data)
    c.close()

main()