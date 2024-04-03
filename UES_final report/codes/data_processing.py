import pandas as pd
import os

# set current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(script_dir)
os.chdir(script_dir)

# read data and extract necessary columns-----------------------------------------------------------
df = pd.read_excel('data/questionnaires/Project Green Final Data n=1010 @ 091222 V2.xlsx', dtype={'PostalCode': str})

colnames1 = ['MSNO', 'PostalCode']
colnames_ngs = [col for col in df.columns if 'G1' in col or 'G2' in col or 'G3' in col]
colnames_pk = [col for col in df.columns if 'G5' in col or 'G6' in col or 'G7' in col]
df_ngs = df[colnames1 + colnames_ngs]
df_pk = df[colnames1 + colnames_pk]


# data cleaning ------------------------------------------------------------------------------------

# drop columns with no listed green spaces
df_ngs = df_ngs.query('G1 == 1')
df_pk = df_pk.query('G5 == 1')

# create a record for each [MSNO + listed green space location]
li_all = []
for n, gs in enumerate([df_ngs, df_pk]):
    li_loc = []
    for loc in range(1, 6):
        colnames_loc = [col for col in gs.columns if 'Location_' + str(loc) in col]
        df_loc = gs[colnames1 + colnames_loc]
        df_loc.columns = ['MSNO', 'PostalCode', 'coords', 'freq', 'dur', 'dur_hour_min']
        if n == 0:
            df_loc['category'] = 'ngs'
        if n == 1:
            df_loc['category'] = 'pk'
        li_loc.append(df_loc)
    df_loc_all = pd.concat(li_loc, axis=0)
    li_all.append(df_loc_all)
df_ngs = li_all[0]
df_pk = li_all[1]

# drop columns where coords column is NaN, meaning that the green space is not listed
df_ngs = df_ngs.query('not coords.isna()')
df_pk = df_pk.query('not coords.isna()')

# convert duration into minutes
df_ngs.loc[df_ngs['dur_hour_min'] == 1, 'dur'] *= 60
df_pk.loc[df_pk['dur_hour_min'] == 1, 'dur'] *= 60

# drop dur_hour_min column
df_ngs.drop('dur_hour_min', axis=1, inplace=True)
df_pk.drop('dur_hour_min', axis=1, inplace=True)

# split the coords column into latitude and longitude column
df_ngs[['lat', 'long']] = df_ngs['coords'].str.split(',', expand=True)
df_pk[['lat', 'long']] = df_pk['coords'].str.split(',', expand=True)

# drop the original column if needed
df_ngs.drop('coords', axis=1, inplace=True)
df_pk.drop('coords', axis=1, inplace=True)

# convert the lat and long into float
df_ngs['lat'] = df_ngs['lat'].astype(float)
df_ngs['long'] = df_ngs['long'].astype(float)
df_pk['lat'] = df_pk['lat'].astype(float)
df_pk['long'] = df_pk['long'].astype(float)

# sort by MSNO (respondent)
df_ngs = df_ngs.sort_values(by='MSNO')
df_pk = df_pk.sort_values(by='MSNO')

# find median total duration for each respondent -----------------------------------------------------------------------

# calcualte total duration for each park visited by each respondent
df_ngs['total_dur'] = df_ngs['freq'] * df_ngs['dur']
df_pk['total_dur'] = df_pk['freq'] * df_pk['dur']

# group by MSNO and found the median total duration for each respondent
resp_ngs_median = df_ngs.groupby('MSNO')['total_dur'].median().reset_index()
resp_pk_median = df_pk.groupby('MSNO')['total_dur'].median().reset_index()

# attach postal code to the median df
df_ngs = pd.merge(resp_ngs_median, df_ngs[['MSNO', 'PostalCode']], on='MSNO', how='left')
df_pk = pd.merge(resp_pk_median, df_pk[['MSNO', 'PostalCode']], on='MSNO', how='left')

df_ngs.to_csv(r'output/ngs_clean.csv', index=False)
df_pk.to_csv(r'output/park_clean.csv', index=False)

print(df_ngs)
print(df_pk)

