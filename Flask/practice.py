import datetime
from flask import Flask, jsonify
import time 
import threading

app = Flask(__name__)

current_time = datetime.datetime.now()
print("The current time is:", current_time.time())

@app.route("/")
def data():
    print(current_time)
    return str(current_time)

# Continuously update the data from ADX every 10 seconds
def update_adx_data():
    while True:
        app.config['ADX_DATA'] = data()
        time.sleep(10)

if __name__ == "__main__":
    # Start the thread to continuously update the data from ADX
    update_thread = threading.Thread(target=update_adx_data)
    update_thread.start()

    # Start the Flask app
    app.run()