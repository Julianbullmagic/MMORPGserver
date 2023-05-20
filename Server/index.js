const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);
setInterval(sendState, 500)


function sendState(){
  console.log("returning state",players)
  io.emit('updateState',JSON.stringify(players))
}

let players=[]
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
  console.log('a user connected');
  let playerid=""
  socket.on('player joining', (data) => {
    let parseddata=JSON.parse(data)
    playerid=parseddata.name
    players.push({id:parseddata.name,x:0,y:0,angle:0})
  });
socket.on('disconnect', () => {
  console.log('user disconnected');
});
socket.on("connect_error", (err) => {
  console.log(`connect_error due to ${err.message}`);
});
socket.on('returning state', (data) => {
  let parseddata=JSON.parse(data)
  for (let player of players){
    if(parseddata.id==player.id){
      player.x=parseddata.offsetx
      player.y=parseddata.offsety
      player.angle=parseddata.angle
    }
  }
});
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});
