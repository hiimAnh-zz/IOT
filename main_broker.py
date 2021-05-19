
from my_mysql import PyMySQL
from my_mqtt import MyMQTT
from random import randint
import time

pymysql = PyMySQL()
pymysql.createTable()



mq = MyMQTT()
mq.subscriber("Sensor") #topic mqtt : Sensor
mq.loop_forever(True)


