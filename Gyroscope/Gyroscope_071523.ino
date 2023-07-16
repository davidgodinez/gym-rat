#include <Arduino_LSM6DS3.h>
#include <SPI.h>
#include <WiFiNINA.h>

float x, y, z;
int plusThreshold = 10, minusThreshold = -10;
int debounceCount = 3;
int upCounter = 0, downCounter = 0;
bool upDetected = false, downDetected = false;
int repCount = 0;
unsigned long lastUpTime = 0, lastDownTime = 0;
unsigned int repDelay = 500; // Minimum time interval between consecutive "Up" or "Down" detections (in milliseconds)

char ssid[] = "Godinez";     // your network SSID (name)
char pass[] = "Godinezfamily123";    // your network password

int status = WL_IDLE_STATUS;
WiFiServer server(80);

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // WiFi Setup
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    while (1);
  }

  String fv = WiFi.firmwareVersion();
  if (fv < "1.0.0") {
    Serial.println("Please upgrade the firmware");
  }

  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
  }

  // start the server:
  server.begin();

  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Gyroscope in degrees/second");
}

void loop() {
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);
  }

  if (y > plusThreshold) {
    upCounter++;
    downCounter = 0;
  } else if (y < minusThreshold) {
    downCounter++;
    upCounter = 0;
  } else {
    upCounter = 0;
    downCounter = 0;
  }

  if (upCounter >= debounceCount && !upDetected && (millis() - lastUpTime) > repDelay) {
    upDetected = true;
    lastUpTime = millis();
    Serial.println("Up");
  }

  if (downCounter >= debounceCount && !downDetected && (millis() - lastDownTime) > repDelay) {
    downDetected = true;
    lastDownTime = millis();
    Serial.println("Down");
  }

  // Only count a rep when "Up" is detected first and then "Down"
  if (upDetected && downDetected) {
    // Increment rep count and display it only on the "Down" movement
    repCount++;
    Serial.print("Rep count: ");
    Serial.println(repCount);

    // Reset both the upDetected and downDetected flags after incrementing the rep count
    upDetected = false;
    downDetected = false;
  }

  // listen for incoming clients
  WiFiClient client = server.available();

  if (client) {
    Serial.println("new client");
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (c == '\n' && currentLineIsBlank) {
          // send a standard http response header
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println("Connection: close");
          client.println("Refresh: 5");
          client.println();
          client.println("<!DOCTYPE HTML>");
          client.println("<html>");
          client.print("Rep count: ");
          client.println(repCount);
          client.println("</html>");
          break;
        }
        if (c == '\n') {
          currentLineIsBlank = true;
        } else if (c != '\r') {
          currentLineIsBlank = false;
        }
      }
    }
    delay(1);
    client.stop();
    Serial.println("client disconnected");
  }
  delay(100);
}
