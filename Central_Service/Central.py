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

import asyncio
import json
import datetime
from time import sleep
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message
from bleak import BleakClient, BleakScanner

# These values have been randomly generated - they must match between the Central and Peripheral devices
# Any changes you make here must be suitably made in the Arduino program as well
Y_AXIS_UUID = "17c73c1a-4bc7-11ed-bdc3-0242ac120002"

# Connection string taken from iothub device. 
CONNECTION_STRING = "HostName=davidsiothub1.azure-devices.net;DeviceId=raspberrypi;SharedAccessKey=z6dU94G4frZoL9+GSf+PNOtyGp8UG2ExFm0zcm7GTnU="
GYM_ID = 1 # This will be encoded better. For now this works as demo. 
MACHINE_ID = 1 #This will be encoded better. For now this works as demo. 

# TO DO

def user():
    # This will take the input from the RFID tag and return the person's username or userID which will all be linked in database :D 
    username = 1
    return username

def weight():
    # This will take the input from second arduino's relative position to calculate weight in lbs
    weight_id = 1
    return weight_id

def get_time():
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def iothub_client_init():
    # Create an IoT Hub client
    new_messenger = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return new_messenger

def send_telemetry_from_pi(new_messenger,telemetry_msg):
    msg = Message(json.dumps(telemetry_msg))
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    print(msg)
    print("Sent message")
    new_messenger.send_message(msg)


async def run():
    new_messenger = iothub_client_init()
    print('BLE Peripheral Central Service')
    print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
    print('Looking for BLE Sense Peripheral Device...')

    # Find device
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

                # Main loop. Listening for arduino messages and loggin in counter variable. 
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
                        # first = 'Raspberry Pi'
                        # second = str(counter)
                        date_time = str(datetime.datetime.now())
                        telemetry_message = {"gym_id": GYM_ID, "machine_id": MACHINE_ID, "user_id": user(), "rep_count": counter, "weight": weight(), "reptime": get_time()}
                        send_telemetry_from_pi(new_messenger, telemetry_message)
                        print('message successfully sent!')
                    sleep(0.5)

    if not found:
        print('Could not find Arduino Nano 33 BLE Sense Peripheral')

def main():                     
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        print('\nReceived Keyboard Interrupt')
    finally:
        print('Program finished')


if __name__ == '__main__':
    main()
