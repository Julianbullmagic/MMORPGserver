const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);
setInterval(getState, 200)

function getState(){
  io.emit('getState')
}

let players=[]
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('chat message', (msg) => {
  console.log('message: ' + msg);
});
socket.on('disconnect', () => {
  console.log('user disconnected');
});
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});

io.on('returning state', (data) => {
  console.log("returning state",data.player)
});
