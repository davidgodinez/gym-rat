from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
import pandas as pd
import json
from kusto import get_data2
from flask import Flask, jsonify
import threading
import time


app = Flask(__name__)


AAD_TENANT_ID = "f0e7e7ca-b83f-4893-94b4-6f982b62bbc8"
KUSTO_CLUSTER = "https://restarteddataexplorer1.southcentralus.kusto.windows.net"
KUSTO_DATABASE = "restarted-gym-rat"
KCSB = KustoConnectionStringBuilder.with_aad_device_authentication(
    KUSTO_CLUSTER)
KCSB.authority_id = AAD_TENANT_ID
KUSTO_CLIENT = KustoClient(KCSB)
KUSTO_QUERY = "Raspberrypi | sort by reptime desc| take 1"
RESPONSE = KUSTO_CLIENT.execute(KUSTO_DATABASE, KUSTO_QUERY)

def get_data2():
    df = dataframe_from_result_table(RESPONSE.primary_results[0])
    df2 = pd.DataFrame.to_json(df, orient="records")
    data = json.loads(df2)
    df3 = json.dumps(data)
    print(df3)
    return df3



@app.route("/data")
def get_adx_data():
    return get_data2()

# Continuously update the data from ADX every 10 seconds
def update_adx_data():
    while True:
        app.config['ADX_DATA'] = get_data2()
        time.sleep(10)

if __name__ == "__main__":
    # Start the thread to continuously update the data from ADX
    update_thread = threading.Thread(target=update_adx_data)
    update_thread.start()

    # Start the Flask app
    app.run()
