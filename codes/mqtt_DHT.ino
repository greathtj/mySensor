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

#include "DHT.h"
#define DHTPIN 32
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

float t, h;

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
  dht.begin();

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

  h = dht.readHumidity();
  t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print("device ID: "); Serial.println("myID");

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("C "));
  Serial.println();

  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    
    char tempString[8];
    dtostrf(t, 1, 2, tempString);
    client.publish("esp32_htj/temperature", tempString);

    char humString[8];
    dtostrf(h, 1, 2, humString);
    client.publish("esp32_htj/humidity", humString);

    Serial.println("published...");
  }  
}