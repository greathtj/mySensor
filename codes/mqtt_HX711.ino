#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>

//===================================================
const char* ssid = "MYSSID";
const char* password = "MYPASS";
const char* mqtt_server = "MYMQTTSERVER";
// const char* my_mqtt_id = "esp32_htj";
// const char* my_subscribe = "esp32_htj/output";
// const char* publish_t = "esp32_htj/temperature";
// const char* publish_h = "esp32_htj/humidity";
const int portNumber = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 32;
const int LOADCELL_SCK_PIN = 33;

HX711 scale;

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("esp32_htj")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("esp32_htj/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  delay(1000);

  // scale.set_scale(2280.f);
  scale.set_scale(218.f);
  scale.tare();	  

  setup_wifi();
  client.setServer(mqtt_server, portNumber);
  client.setCallback(callback);  
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  delay(1000);

  float reading;
  if (scale.is_ready()) {
    reading = scale.get_units(10);
    Serial.print("device ID: "); Serial.println("myID");
    Serial.print("HX711 reading: ");
    Serial.println(reading);
  } else {
    Serial.println("HX711 not found.");
  }

  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    
    char tempString[8];
    dtostrf(reading, 1, 2, tempString);
    client.publish("esp32_htj/weight", tempString);

    Serial.println("published...");
  }  

  delay(200);
}