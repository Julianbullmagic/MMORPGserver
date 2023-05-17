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
  players.push({id:socket.id})
  socket.on('chat message', (msg) => {
  console.log('message: ' + msg);
});
socket.on('disconnect', () => {
  console.log('user disconnected');
  players.filter(player=>player.id!==socket.id)
});
socket.on("connect_error", (err) => {
  console.log(`connect_error due to ${err.message}`);
});
socket.on('returning state', (data) => {
  console.log("returning state",data,players)
  for (let player of players){
    if(socket.id==player.id){
      player.x=data.offsetx
      player.y=data.offsety
      player.angle=data.angle
    }
  }
});
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});
