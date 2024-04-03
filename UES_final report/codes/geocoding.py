import pandas as pd
import os
from pyonemap import OneMap
import numpy as np

# set current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(script_dir)
os.chdir(script_dir)

# read data
df_ngs = pd.read_csv('output/ngs_clean.csv', dtype={'PostalCode': str})
df_pk = pd.read_csv('output/park_clean.csv', dtype={'PostalCode': str})

# Obtain access token using email and password.
response = OneMap.getToken('cxy285@outlook.com', 'CXy82377882@97')  # go to OneMap API and register
access_token = response['access_token']

# Instantiate OneMap object for API query.
onemap = OneMap(access_token)


# Define function to call geocoding API
def get_coords(address):
    responses = onemap.search(address)
    out = [responses['results'][0]['LATITUDE'], responses['results'][0]['LONGITUDE'],
           responses['results'][0]['ADDRESS']]
    print(out[2])
    if not bool(out): # check if the response is empty
        print("response is empty")
    return out[0], out[1], out[2]

# print(get_coords("169480"))

# Define function to execute Geocoding
def execute(data):
    li_lat = []
    li_long = []
    li_address = []
    li_code = []
    for index, code in enumerate(data['PostalCode'].unique()):
        print(f'progress: {index + 1}|{len(data["PostalCode"].unique())}')
        li_code.append(code)
        output = get_coords(code)
        li_lat.append(output[0])
        li_long.append(output[1])
        li_address.append(output[2])
    df_coords = pd.DataFrame()
    df_coords['PostalCode'] = li_code
    df_coords['lat'] = li_lat
    df_coords['long'] = li_long
    df_coords['address'] = li_address
    # Attach the response to the original df
    merged_df = pd.merge(data, df_coords, on='PostalCode', how='left')
    merged_df = merged_df.drop_duplicates(subset=['MSNO'])

    return merged_df


# Cut df into chunks to prevent empty responses
li_output = []
for n, df in enumerate([df_pk, df_ngs]):
    num_chunks = 30
    chunks = np.array_split(df, num_chunks)
    li_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:")
        chunk_coords = execute(chunk)
        li_chunks.append(chunk_coords)
    df_output = pd.concat(li_chunks, axis=0)
    li_output.append(df_output)

# write output to csv
output_pk = li_output[0]
output_ngs = li_output[1]
output_pk.to_csv('output/park_coords.csv', index=False)
output_ngs.to_csv('output/ngs_coords.csv', index=False)

