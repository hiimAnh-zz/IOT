const express = require('express');
const config = require('./config.js');
const data = require('./data.js');
const mqtt = require('mqtt');
const mysql = require('mysql');
const { Socket } = require('dgram');


//APP
const app = express();
app.use(express.static("views"));

app.get('/', function(require, response) {
    response.sendFile('views/home.html', { root : __dirname});
});
var server = require("http").createServer(app).listen(config.app.port, function(){
    console.log("[Server] Running on http://localhost:3000");
}) ;

var con = mysql.createConnection({
    host: config.db.host,
    user: config.db.user,
    password: config.db.password,
    database: config.db.database
});

con.connect(function(err) {
    if (err) throw err;
    console.log("[MySQL] Connected!");
});

//MQTT
const mqtt_server = config.mqtt.server;
var mqtt_client = mqtt.connect(mqtt_server);

mqtt_client.on("connect", function () {
    console.log("[MQTT][Connect] Connected to MQTT server!");
    mqtt_client.subscribe('Sensors');
    mqtt_client.subscribe('Feedback/button');
    console.log("[MQTT][Subscriber] Topic: Feedback/button");
});

mqtt_client.on("message", function(topic, message){
    if(topic.includes("Feedback/button")){
        console.log("[MQTT][Message] Feedback:",topic,message.toString());
        io.sockets.emit('button', message.toString()); 
    }
});

//SOCKETIO
const io = require("socket.io")(server);

setInterval(function () {
    updateStatus();

}, config.db.timeRefresh);

console.log("[Socket] connected!");
function updateStatus() {
    //select last row
    var sql = "SELECT * FROM ( SELECT * FROM sensors ORDER BY id DESC LIMIT 1) sub ORDER BY id ASC";
    con.query(sql, function (err, res) {
        if (err) throw err;
        io.sockets.emit("status", JSON.stringify({"temp": res[0].temperature, "humi": res[0].humidity, "light": res[0].light,"time":res[0].time}));
        //console.log(JSON.stringify({"time":res[0].time}));
    });  
}
//SOCKET IO Control
io.on("connection", function (socket) {
    socket.on('button', function (data) {
        console.log("[Socket][On]", data.button, data.value);
        mqtt_client.publish("Control", 
	JSON.stringify({"button": data.button, "value": data.value}));
    });
    socket.on('buzzer', function (data) {
        console.log("[Socket][On] Buzzer:", data);
        mqtt_client.publish("Control/buzzer", data);
    });
});