#include <Arduino_LSM9DS1.h>
#include <ArduinoBLE.h>

float x, y, z;
int plusThreshold = 30, minusThreshold = -30;
unsigned long debounceTime = 200;
unsigned long repDelay = 1000;
unsigned long lastUpTime = 0;
unsigned long lastDownTime = 0;
bool upDone = false;
int repCount = 0;

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
  BLEDevice central = BLE.central();
  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
    while (central.connected()) {
      if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(x, y, z);

        if (y > plusThreshold && !upDone && millis() - lastDownTime > debounceTime) {
          upDone = true;
          lastUpTime = millis();
          Serial.println("Up");
        }

        if (y < minusThreshold && upDone && millis() - lastUpTime > debounceTime) {
          upDone = false;
          repCount++;
          lastDownTime = millis();
          Serial.print("Rep count: ");
          Serial.println(repCount);
          repCountCharacteristic.writeValue(repCount);
        }
      }
    }
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}
