// Here does nothing 

/*
  Arduino LSM9DS1 - Simple Accelerometer

  This example reads the acceleration values from the LSM9DS1
  sensor and continuously prints them to the Serial Monitor
  or Serial Plotter.

  The circuit:
  - Arduino Nano 33 BLE Sense

  created 10 Jul 2019
  by Riccardo Rizzo

  This example code is in the public domain.
*/

#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>

BLEService customService("17c73c1a-4bc7-11ed-bdc3-0242ac120002");

// BLEIntCharacteristic CharacteristicX("17c73c1a-4bc7-11ed-bdc3-0242ac120002", BLERead | BLENotify);
BLEIntCharacteristic CharacteristicY("17c73c1a-4bc7-11ed-bdc3-0242ac120002", BLERead | BLENotify);
// BLEIntCharacteristic CharacteristicZ("17c73c1a-4bc7-11ed-bdc3-0242ac120002", BLERead | BLENotify);

int plusThreshold = 30, minusThreshold = -30;


void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Gyroscope in degrees/second");

  // begin initialization
  BLE.begin();

  // set advertised local name and service UUID:
  BLE.setLocalName("BLE");
  BLE.setAdvertisedService(customService);

  // add the characteristic to the service
  // customService.addCharacteristic(CharacteristicX);
  customService.addCharacteristic(CharacteristicY);
  // customService.addCharacteristic(CharacteristicZ);

  // add service
  BLE.addService(customService);

  // set the initial value for the characeristic:
  // CharacteristicX.writeValue(0);
  CharacteristicY.writeValue(0.0);
  // CharacteristicZ.writeValue(0);

  // start advertising
  BLE.advertise();

  Serial.println("BLE LED Peripheral");
  pinMode(LED_BUILTIN, OUTPUT);

  
}

void loop() {
  // char myString ;
   BLEDevice central = BLE.central();
   if (central) {
     Serial.print("Connected to central ");
     Serial.print(central.address());
     digitalWrite(LED_BUILTIN, HIGH);
   }
  // BLE.poll();
   while (central.connected()) {

    float x, y, z;


    if (IMU.gyroscopeAvailable()) {
      IMU.readGyroscope(x, y, z);
      if (y > plusThreshold) {
      CharacteristicY.writeValue(y);
      }
    else if (y < minusThreshold) {
      CharacteristicY.writeValue(1000);
    }

    }
    // if(y > plusThreshold)
    // {
    //   Serial.println("Up");
    //   Serial.println(y);
    //   // CharacteristicY.writeValue(y*1000);
    //   // char myString[] = "Up";
    //   delay(500);
    // }
    // if(y < minusThreshold)
    // {
    //   Serial.println("Down");
    //   Serial.println(y);
    //   // CharacteristicY.writeValue(y*1000);
    //   // char myString[] = "Down";
    //   delay(500);
    // }  

    // CharacteristicY.writeValue(y*1000);
    // CharacteristicX.writeValue(x*100);
    // CharacteristicZ.writeValue(z*100);
  }
}

