var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = process.env.PORT || 3000;
var json = require('../users.json');
var defaults = require('../default.json');
var request = require('request');
var fs = require('fs');

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  socket.on('chat message', function(msg){
    io.emit('chat message', msg);
  });
  socket.on('message', (data) => {
    let date = new Date();
    defaults['users'][`${data.to}`]['inbound'].push({ 
      content: `${data.msg}`, 
      from: `${data.from}`, 
      to: `${data.to}`, 
      time: `${date.getMinutes()}`});
    defaults['users'][`${data.from}`]['insent'].push({ 
      content: `${data.msg}`, 
      from: `${data.from}`, 
      to: `${data.to}`,
      time: `${date.getMinutes()}`,
      encrypted: ''});
    var strfy = JSON.stringify(defaults, null, 3);
    fs.writeFile('../default.json', strfy, err => {
      if (err) throw err;
    });
    request(`http://127.0.0.1:5000/user/${data.to}`, { json: true }, (err, res, body) => {
      if (err) {return console.log(err);}
      console.log(body);
    });
  });
});

http.listen(port, function(){
  console.log('listening on *:' + port);
});
