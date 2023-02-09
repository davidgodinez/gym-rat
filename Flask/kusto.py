from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
import pandas as pd
import json




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
    return df3

get_data2()
# def get_client():
#     kcsb = KustoConnectionStringBuilder.with_aad_device_authentication("https://restarteddataexplorer1.southcentralus.kusto.windows.net")
#     client = KustoClient(kcsb)
#     return client
    
# client = get_client()

# def get_data():
#     query = ".show databases"
#     results = client.execute(database="restarted-gym-rat", query=query)
#     return results.primary_results[0]



