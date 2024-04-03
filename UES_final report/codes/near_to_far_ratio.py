import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

# set current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(script_dir)
os.chdir(script_dir)

# read respondent data
df_ngs = pd.read_csv('output/ngs_coords.csv')
df_pk = pd.read_csv('output/park_coords.csv')

# convert respondent location into spatial points
li_gdf = []
for df in [df_ngs, df_pk]:
    geometry = [Point(xy) for xy in zip(df['long'], df['lat'])]
    gdf_point = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
    li_gdf.append(gdf_point)
gdf_ngs = li_gdf[0]
gdf_pk = li_gdf[1]

# import boundary data
town_path = 'data/boundaries/HDBTown_SHP/HDB_TOWNESTATE_P.shp'
gdf_town = gpd.read_file(town_path)
PA_path = 'data/boundaries/MasterPlan2014PlanningAreaBoundaryNoSeaSHP/MP14_PLNG_AREA_NO_SEA_PL.shp'
gdf_PA = gpd.read_file(PA_path)
subzone_path = 'data/boundaries/MasterPlan2019SubzoneBoundaryNoSeaGEOJSON.geojson'
gdf_subzone = gpd.read_file(subzone_path)

# align crs
gdf_town = gdf_town.to_crs('EPSG:3857')
# gdf_subzone = gdf_subzone.to_crs('EPSG:3857')
gdf_PA = gdf_PA.to_crs('EPSG:3857')


# rename columns
gdf_town = gdf_town.rename(columns={'TEXTSTRING': 'NAME'})
gdf_PA = gdf_PA.rename(columns={'PLN_AREA_N': 'NAME'})
# gdf_subzone = gdf_subzone.rename(columns={'subzone_n': 'NAME'})
gdf_subzone = gdf_subzone.rename(columns={'Name': 'NAME'})


# define functino to conduct spatial join (find points within certain planning units)
def spatial_join(point_gdf, polygon_gdf):
    """
    This function is to conduct spatial join between two geo-datafrmaes.
    point_df: a geo-dataframe of the points (respondent locations)
    polygon_gdf: a geo-dataframe of the polygons (planning boundaries)
    return: the point geo-dataframe with information of corresponding planning unit
    (which planning unit the point is within).
    """
    if point_gdf.crs != polygon_gdf.crs:
        point_gdf = point_gdf.to_crs(polygon_gdf.crs)
    joined_gdf = gpd.sjoin(point_gdf, polygon_gdf, how='left', predicate='within')
    print('If there is any point cannot be matched?', joined_gdf.isna().any().any())
    return joined_gdf


# define function to get median for each planning unit
def get_median(joined_data):
    """
    This function is to get the median total duration of each planning unit.
    joined_data: the joined data frame retrieved from the spatial_join() function.
    return: a new point geo-dataframe with 2 columns - name of the planning units and the unit median (the point
    location is the location of respondent with median total duration of each planning ynit).
    """
    joined_median = joined_data.groupby('NAME')['total_dur'].transform('median')
    joined_data['unit_median'] = joined_median
    df_median = joined_data.drop_duplicates(subset=['NAME'])
    return df_median[['NAME', 'unit_median', 'geometry']]


# define function to calculate near-to-far ratio
def cal_ratio(m_pk, m_ngs):
    """
    This function is to calculate the near-to-far ratio of green space visits for each planning unit (the visit is to
    all the green spaces in Singapore but the aggregation is based on the planning unit).
    m_pk: the geo-dataframe of median total_duration for parks
    m_ngs: the geo-dataframe of median total_duration for ngs
    return: the geo-dataframe with near-to_far ratio
    """
    m_pk = m_pk.sort_values(by='NAME')
    m_ngs = m_ngs.sort_values(by='NAME')
    m_pk = m_pk.set_index(pd.Index(range(len(m_pk))))
    m_ngs = m_ngs.set_index(pd.Index(range(len(m_ngs))))
    merged_df = pd.merge(m_pk, m_ngs, on='NAME', how='outer', suffixes=['_pk', '_ngs'])
    # test = merged_df[merged_df.isnull().any(axis=1)] # there are 4 subzones with only ngs visits and 1 with only pk
    # visits
    merged_df[[col for col in merged_df.columns if 'median' in col]] = merged_df[[col for col in merged_df.columns if
                                                                                  'median' in col]].fillna(0)
    ratio = merged_df['unit_median_ngs'] / merged_df['unit_median_pk']
    merged_df['ratio'] = ratio
    merged_df = merged_df.drop(columns=['geometry_pk'])  # choose either on of the geometry column to drop as they are
    # the same
    merged_df = merged_df.rename(columns={'geometry_ngs': 'geometry'})
    return merged_df


for n, boundary in zip(['town', 'PA', 'subzone'], [gdf_town, gdf_PA, gdf_subzone]):
    joined_ngs = spatial_join(gdf_ngs, boundary)
    joined_median_ngs = get_median(joined_ngs)
    joined_pk = spatial_join(gdf_pk, boundary)
    joined_median_pk = get_median(joined_pk)
    gdf_output = cal_ratio(joined_median_pk, joined_median_ngs)
    # merge the ratio results to the boundary
    df_ratio = gdf_output[['NAME', 'unit_median_pk', 'unit_median_ngs', 'ratio']]
    df_ratio.to_csv(f'output/ratio_{n}.csv',index=False)
    boundary_output = pd.merge(boundary, df_ratio, on='NAME', how='left')
    boundary_output.to_file(f'output/ratio_{n}.geojson', driver='GeoJSON')
