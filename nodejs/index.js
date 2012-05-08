// Grab the modules we'll be using
var http = require('http');
var fs = require('fs');
var io = require('socket.io');

var rooms = [];
var room_embeds = [];
var room_starts = [];
// Sends the client html file
// The file is cached after the first time it's been read
function sendClientHtml(response) {
	if (sendClientHtml.cachedHtml) {
		response.writeHead(200, {'Content-Type': 'text/html', 'Transfer-Encoding': 'chunked'});
		response.write(sendClientHtml.cachedHtml);
		response.end();
	} else {
		fs.readFile('client.html', function(err, data) {
			sendClientHtml.cachedHtml = data;
			sendClientHtml(response);
		});
	}
}

//parse link for embed code
function getEmbedHTML(link) {
	var html = "";
	link = link.replace('http://','');
	link = link.replace('www.','');
	if (link.indexOf('youtube') != -1) {
		//http://www.youtube.com/watch?v=YvE91KHLrG4
		console.log("pre-embed:" + link);
		link = link.substring(20);
		if(link.indexOf('&')!= -1){
			link = link.substring(0,link.indexOf('&'));
		}
		html = "<iframe class=\"youtube-player\" type=\"text/html\" width=\"640\" height=\"385\" src=\"http://www.youtube.com/embed/"+link+"?autoplay=1&start=0\" frameborder=\"0\">\n</iframe>"
		console.log("pre-embed:" + link);
	} 
	else if (link.indexOf('twitch.tv') != -1){

	}
	return html;
}

function offsetVideo(embed,offset){
	var e = "" + embed;
	console.log(e);
	if (e.indexOf('youtube') != -1) {
		e = e.replace('&start=0','&start='+offset);
	}
	return e;
}

// Create the server
var app = http.createServer(function(request, response) {
	if (request.url == '/') {
		sendClientHtml(response);
	}
});

// Listen for Socket.IO events
var ioApp = io.listen(app);
ioApp
	.of('/listen')
	.on('connection', function(socket) {
		console.log('connection made');
		socket.on('set name', function(userName) {
			socket.username = userName;
			socket.room = 'room1';
			socket.join('room1');
			console.log('username: ' + userName);
			socket.emit('begin chat');	
		});
		socket.on('create room', function(userName, link) {
			socket.username = userName;
			var roomnum = Math.floor(Math.random()*100000);
			var room = ''+roomnum;
			while (room.length < 6){room = '0' + room;}
			room = '#!' + room; 			
			socket.room = room;
			socket.join(room);
			console.log('Room created!'+ room +' username: ' + userName);
			var embed = getEmbedHTML(link);
			var startTime = Math.round(new Date().getTime() / 1000.0);
			//add room details to arrays
			rooms.push(room);
			room_embeds.push(embed);
			room_starts.push(startTime);
			//http://localhost:1337/#!/#!075042
			socket.emit('begin chat', room,embed);	
		});
		socket.on('join room', function(userName, room) {
			socket.username = userName;
			var index = rooms.indexOf(room);
			if(index == -1){
				console.log('Unknown room:'+room);
			}
			socket.room = room;
			socket.join(room);
			console.log('Joining '+ room +'. Username: ' + userName);
			var offset =  Math.round(new Date().getTime() / 1000.0) - room_starts[index];
			var embed = offsetVideo(room_embeds[index],offset);
			console.log(embed);
			socket.emit('begin chat', embed);	
		});
	});

ioApp
	.of('/addText')
	.on('connection', function(socket) {
		socket.on('add text', function(data) {
			console.log(data.user + ": " + data.text);
			socket.broadcast.emit('msg received', data.user, data.text);
			socket.emit('msg received', data.user, data.text);
		})
	});

app.listen(1337, "127.0.0.1");


