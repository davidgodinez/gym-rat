# Gym-rat

Gym Rat is my envisioning of a smarter gym. This means, in no uncertain terms, having the tasks that can be automated left to the computers so that you can focus on what matters, getting in shape and staying in shape. Gym rat is the defacto solution to having your workout logs automated for you, i.e having your machines take a note of your reps, sets, and workouts for your gym session. This data (in conjunction with devices such as the apple watch which measures heartrate, etc) can then be used for very granular insights into your workout sessions. The data can be used in machine learning models and neural nets for forecasting future strength levels, weight, and overall indicators of health. It is a very powerful tool.

This README will be used to help you get started on setting up the arduinos, rasperrypi and overall environment to get going.

Install Gyroscope.ino on your arduino using the web editor or install IDE on your computer and run Central.py from your raspberry pi after you have created a virtual environment and pip install requirements.txt. My workflow involves ssh-ing into the raspberry pi from my desktop. This allows me to use vscode and simply copy over any modified files to the raspberry pi using the `scp` command. 

`scp path/to/Central.py pi@11.1.1.11:/home/pi/`

From there, place your arduino atop some weights in the gym and stream to your raspberry pi and azure directly. 

I am currently working on setting up the database end. This data will be stored in a data warehouse and further analyzed. It will all update your ios/android app in real time.

## For interacting with data explorer

Create Gymrat database
create table and table mapping copying text from `initial_queries.kql`.

Enjoy :)

Updated scripts: 
use `Central_071523_iot.py` and `Gyroscope_071523.ino`


## Cloud Architecture 

To run the terraform script, you can type `terraform plan` and `terraform apply`. This will create the necessary resources for you to run the project.

## Hardware

1. Power Connections: Connect the HV (High Voltage) pin of the level converter to the 5V pin of your Arduino Nano 33 IoT. Connect the LV (Low Voltage) pin of the converter to the 3.3V pin of the Arduino.

2. Ground Connection: Connect the GND pin of the level converter to the GND pin of the Arduino. Also, connect the GND pin of the Arduino to the GND pin of the HC-SR04 sensor.

3. Sensor Power: Connect the VCC pin of the HC-SR04 sensor to the 5V pin of the Arduino.

4. Sensor Trigger Connection: Connect the Trig pin of the HC-SR04 sensor to one of the HV1-HVx pins on the level converter. Connect the corresponding LV pin (LV1 if you used HV1, LV2 if you used HV2, etc.) to the digital pin on the Arduino that you're using for the trigger signal in your code.

5. Sensor Echo Connection: Connect the Echo pin of the HC-SR04 sensor to another one of the HV1-HVx pins on the level converter. Connect the corresponding LV pin to the digital pin on the Arduino that you're using for the echo signal in your code.

In summary:

HC-SR04 VCC -> Arduino 5V
HC-SR04 GND -> Arduino GND
HC-SR04 Trig -> Logic level converter HV pin
HC-SR04 Echo -> Logic level converter HV pin
Logic level converter LV (corresponding to Trig) -> Arduino Trig pin
Logic level converter LV (corresponding to Echo) -> Arduino Echo pin
Logic level converter GND -> Arduino GND
Logic level converter HV -> Arduino 5V
Logic level converter LV -> Arduino 3.3V
Please note that the HV and LV labels may vary depending on the model of your level converter. HV stands for High Voltage, which in this case is the 5V side (HC-SR04 side). LV stands for Low Voltage, which in this case is the 3.3V side (Arduino side).

Remember to double-check all connections before powering on your Arduino to prevent any damage. Once you've made these connections, your HC-SR04 should be able to communicate with your Arduino Nano 33 IoT without any issues.

Also, be aware that the Arduino Nano 33 IoT operates at 3.3V. The 5V pin on the board is not connected by default. If you want to use the 5V pin to power your sensor, you will need to close the VUSB jumper on the back of the board by soldering a small blob of solder across the two pads of the jumper. Be sure to follow all safety precautions when soldering.