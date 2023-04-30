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
use `Central_gpt.py` and `gym_rat_arduino.ino`