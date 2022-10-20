# -*- coding: utf-8 -*-
"""
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
"""

from codecs import utf_8_decode
import logging
import asyncio
import platform
import ast
from time import sleep
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message
from bleak import BleakClient, BleakScanner, discover

# These values have been randomly generated - they must match between the Central and Peripheral devices
# Any changes you make here must be suitably made in the Arduino program as well

Y_AXIS_UUID = "17c73c1a-4bc7-11ed-bdc3-0242ac120002"
CONNECTION_STRING = "HostName=davidiothub2.azure-devices.net;DeviceId=raspberrypi;SharedAccessKey=yxztDdIOVP3vWCfpyF3G7N1KljKhWFEEkWuYrlyl0Kg="



def iothub_client_init():
    # Create an IoT Hub client
    new_messenger = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return new_messenger


async def run():
    new_messenger = iothub_client_init()
    print('BLE Peripheral Central Service')
    print('Looking for BLE Sense Peripheral Device...')
    print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

    found = False
    devices = await BleakScanner.discover()
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
                    #TODO include logic that defaulst back to 0 after a value has been counted. 
                    # I.e if still 'up' it won't continue counting but go back to 0
                    else:
                        counter= counter + 1
                        print(counter)
                        print(f'sending message {counter}')
                        first = 'Raspberry Pi'
                        second = str(counter)
                        MSG_TXT = '{{"From": {first},"Message": {second}}}'

                        msg_txt_formatted = MSG_TXT.format(first=first, second=second)
                        counter_message = Message(msg_txt_formatted)
                        print(counter_message)
                        new_messenger.send_message(counter_message)
                        print('message successfully sent! :`)')
                    sleep(0.5)

    if not found:
        print('Could not find Arduino Nano 33 BLE Sense Peripheral')

# define as main():                     
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    print('\nReceived Keyboard Interrupt')
finally:
    print('Program finished')


        
