import asyncio
import json
import datetime
from time import sleep
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message
import requests
from bs4 import BeautifulSoup
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

# Connection string taken from iothub device. 
CONNECTION_STRING = "HostName=restartedhub1.azure-devices.net;DeviceId=raspberrypi-1;SharedAccessKey=LisBgX0dsS1HPRvBqJ6N9yxFXX45luiRHJag2G2SF/I="
GYM_ID = 1 # This will be encoded better. For now this works as demo. 
MACHINE_ID = 1 #This will be encoded better. For now this works as demo. 

def get_rep_count():
    try:
        response = requests.get('http://10.0.0.29')
        response.raise_for_status()  # raise an exception if the request was unsuccessful
    except requests.exceptions.RequestException as e:
        print(f"Failed to get rep count: {e}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        rep_count_text = soup.find(string=lambda t: t and 'Rep count:' in t)  # find the text that contains 'Rep count:'
        rep_count = int(rep_count_text.split(': ')[1])  # extract the rep count from the found text
        return rep_count
    except (IndexError, ValueError) as e:
        print(f"Failed to parse rep count: {e}")
        return None

def get_user_id():
    reader = SimpleMFRC522()
    try:
        print("Hold a tag near the reader")
        id, name = reader.read()
        print(f"Tag ID: {id}")
        print(f"Tag Name: {name}")
        return id
    finally:
        GPIO.cleanup()

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
    print('IoT Hub device sending periodic messages, press Ctrl-C to exit')
    print('Connecting to Arduino Nano IoT Peripheral Device...')
    counter = 0
    last_rep_count = -1
    user_id = None
    # Main loop. Get rep count from Arduino over WiFi and send it to Azure IoT Hub
    while True:
        if user_id is None:
            user_id = get_user_id()
            print(f"User ID: {user_id}")
            print("New user detected, waiting for session to start")
            continue
        counter = get_rep_count()
        if counter is not None:
            print(f'Rep count: {counter}')
            # If the rep_count has changed and is greater than 0, send the data
            if counter != last_rep_count and counter > 0:
                telemetry_message = {
                    "gym_id": GYM_ID,
                    "machine_id": MACHINE_ID,
                    "user_id": user_id,
                    "rep_count": counter,
                    "weight": weight(),
                    "reptime": get_time()
                }
                send_telemetry_from_pi(new_messenger, telemetry_message)
                last_rep_count = counter
        sleep(0.5)

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
