const express = require('express');
const http = require('http');
const {Server} = require('socket.io');
const cors = require('cors');


const app = express();
app.use(cors());

const server = http.createServer(app);

const io = new Server(server, {
   cors: {
    origin: "http://10.1.229.100:3000",
    methods: ["GET","POST"],
   }
});

io.on("connection", (socket) => {
    console.log(`A client has connected... ${socket.id}`);

    socket.on("cursorMove", (data) => {
        console.log(data)
    });
    
    socket.on("mouseClick", (data) => {
        console.log(data)
    });

});

server.listen(3001, ()=> {console.log('Server chal raha hain BC!')});