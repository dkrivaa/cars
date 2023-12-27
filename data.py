import requests
import pandas as pd
import json
import aiohttp
import asyncio

# Getting data according to license plate
def data_license(license):
    # Resource ID's
    resource_id1 = "053cea08-09bc-40ec-8f7a-156f0677aff3"
    resource_id2 = '0866573c-40cd-4ca8-91d2-9dd2d7a492e5'
    resource_id3 = '56063a99-8a3e-4ff4-912e-5966c0279bad'
    resource_id4 = 'bb2355dc-9ec7-4f06-9c3f-3344672171da'
    resource_id = [resource_id1, resource_id2, resource_id3, resource_id4]

    # Specify the filter value for the mispar_rechev column
    mispar_rechev = license

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

    if len(info[0]) > 0:
        degem_nm = info[0][0]['degem_nm']
        degem_cd = info[0][0]['degem_cd']
        shnat_yitzur = info[0][0]['shnat_yitzur']

        # Making list of similar cars - model and production year
        similar_car_license = similar(mispar_rechev, degem_nm, shnat_yitzur)
        print('similar cars: ', len(similar_car_license))

        if shnat_yitzur > 2016 and len(info[2]) > 0:
            kl, owner = calc_for_similar_cars(similar_car_license)

            kl = [value for value in kl if value is not None]
            average_kilometer = (int(sum(kl)/len(kl)))

            owner = [value for value in owner if value is not None]
            average_owner = (int(sum(owner) / len(owner)))

            # # Calculating various comparable variables
            print('Kilometers - this car: ', info[2][0]['kilometer_test_aharon'], 'average similar cars: ', average_kilometer)
            print('owners - this car: ', len(info[3]), 'average similar cars: ', average_owner)

        else:
            average_kilometer = 'No data available'
            average_owner = 'No data available'

            # # Calculating various comparable data
            print('Kilometers - this car: ', 'No data available.', 'average similar cars: ', average_kilometer)
            print('owners - this car: ', 'No data available.', 'average similar cars: ', average_owner)

        # Prices of new cars (same model) according to importers
        price = prices(degem_nm, degem_cd, shnat_yitzur)

    else:
        print("No Data")

    return info[0][0]['shnat_yitzur'], info[2][0]['kilometer_test_aharon'], len(info[3]), price



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

        #return list of license numbers of similar cars
        return similar_car_license

def calc_for_similar_cars(similar_car_license):
    kl = []
    owner = []

    async def fetch_data1(session, semaphore, car_license, resource_id):
        params = {"resource_id": resource_id, "filters": f'{{"mispar_rechev": "{car_license}"}}'}
        api_url = "https://data.gov.il/api/action/datastore_search"

        async with semaphore:
            try:
                async with session.get(api_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        kilometer_test_aharon = int(data['result']['records'][0]['kilometer_test_aharon'])
                        return kilometer_test_aharon
                    else:
                        return None
            except:
                return None

    async def kilometer(similar_car_license):
        resource_id3 = "56063a99-8a3e-4ff4-912e-5966c0279bad"  # Replace with your actual resource ID
        concurrent_requests_limit = 10000  # Set the desired limit

        semaphore = asyncio.Semaphore(concurrent_requests_limit)

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_data1(session, semaphore, car, resource_id3) for car in similar_car_license]
            results = await asyncio.gather(*tasks)

        # results now contains the kilometer_test_aharon values for each car license
        kl.extend(results)

    async def fetch_data2(session, semaphore, car_license, resource_id):
        params = {"resource_id": resource_id, "filters": f'{{"mispar_rechev": "{car_license}"}}'}
        api_url = "https://data.gov.il/api/action/datastore_search"

        async with semaphore:
            try:
                async with session.get(api_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        owners = len(data['result']['records'])
                        return owners
                    else:
                        return None
            except:
                return None


    async def num_of_owners(similar_car_license):
        resource_id4 = 'bb2355dc-9ec7-4f06-9c3f-3344672171da'
        concurrent_requests_limit = 10000  # Set the desired limit

        semaphore = asyncio.Semaphore(concurrent_requests_limit)

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_data2(session, semaphore, car, resource_id4) for car in similar_car_license]
            results = await asyncio.gather(*tasks)

        # results now contains the number of owners values for each car license
        owner.extend(results)


    asyncio.run(kilometer(similar_car_license))
    asyncio.run(num_of_owners(similar_car_license))

    return kl, owner


def prices(degem_nm, degem_cd, shnat_yitzur):
    # Data with prices for new cars as reported by importers
    resource_id = '39f455bf-6db0-4926-859d-017f34eacbcb'

    # Construct the URL with the filter using the params parameter
    params = {"resource_id": resource_id, "filters": f'{{"degem_nm": "{degem_nm}", "degem_cd":{degem_cd}}}'}
    api_url = "https://data.gov.il/api/action/datastore_search"

    # Make the HTTP request
    response = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        data = json.loads(response.text)
        print(data['result']['records'])

        # Create a dictionary where key is shnat_yitzur and value is mehir value
        result_dict = {item['shnat_yitzur']: item['mehir'] for item in data['result']['records']}
        print(result_dict)
        # if result_dict[shnat_yitzur]:
        if len(result_dict) > 0:
            print(result_dict[shnat_yitzur])
        else:
            print('No Data')

        return result_dict[shnat_yitzur]

