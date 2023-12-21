import pandas as pd
import requests
import json


def owner_data():
    url = 'https://data.gov.il/api/3/action/datastore_search'
    resource_id = 'bb2355dc-9ec7-4f06-9c3f-3344672171da'

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

    # Convert the 'date_column' to datetime
    df['baalut_dt'] = pd.to_datetime(df['baalut_dt'], format='%Y%m')

    # Create new columns for year and month
    df['baalut_year'] = df['baalut_dt'].dt.year
    df['baalut_month'] = df['baalut_dt'].dt.month

    df.to_csv('owner.csv', index=False)


def new_cars_by_year_owner():
    df = pd.read_csv('owner.csv')

    # Convert 'baalut_dt' to datetime format
    df['baalut_dt'] = pd.to_datetime(df['baalut_dt'])
    # Get the row with the lowest 'baalut_dt' date value for each 'mispar_rechev' = new cars
    df_first_owner = df.loc[df.groupby('mispar_rechev')['baalut_dt'].idxmin()]

    annual_data = []
    for year in sorted(df_first_owner['baalut_dt'].dt.year.unique()):
        # print(year, len(df_first_owner.loc[df_first_owner['baalut_year'] == year]))
        for owner in df_first_owner['baalut'].unique():
            # print(owner, len(df_first_owner.loc[(df_first_owner['baalut_year'] == year) & (df_first_owner['baalut'] == owner)]))
            row = {'year': year, 'owner': owner,
                   'amount': (len(df_first_owner.loc[(df_first_owner['baalut_year'] == year) & (df_first_owner['baalut'] == owner)]))}
            annual_data.append(row)


    print(annual_data)


def new_cars_private():
    # Getting worth of purchase of new cars by year and owner
    df = pd.read_csv('owner.csv')

    # Convert 'baalut_dt' to datetime format
    df['baalut_dt'] = pd.to_datetime(df['baalut_dt'])
    # Get the row with the lowest 'baalut_dt' date value for each 'mispar_rechev' = new cars
    df_first_owner = df.loc[df.groupby('mispar_rechev')['baalut_dt'].idxmin()]

    # make dataframe consisting of private first owners
    df_first_owner_private = df_first_owner.loc[df_first_owner['baalut'] == 'פרטי']
    print(df_first_owner_private.shape)
    print(df_first_owner_private.columns)

    # Resources for looking up info about the cars
    resource_id1 = '053cea08-09bc-40ec-8f7a-156f0677aff3'

    url = 'https://data.gov.il/api/action/datastore_search'

    price_by_year = {2017: [], 2018: [], 2019: [], 2020: [], 2021: [], 2022: [], 2023: []}

    for year in df_first_owner_private['baalut_year'].unique():
        for car in df_first_owner_private['mispar_rechev'].unique():
            params1 = {"resource_id": resource_id1, "filters": f'{{"mispar_rechev": "{car}"}}'}

            # Make the HTTP request
            response = requests.get(url, params=params1)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the response JSON
                data1 = json.loads(response.text)

                # Getting data for each car
                if 'records' in data1['result'] and data1['result']['records']:
                    degem_nm = data1['result']['records'][0]['degem_nm']
                    degem_cd = data1['result']['records'][0]['degem_cd']
                    shnat_yitzur = data1['result']['records'][0]['shnat_yitzur']

                    car_price = get_car_price(degem_nm, degem_cd, shnat_yitzur)

                    if car_price:
                        price_by_year[shnat_yitzur].append(car_price)

    for year, prices in price_by_year.items():
        if prices:
            average_price = sum(prices) / len(prices)
            print(f'{year}: {average_price}')
        else:
            print(f'{year}: No data')


def get_car_price(degem_nm, degem_cd, shnat_yitzur):
    resource_id5 = '39f455bf-6db0-4926-859d-017f34eacbcb'
    url = 'https://data.gov.il/api/action/datastore_search'
    params2 = {"resource_id": resource_id5,
               "filters": f'{{"degem_nm": "{degem_nm}", "degem_cd": {degem_cd}, "shnat_yitzur":{shnat_yitzur}}}'}

    # Make the HTTP request
    response2 = requests.get(url, params=params2)

    # Check if the request was successful (status code 200)
    if response2.status_code == 200:
        # Parse the response JSON
        data2 = json.loads(response2.text)

        # Check if records exist
        if 'records' in data2['result'] and data2['result']['records']:
            return data2['result']['records'][0]['mehir']
    return None




new_cars_private()


