#include <Arduino.h>

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


#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include "arduinoFFT.h" 
#include <math.h> 

// --- Configuration ---
const uint16_t samples = 128; // Must be a power of 2
const double theoreticalSamplingFrequency = 10000.0; 

// --- Global variables for FFT ---
// We'll reuse vReal and vImag for each axis analysis
double vReal[samples];
double vImag[samples];
ArduinoFFT<double> FFT = ArduinoFFT<double>(vReal, vImag, samples, theoreticalSamplingFrequency);

Adafruit_MPU6050 mpu;

// --- Function Declarations ---
void setup(void);
void loop();
void perform_fft(double* data_array, double actual_sampling_rate, double* frequency);
double calculate_sampling_rate(int num_points, long duration_ms);
double calculate_rms(const float* data_array, int num_points);

// ====================================================================
// UTILITY FUNCTIONS
// ====================================================================

double calculate_sampling_rate(int num_points, long duration_ms) {
  if (duration_ms == 0) return 0.0;
  return (double)num_points / (duration_ms / 1000.0); 
}

double calculate_rms(const float* data_array, int num_points) {
    if (num_points == 0) return 0.0;
    
    double sum_of_squares = 0.0;
    
    // NOTE: For true AC vibration RMS, you should detrend (subtract the mean) 
    // before summing the squares. We use the raw data here for the RMS of the total signal.
    for (int i = 0; i < num_points; i++) {
        sum_of_squares += data_array[i] * data_array[i];
    }
    
    return sqrt(sum_of_squares / num_points);
}


// ====================================================================
// FFT IMPLEMENTATION
// ====================================================================
/**
 * @brief Performs detrending and FFT on the provided data_array and finds 
 * the dominant frequency.
 * @param data_array The acceleration data for one axis (e.g., ax, ay, or az).
 * @param actual_sampling_rate The measured sampling rate.
 * @param frequency Pointer to store the calculated dominant frequency.
 */
void perform_fft(double* data_array, double actual_sampling_rate, double* frequency) {
  
  // 1. Calculate Mean (DC Bias)
  double sum = 0.0;
  for (int i = 0; i < samples; i++) {
    sum += data_array[i];
  }
  double mean = sum / samples;

  // 2. Copy detrended data to vReal and zero out vImag
  for (int i = 0; i < samples; i++) {
    vReal[i] = data_array[i] - mean; // Detrending
    vImag[i] = 0.0; 
  }

  // 3. Perform FFT
  FFT.windowing(FFT_WIN_TYP_HAMMING, FFT_FORWARD); 
  FFT.compute(FFT_FORWARD);                          
  FFT.complexToMagnitude();                          

  // 4. Find the peak (dominant) frequency
  double peak_magnitude = 0.0;
  uint16_t peak_index = 0;

  // Start from index 1 to ignore the DC component
  for (uint16_t i = 1; i < samples / 2; i++) { 
    if (vReal[i] > peak_magnitude) {
      peak_magnitude = vReal[i];
      peak_index = i;
    }
  }

  // 5. Calculate the dominant frequency
  *frequency = ((double)peak_index * actual_sampling_rate) / samples;
}


// ====================================================================
// SETUP
// ====================================================================
void setup(void) {
  Wire.begin();
  Wire.setClock(400000); 

  Serial.begin(115200);
  while (!Serial)
    delay(10); 

  Serial.println("MPU6050 3-Axis FFT and RMS Test!");

  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_44_HZ); 

  Serial.println("");
  delay(100);

  setup_wifi();
  client.setServer(mqtt_server, portNumber);
  client.setCallback(callback);  
}

// ====================================================================
// LOOP
// ====================================================================
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  delay(1000);

  sensors_event_t a, g, temp;
  
  // Storage for raw data (float)
  float raw_ax[samples], raw_ay[samples], raw_az[samples];
  
  // Storage for data passed to FFT (double)
  double fft_ax[samples], fft_ay[samples], fft_az[samples];
  
  long startTime = millis();
  
  // --- Data Collection Loop ---
  for (int i = 0; i < samples; i++) {
    mpu.getEvent(&a, &g, &temp);
    raw_ax[i] = a.acceleration.x;
    raw_ay[i] = a.acceleration.y;
    raw_az[i] = a.acceleration.z;
    
    // Copy to double arrays for FFT/detrending prep
    fft_ax[i] = a.acceleration.x;
    fft_ay[i] = a.acceleration.y;
    fft_az[i] = a.acceleration.z;
    
    delayMicroseconds(100); 
  }
  long duration_ms = millis() - startTime;
  
  // --- Calculate Actual Sampling Rate ---
  double actual_sampling_rate = calculate_sampling_rate(samples, duration_ms);
  Serial.println("====================================");
  Serial.print("Data Duration: "); Serial.print(duration_ms); Serial.println(" ms");
  Serial.print("Actual Sampling Rate: "); Serial.print(actual_sampling_rate, 2); Serial.println(" Hz");
  Serial.println("------------------------------------");

  double rms_x, rms_y, rms_z;
  double freq_x, freq_y, freq_z;
  
  Serial.print("device ID: "); Serial.println("myID");

  // --- X-Axis Analysis ---
  rms_x = calculate_rms(raw_ax, samples);
  perform_fft(fft_ax, actual_sampling_rate, &freq_x); 
  Serial.print("X-AXIS | RMS: "); Serial.print(rms_x, 4); Serial.print(" m/s^2 | Freq: "); Serial.print(freq_x, 2); Serial.println(" Hz");

  // --- Y-Axis Analysis ---
  rms_y = calculate_rms(raw_ay, samples);
  perform_fft(fft_ay, actual_sampling_rate, &freq_y);
  Serial.print("Y-AXIS | RMS: "); Serial.print(rms_y, 4); Serial.print(" m/s^2 | Freq: "); Serial.print(freq_y, 2); Serial.println(" Hz");

  // --- Z-Axis Analysis ---
  rms_z = calculate_rms(raw_az, samples);
  perform_fft(fft_az, actual_sampling_rate, &freq_z);
  Serial.print("Z-AXIS | RMS: "); Serial.print(rms_z, 4); Serial.print(" m/s^2 | Freq: "); Serial.print(freq_z, 2); Serial.println(" Hz");
  
  Serial.println("====================================");

  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    
    char tempString[8];

    dtostrf(freq_x, 1, 2, tempString);
    client.publish("esp32_htj/freq_x", tempString);

    dtostrf(freq_y, 1, 2, tempString);
    client.publish("esp32_htj/freq_y", tempString);

    dtostrf(freq_z, 1, 2, tempString);
    client.publish("esp32_htj/freq_z", tempString);

    dtostrf(rms_x, 1, 4, tempString);
    client.publish("esp32_htj/rms_x", tempString);

    dtostrf(rms_y, 1, 4, tempString);
    client.publish("esp32_htj/rms_y", tempString);

    dtostrf(rms_z, 1, 4, tempString);
    client.publish("esp32_htj/rms_z", tempString);

    Serial.println("published...");
  }

  delay(100); 
}