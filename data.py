import requests
import pandas as pd
import json

# Getting data according to license plate
def data_license():
    # Resource ID's
    resource_id1 = "053cea08-09bc-40ec-8f7a-156f0677aff3"
    resource_id2 = '0866573c-40cd-4ca8-91d2-9dd2d7a492e5'
    resource_id3 = '56063a99-8a3e-4ff4-912e-5966c0279bad'
    resource_id4 = 'bb2355dc-9ec7-4f06-9c3f-3344672171da'
    resource_id = [resource_id1, resource_id2, resource_id3, resource_id4]

    # Specify the filter value for the mispar_rechev column
    mispar_rechev_value = 1000039

    info = []
    for resource in resource_id:
        # Construct the URL with the filter
        api_url = f"https://data.gov.il/api/action/datastore_search?resource_id={resource}&filters=%7B%22mispar_rechev%22%3A%20{mispar_rechev_value}%7D"

        # Make the HTTP request
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            data = json.loads(response.text)
            print(data['result']['records'])
            info.append(data['result']['records'])

    print(info)


def similar():
    resource_id1 = "053cea08-09bc-40ec-8f7a-156f0677aff3"
    # Specify the filter value for the degem_nm column
    degem_nm = '92A'
    # Construct the URL with the filter using the params parameter
    params = {"resource_id": resource_id1, "filters": f'{{"degem_nm": "{degem_nm}", "shnat_yitzur":{2017}}}'}
    api_url = "https://data.gov.il/api/action/datastore_search"

    # Make the HTTP request
    response = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        data = json.loads(response.text)
        print(data['result']['records'])


