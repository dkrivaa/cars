import pandas as pd
import requests
import json

url = 'https://data.gov.il/api/3/action/datastore_search'
resource_id = '39f455bf-6db0-4926-859d-017f34eacbcb'

# Make a GET request to the API endpoint
params = {'resource_id': resource_id}
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON
    data = json.loads(response.text)

    # Extract the count of records
    count = data["result"]["total"]

limit = 100000  # Number of rows to retrieve per request

# Calculate the total number of requests needed
total_rows = count
total_requests = (total_rows // limit) + 1

# Initialize an empty list to store the results
results = []

# Make multiple requests to retrieve all the rows
for offset in range(0, total_requests * limit, limit):
    params = {'resource_id': resource_id, 'limit': limit, 'offset': offset}
    response = requests.get(url, params=params).json()
    data = response['result']['records']
    results.extend(data)

# Create a DataFrame from the combined results
df = pd.DataFrame(results)

print(len(df.loc[(df['degem_nm'] == '117.343') & (df['degem_cd'] == 54) & (df['shnat_yitzur'] == 2017)]))

# # Average prices per importer by year
# for importer in df['semel_yevuan'].unique():
#     df_temp = df[df['semel_yevuan'] == importer]
#     prices = df_temp.groupby('shnat_yitzur')['mehir'].mean()
#     change = ((prices.iloc[-1]/prices.iloc[0])**(1/len(prices))-1)*100
#     # print(df.loc[df['semel_yevuan'] == importer, 'shem_yevuan'].iloc[0], prices, change)
#
# # Average prices per model by year
# for car in df['degem_nm'].unique():
#     df_temp = df[df['degem_nm'] == car]
#     prices = df_temp.groupby('shnat_yitzur')['mehir'].mean()
#     change = ((prices.iloc[-1]/prices.iloc[0])**(1/len(prices))-1)*100
#     if prices.index[-1] == 2023:
#         print(car, df.loc[df['degem_nm'] == car, 'kinuy_mishari'].iloc[0], prices, change)
