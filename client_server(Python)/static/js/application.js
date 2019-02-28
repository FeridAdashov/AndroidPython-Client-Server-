
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var message_received = [];

    //receive details from server
    socket.on('newmessage', function(msg) {
        console.log("Received message" + msg.message);
        //maintain a list of ten messages
        if (message_received.length >= 10){
            message_received.shift()
        }
        
        message_received.push(msg.message);
        message_string = '';
        for (var i = 0; i < message_received.length; i++){
            message_string = message_string + '<p>' + message_received[i].toString() + '</p>';
        }
        $('#log').html(message_string);
    });

});