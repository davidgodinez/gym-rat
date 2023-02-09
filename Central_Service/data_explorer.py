from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
import pandas as pd


print("Success!")

AAD_TENANT_ID = "f0e7e7ca-b83f-4893-94b4-6f982b62bbc8"
KUSTO_CLUSTER = "https://restarteddataexplorer1.southcentralus.kusto.windows.net"
KUSTO_DATABASE = "restarted-gym-rat"

KCSB = KustoConnectionStringBuilder.with_aad_device_authentication(
    KUSTO_CLUSTER)
KCSB.authority_id = AAD_TENANT_ID


KUSTO_CLIENT = KustoClient(KCSB)
KUSTO_QUERY = "Raspberrypi | take 5"

RESPONSE = KUSTO_CLIENT.execute(KUSTO_DATABASE, KUSTO_QUERY)
print("You got this far!")
df = dataframe_from_result_table(RESPONSE.primary_results[0])
print(df)

