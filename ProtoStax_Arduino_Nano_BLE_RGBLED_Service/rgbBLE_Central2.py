# -*- coding: utf-8 -*-
"""
/******************************************************************* 

  Gyroscope Arduino Nano Nano BLE Control Central Device

  This is the main file for receiving data from Arduino Nano BLE. 

  This is a example sketch for controlling the RGB LED on an 
  Arduino Nano 33 BLE Sense with Bluetooth over Python  
   
  Items used:
    -Arduino Nano 33 BLE Sense
    -Raspbery Pi 
  
  The Nano publishes a Bluetooth LE Client profile with Characteristics Gyroscope Axis Y. Y is used because we are measuring
  upward movement. 

  This program counts the number of reps a person does at a specific machine at the gym and streams the data to Azure IoT.
  From there the data is streamed back to an app on the user's phone where they can have a permanent and accurate log of 
  their workout. 
  
  The Red, Green and Blue colors of the onboard RGB LED can only be turned on or off. 
  It is not possible to use PWM to mix colors, unfortunately, based on how the Arduino 
  Nano BLE Sense board is configured.
  
  We write a value of 1 to turn on a color and 0 to turn it off. The user inputs 
  a string that can contain r,g,b (or any combination) and those colors will be toggled. 

  The Arduino Nano 33 BLE Sense is chockful of other sensors - you can similarly expose 
  those sensors data as Characteristics
 
  Written by Sridhar Rajagopal for ProtoStax
  BSD license. All text above must be included in any redistribution
 */
"""


from codecs import utf_8_decode
import logging
import asyncio
import platform
import ast
from time import sleep
from bleak import BleakClient, BleakScanner, discover

# These values have been randomly generated - they must match between the Central and Peripheral devices
# Any changes you make here must be suitably made in the Arduino program as well

# X_AXIS_UUID = "17c73c1a-4bc7-11ed-bdc3-0242ac120002"
Y_AXIS_UUID = "17c73c1a-4bc7-11ed-bdc3-0242ac120002"
# Z_AXIS_UUID = "17c73c1a-4bc7-11ed-bdc3-0242ac120002"


async def run():
    print('BLE Peripheral Central Service')
    print('Looking for BLE Sense Peripheral Device...')

    found = False
    devices = await discover()
    for d in devices:       
        if 'BLE'in d.name:
            print('Found BLE Peripheral')
            found = True
            async with BleakClient(d.address) as client:
                print("Services")
                for service in client.services:
                    print(service)
                print(f'Connected to {d.address}')
                counter = 0
                while True:
                    val = bytes(await client.read_gatt_char(Y_AXIS_UUID))
                    # print(val)
                    val1 = str(val)
                    if val1 == str(b'\xe8\x03\x00\x00') or val1 == str(b'\x00\x00\x00\x00'):
                        print('None')
                    # elif val1 == str(b'\x00\x00\x00\x00'):
                    #     print('None')
                    else:
                        # print(bytes(val1,encoding='utf-8'))
                        
                        # for i in range(len(val)):
                        #     print(ord(val1[i]))
                        counter= counter + 1
                        print(counter)
                    sleep(0.5)

    if not found:
        print('Could not find Arduino Nano 33 BLE Sense Peripheral')

                    
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    print('\nReceived Keyboard Interrupt')
finally:
    print('Program finished')
        
