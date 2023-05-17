const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);
setInterval(getState, 2000)

function getState(){
  console.log("getting state")
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
socket.on("connect_error", (err) => {
  console.log(`connect_error due to ${err.message}`);
});
socket.on('returning state', (data) => {
  console.log("returning state",data)
});
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});
