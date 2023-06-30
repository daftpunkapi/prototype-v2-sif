const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const { Kafka, Partitioners } = require('kafkajs');

const app = express();
app.use(cors());

const server = http.createServer(app);

const io = new Server(server, {
  cors: {
    origin: 'http://10.1.229.100:3000',
    methods: ['GET', 'POST'],
  },
});

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092'],
});

const producer = kafka.producer({
  createPartitioner: Partitioners.LegacyPartitioner,
});

const run = async () => {
  await producer.connect();
};

run().catch((error) => {
  console.error('Error connecting to Kafka:', error);
  process.exit(1);
});

io.on('connection', (socket) => {
  console.log(`A client has connected... ${socket.id}`);

  socket.on('cursorMove', (data) => {
    console.log(data);
    producer.send({
      topic: 'cursor_positions',
      messages: [{ value: JSON.stringify(data) }],
    });
  });

  socket.on('mouseClick', (data) => {
    console.log(data);
    producer.send({
      topic: 'mouse_clicks',
      messages: [{ value: JSON.stringify(data) }],
    });
  });
});

server.listen(3001, () => {
  console.log('Server chal raha hain BC!');
});
