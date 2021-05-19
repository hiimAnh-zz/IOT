#include "MyTime.h"
#include "MyWifi.h"
#include "AppDebug.h"
#include "Sensor_DHT.h"
#include "MyJson.h"
#include "MyMQTT.h"

char* ssid = "BS Long";
char* password = "12345679";

IPAddress mqttServer(192,168,1,112);
char* mqttTopic = "Sensor";
MyMQTT mqtt = MyMQTT(MyWifi.espClient,mqttServer);

void setup(){
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  MyWifi.connect(ssid,password);
  MyTime.configTimeDate();
  mqtt.connect();
}
void loop(){
  mqtt.publish(mqttTopic, "hello");
  delay(2000);
}
