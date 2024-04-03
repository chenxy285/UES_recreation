import matplotlib.pyplot as plt
import geopandas as gpd
import os
import contextily as cx

# set current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(script_dir)
os.chdir(script_dir)


def mapping(boundary):
    boundary_file = gpd.read_file(f'output/ratio_{boundary}.geojson')

    if boundary == 'subzone':
        boundary_file = boundary_file.to_crs('EPSG:3857')

    # Plot polygons with missing 'ratio' values
    fig, ax = plt.subplots(figsize=(8, 6))

    boundary_file.plot(column='ratio', cmap='viridis', linewidth=0.5, ax=ax, edgecolor='black', legend=True,
                       scheme='quantiles', k=5, aspect='equal', label='Ratio', missing_kwds={'color': 'None',
                                                                                             'label': "Missing",
                                                                                             'edgecolor': 'grey'},
                       legend_kwds={'title': 'Ratio of near-to-far visits last year (dur)', 'fontsize': 10,
                                    'title_fontsize': 10})

    mask_bounds = [11530646.691451669, 127257.07485223816, 11589770.086582351, 170481.35667356252] # retrieve from
    # map of PA
    # Set the extent of the plot to match the mask layer
    ax.set_xlim(mask_bounds[0], mask_bounds[2])
    ax.set_ylim(mask_bounds[1], mask_bounds[3])

    cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)

    ax.set_axis_off()
    plt.tight_layout()

    # Save the plot as an image file
    boundary_filename = f'{boundary}_map.pdf'
    plt.savefig(f'output/figures/{boundary_filename}', dpi=300, bbox_inches='tight', pad_inches=0)
    print(f'{boundary} map saved!')


mapping('town')
mapping('subzone')
mapping('PA')
