#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme; // I2C

#include <WiFi.h>
#include <PubSubClient.h>

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

  setup_wifi();
  client.setServer(mqtt_server, portNumber);
  client.setCallback(callback);

  Serial.println(F("BME280 test"));


  unsigned status;
  status = bme.begin(0x76);  
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring, address, sensor ID!");
    Serial.print("SensorID was: 0x"); Serial.println(bme.sensorID(),16);
    Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
    Serial.print("   ID of 0x56-0x58 represents a BMP 280,\n");
    Serial.print("        ID of 0x60 represents a BME 280.\n");
    Serial.print("        ID of 0x61 represents a BME 680.\n");
    while (1) delay(10);
  }

  Serial.println("-- Default Test --");

  Serial.println();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  delay(1000);

  t = bme.readTemperature();
  h = bme.readHumidity();

  Serial.print("device ID: "); Serial.println("myID");

  Serial.print("Temperature = ");
  Serial.print(t);
  Serial.println(" C");

  Serial.print("Pressure = ");

  Serial.print(bme.readPressure() / 100.0F);
  Serial.println(" hPa");

  Serial.print("Approx. Altitude = ");
  Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));
  Serial.println(" m");

  Serial.print("Humidity = ");
  Serial.print(h);
  Serial.println(" %");

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