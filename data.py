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
    mispar_rechev = 1000611

    info = []
    for resource in resource_id:
        # Construct the URL with the filter
        api_url = f"https://data.gov.il/api/action/datastore_search?resource_id={resource}&filters=%7B%22mispar_rechev%22%3A%20{mispar_rechev}%7D"

        # Make the HTTP request
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            data = json.loads(response.text)
            print(data['result']['records'])
            info.append(data['result']['records'])

    degem_nm = info[0][0]['degem_nm']
    shnat_yitzur = info[0][0]['shnat_yitzur']

    print(degem_nm, shnat_yitzur)
    similar(mispar_rechev, degem_nm, shnat_yitzur)


def similar(mispar_rechev, degem_nm, shnat_yitzur):
    resource_id1 = "053cea08-09bc-40ec-8f7a-156f0677aff3"
    # Specify the filter value for the degem_nm column
    degem_nm = degem_nm
    year = shnat_yitzur
    # Construct the URL with the filter using the params parameter
    params = {"resource_id": resource_id1, "filters": f'{{"degem_nm": "{degem_nm}", "shnat_yitzur":{year}}}'}
    api_url = "https://data.gov.il/api/action/datastore_search"

    # Make the HTTP request
    response = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        data = json.loads(response.text)
        similar_car_license = [d['mispar_rechev'] for d in data['result']['records'] if 'mispar_rechev' in d]
        similar_car_license.remove(mispar_rechev)
        print(len(similar_car_license))



