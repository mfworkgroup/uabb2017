var spawn = require('child_process').spawn;
var fs = require('fs');
var os = require('os');
var readline = require('readline');
var CryptoJS = require('crypto-js');
var mqtt = require('mqtt');
var request = require('request');
var crypto = require('crypto');


var productKey = 'n60O6k3LPyA';
var deviceName = 'rasptest01';
var deviceSecret = 'Jf5Dg8lHF43Q5NzuWhXOJpHlqqfpQWOw';
var targetServer = "tcp://" + productKey + ".iot-as-mqtt.cn-shanghai.aliyuncs.com:1883";
var port = 1883;
var host = productKey + '.iot-as-mqtt.cn-shanghai.aliyuncs.com';



var clientId = "testing123";
var timestamp = new Date().getTime();

var mqttClientId = clientId + "|securemode=3,signmethod=hmacsha1,timestamp=" + timestamp + "|";
var mqttUsername = deviceName + "&" + productKey;

var content = 'clientId' + clientId + 'deviceName' + deviceName + 'productKey' + productKey + 'timestamp' + timestamp
//var hash = CryptoJS.HmacSHA1(deviceSecret, content).toString();
var mqttPassword = crypto.createHmac('sha1', deviceSecret).update(content).digest('hex');

console.log(mqttClientId);
console.log(mqttUsername);
console.log(mqttPassword);
console.log(content);

var tsl_options = {
    port: port,
    host: host,
    rejectUnauthorized: false,
    keepalive: 100,
    clientId: mqttClientId,
    username: mqttUsername,
    password: mqttPassword
};



var client= mqtt.connect(targetServer,tsl_options);

client.on('connect', function () {
    console.log('connected.....');
    client.subscribe('#');
    client.publish('app2dev/', 'Hello mqtt');
});

//client.subscribe('test', {qos:1});//订阅主题为ｔｅｓｔ的消息

client.on('message', function (topic, message) {
    console.log(message.toString());
});

//var tail = spawn("tail", ["-f", "-n", "-1", fileName]);

//tail.stdout.on("data", function (data) {
//    console.log(data.toString('utf-8'));
//});

/*
fs.open(fileName, 'a+', function(error, fd){
    var buffer;
    var remainder = null;


    fs.watchFile(fileName, {
        persistent: true,
        interval: 1000
    }, function(curr, prev) {
        console.log("change");
        if(curr.mtime > prev.mtime) {
            var tail = spawn("tail", ["-n 1", fileName]);

            tail.stdout.on("data", function (data) {
               console.log(data.toString('utf-8'));
            });
            //fs.readFile(fileName, 'utf-8',function(err, data) {
            //    if (err) {
            //        console.log("error");
            //    } else {
            //        var lines = data.split("\n");
            //        console.log(lines[lines.length-1]);
            //    }
            //});


            } else {
            console.log('文件读取错误');
        }

    });
});
*/

/*fs.watchFile(fileName, {
    persistent: true,
    interval: 1000
}, function(curr, prev) {
    console.log('the current mtime is: ' + curr.mtime);
    console.log('the previous mtime was: ' + prev.mtime);
    if(curr.mtime > prev.mtime){
        //文件内容有变化，那么通知相应的进程可以执行相关操作。例如读物文件写入数据库等
        console.log("if");
        console.log(curr);
        console.log(prev);

        var buffer = new Buffer(curr.size - prev.size);

        fs.read(fileName, buffer, 0, (curr.size - prev.size), prev.size, function(err, bytesRead, buffer){
            console.log(buffer.toString());
        });

    } else {
        //console.log('curr.mtime<=prev.mtime');
        console.log("else");
    }

});
*/

console.log("hi");