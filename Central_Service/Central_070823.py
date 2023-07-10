# -*- coding: utf-8 -*-
"""
  Gyroscope Arduino Nano Nano BLE Control Central Device
"""

import asyncio
import json
import datetime
from time import sleep
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message
from bleak import BleakClient, BleakScanner

# These values have been randomly generated - they must match between the Central and Peripheral devices
REP_COUNTER_UUID = "17c73c1a-4bc7-11ed-bdc3-0242ac120002"

# Connection string taken from iothub device. 
CONNECTION_STRING = "HostName=restartedhub1.azure-devices.net;DeviceId=raspberrypi-1;SharedAccessKey=LisBgX0dsS1HPRvBqJ6N9yxFXX45luiRHJag2G2SF/I="
GYM_ID = 1 # This will be encoded better. For now this works as demo. 
MACHINE_ID = 1 #This will be encoded better. For now this works as demo. 

def user():
    username = 1
    return username

def weight():
    weight_id = 1
    return weight_id

def get_time():
    now = datetime.datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
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
    print('Looking for BLE Rep Counter Peripheral Device...')

    # Find device
    found = False
    devices = await BleakScanner.discover(timeout=20.0)
    for d in devices:       
        if d.name is not None and 'BLE Rep Counter' in d.name:
            print('Found BLE Peripheral')
            found = True
            async with BleakClient(d.address) as client:
                try:
                    print(f'Connected to {d.address}')
                    print("Services:")
                    for service in client.services:
                        print(service)

                    # Also print out the characteristics of each service
                    for service in client.services:
                        print(f"Service: {service.uuid}")
                        for char in service.characteristics:
                            print(f"\tCharacteristic: {char.uuid}")

                    counter = 0
                    # Main loop. Listening for arduino messages and loggin in counter variable. 
                    while True:
                        val = bytes(await client.read_gatt_char(REP_COUNTER_UUID))
                        if val:
                            counter = int.from_bytes(val, byteorder='little')
                            print(f'Rep count: {counter}')
                            telemetry_message = {
                                "gym_id": GYM_ID,
                                "machine_id": MACHINE_ID,
                                "user_id": user(),
                                "rep_count": counter,
                                "weight": weight(),
                                "reptime": get_time()
                            }
                            send_telemetry_from_pi(new_messenger, telemetry_message)
                        sleep(0.5)
                except Exception as e:
                    print(f"Exception occurred: {e}")

                    
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
