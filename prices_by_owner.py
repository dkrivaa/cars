import aiohttp
import asyncio
import pandas as pd


async def fetch_price(session, degem_nm, degem_cd, shnat_yitzur):
    resource_id5 = '39f455bf-6db0-4926-859d-017f34eacbcb'
    url = 'https://data.gov.il/api/action/datastore_search'
    params2 = {
        "resource_id": resource_id5,
        "filters": f'{{"degem_nm": "{degem_nm}", "degem_cd": {degem_cd}, "shnat_yitzur":{shnat_yitzur}}}'
    }

    async with session.get(url, params=params2, timeout=aiohttp.ClientTimeout(total=360)) as response:
        data2 = await response.json()
        if 'records' in data2['result'] and data2['result']['records']:
            return data2['result']['records'][0]['mehir']


async def process_car(session, car, resource_id1):
    params1 = {"resource_id": resource_id1, "filters": f'{{"mispar_rechev": "{car}"}}'}
    url = 'https://data.gov.il/api/action/datastore_search'

    async with session.get(url, params=params1, timeout=aiohttp.ClientTimeout(total=360)) as response:
        data1 = await response.json()
        if 'records' in data1['result'] and data1['result']['records']:
            degem_nm = data1['result']['records'][0]['degem_nm']
            degem_cd = data1['result']['records'][0]['degem_cd']
            shnat_yitzur = data1['result']['records'][0]['shnat_yitzur']

            return await fetch_price(session, degem_nm, degem_cd, shnat_yitzur)


async def main():
    # Load only necessary columns
    df = pd.read_csv('owner.csv', usecols=['mispar_rechev', 'baalut', 'baalut_dt', 'baalut_year'])
    print(df['baalut'].unique())
    # Convert 'baalut_dt' to datetime format
    df['baalut_dt'] = pd.to_datetime(df['baalut_dt'])
    # Get the row with the lowest 'baalut_dt' date value for each 'mispar_rechev' = new cars
    df = df.loc[df.groupby('mispar_rechev')['baalut_dt'].idxmin()]
    # df = df.loc[(df['baalut'] == 'השכרה') & (df['baalut_year'] == 2017)]
    print(df.shape)
    print(df.columns)
    resource_id1 = '053cea08-09bc-40ec-8f7a-156f0677aff3'
    url = 'https://data.gov.il/api/action/datastore_search'

    price_by_year = {year: [] for year in df['baalut_year'].unique()}

    async with aiohttp.ClientSession() as session:
        tasks = []
        for year in df['baalut_year'].unique():
            for car in df['mispar_rechev'].unique():
                tasks.append(process_car(session, car, resource_id1))

        # Execute the tasks concurrently
        results = await asyncio.gather(*tasks)

        # Update the price_by_year dictionary
        index = 0
        for year in df['baalut_year'].unique():
            for _ in df['mispar_rechev'].unique():
                price_by_year[year].append(results[index])
                index += 1

    # Calculate and print average prices
    for year, prices in price_by_year.items():
        if prices:
            average_price = sum(prices) / len(prices)
            print(f'{year}: {average_price}')
        else:
            print(f'{year}: No data')

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())