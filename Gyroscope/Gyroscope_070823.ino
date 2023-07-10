#include <Arduino_LSM9DS1.h>
#include <ArduinoBLE.h>

float x, y, z;
int plusThreshold = 10, minusThreshold = -10;
int debounceCount = 3;
int upCounter = 0, downCounter = 0;
bool upDetected = false, downDetected = false;
int repCount = 0;
unsigned long lastUpTime = 0, lastDownTime = 0;
unsigned int repDelay = 500; // Minimum time interval between consecutive "Up" or "Down" detections (in milliseconds)

// BLE UUIDs
const char* serviceUUID = "17c73c1a-4bc7-11ed-bdc3-0242ac120001";
const char* repCountUUID = "17c73c1a-4bc7-11ed-bdc3-0242ac120002";

// BLE Objects
BLEService repService(serviceUUID);
BLEIntCharacteristic repCountCharacteristic(repCountUUID, BLERead | BLENotify);

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // BLE Setup
  if (!BLE.begin()) {
    Serial.println("Failed to start BLE!");
    while (1);
  }
  BLE.setLocalName("BLE Rep Counter");
  BLE.setAdvertisedService(repService);
  repService.addCharacteristic(repCountCharacteristic);
  BLE.addService(repService);
  repCountCharacteristic.writeValue(repCount);
  BLE.advertise();
  
  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Gyroscope in degrees/second");
}

void loop() {
  BLEDevice central = BLE.central(); // Check if a central device has connected
  if (central) { // If a central device is connected
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

      // Write the rep count to the BLE characteristic
      repCountCharacteristic.writeValue(repCount);
    }
  }
  delay(100);
}
