import paho.mqtt.client as mqtt
import socket 
import time
import json
from datetime import datetime

from my_mysql import PyMySQL 


class MyMQTT():
    
    topic_static = "[Sensor]"
    
    def __init__(self,hostname ="",topic= topic_static,loop=False):
        if hostname == "":
            self.hostname = self.get_ip()
        else:
            self.hostname = hostname
        print("[MQTT][Hostname] %s" %hostname)
        self.topic = topic
        self.client= mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.hostname,1883,60)
        self.loop_forever(loop)
    
    #get device's IP
    def get_ip(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255',1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    def on_connect(self,client,userdata,flags,rc):
        print("[MQTT][OnConnect] Connected with result code " + str(rc))

    def on_message(self, client, userdata, msg):
        #print("[MQTT][OnMessage] " + self.topic + " " + str(msg.payload))
        messenger = str(msg.payload)
        mess = messenger[2:-1] #loai bo phan thua cua json khi nhan 
        data = json.loads(mess)
        # "TEMPERATURE" : "27","Humidity" : 30,
        temp = data["TEMPERATURE"]
        humi = data["HUMIDITY"]
        light = data["LIGHT"]
        #light = 0
        #gia tri time : so giay tinh tu năm 1970 den nay : 1680000000
        currentTime = datetime.fromtimestamp(int(data["TIME"]))
        #gui du lieu len mysql
        mysql = PyMySQL()
        mysql.insertData(temp,humi,light,currentTime)
        mysql.close()

    def loop_forever(self, loop):
        if loop:
            self.client.loop_forever()
    
    # publish, subcribe
    def publish(self, message):
        self.client.publish(self.topic, message)

    def subscribe(self):
        self.client.subscribe(self.topic)

    def subscriber(self, topic):
        self.client.subscribe(topic)

