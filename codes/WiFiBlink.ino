#include <WiFi.h>

void setup() {
    Serial.begin(115200);
    pinMode(2, OUTPUT);
    Serial.println("Starting ESP32 GUI test!");
    // Replace with user-entered credentials
    // WiFi.begin("SSID", "PASSWORD");
}

void loop() {
    digitalWrite(2, HIGH);  // Turn the LED on
    delay(200);
    digitalWrite(2, LOW);   // Turn the LED off
    delay(200);
}