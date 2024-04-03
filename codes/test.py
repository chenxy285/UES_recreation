import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
import os
from pyproj import Transformer

script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(script_dir)
os.chdir(script_dir)


# # Load the GeoDataFrame containing Singapore's subzone boundary data
# subzone = gpd.read_file("output/ratio_subzone.geojson")
#
# # Separate polygons with missing 'ratio' values
# missing_values_mask = subzone['ratio'].isnull()
# subzone_with_missing_values = subzone[missing_values_mask]
# subzone_with_values = subzone[~missing_values_mask]
#
# # Plot polygons with missing 'ratio' values
# fig, ax = plt.subplots(figsize=(10, 6))
# subzone_with_missing_values.plot(color='gray', linewidth=0.8, edgecolor='black', ax=ax, alpha=0.5)
#
# # Plot polygons with 'ratio' values
# subzone_with_values.plot(column='ratio', cmap='viridis', linewidth=0.8, ax=ax, edgecolor='black', legend=True, scheme='quantiles', k=5)
#
# # Choose an alternative basemap provider (e.g., OpenStreetMap)
# basemap_provider = ctx.providers.OpenStreetMap.Mapnik
#
# # Get the CRS of the GeoDataFrame
# crs_subzone = subzone_with_values.crs
#
# # Define the CRS of the basemap (EPSG code 3857)
# crs_basemap = "EPSG:3857"
#
# # Transform the GeoDataFrame CRS to match the basemap CRS
# transformer = Transformer.from_crs(crs_subzone, crs_basemap)
# subzone_transformed = subzone_with_values.to_crs(transformer)
#
# # Add basemap
# ctx.add_basemap(ax, crs=crs_basemap)
#
# # Set title
# plt.title('Choropleth Map')
#
# # Save the plot as an image file
# subzone_filename = 'subzone_map.png'
# plt.savefig(f'output/{subzone_filename}', dpi=300)  # dpi parameter sets the resolution (dots per inch)
#
# # Show the plot
# plt.show()



# fig, ax = plt.subplots(figsize=(8, 8))
# extent = (-12600000, -10300000, 1800000, 3800000)
# ax.axis(extent)
# cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
# plt.show()

boundary = 'subzone'
boundary_file = gpd.read_file(f'output/ratio_{boundary}.geojson')
# boundary_file = gpd.read_file(f'data/sg_subzones.geojson')



fig, ax = plt.subplots(figsize=(10, 10))
boundary_file.plot(column='ratio', cmap='viridis', linewidth=0.5, ax=ax, edgecolor='black', legend=True,
                              scheme='quantiles', k=5, aspect='equal', label='Ratio',missing_kwds={'color': 'None',
                                                                                                   'label': "Missing",
                                                                                                   'edgecolor':'grey'})
# boundary_file.plot(linewidth=0.5, ax=ax, edgecolor='black', legend=True, label='Boundary')
cx.add_basemap(ax,source=cx.providers.CartoDB.Positron)
plt.show()