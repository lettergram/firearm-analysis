import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter  
import pandas as pd
import geopandas
import imageio

# Load the firearm data data
data_file = 'data/rand-gun-ownership/United-States-1980-2016-Firearm-Ownership-Rand.csv'

state_data = pd.read_csv(data_file)

# Create a snapshot of each year
years = state_data.sort_values(by=['Year'])['Year'].unique()

# Import map data & merge with states
# https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
pd.set_option('display.max_columns', None) 
geo_us_data = geopandas.read_file('data/geo-data')
geo_us_data = geo_us_data.rename(columns={'NAME': 'STATE'})
geo_us_data = geo_us_data.merge(state_data, on='STATE')

country_data = {}
for year in years:
    year_filter = geo_us_data['Year'] == year
    country_data[year] = geo_us_data.where(year_filter).dropna()

# Generate figures
output_path = 'images/geo-us-firearme-ownership-rate/'
ymin, ymax = 0, max(geo_us_data['Rate'])
for year in years:

    print(country_data[year])

    # Assumes matplotlib backend
    fig = country_data[year].plot(column='Rate', cmap='OrRd',
                                  figsize=(20,10), legend=True,
                                  vmin=ymin, vmax=ymax,
                                  norm=plt.Normalize(vmin=ymin, vmax=ymax))

    # Zoom to Continental U.S.
    fig.set_xlim(-125, -67)
    fig.set_ylim(24, 49)
    
    fig.axis('off')
    
    fig.set_title('Homicides per 100,000 Inhabitants, United States', \
                  fontdict={'fontsize': '28', 'fontweight' : '4'})

    fig.annotate(year, xy=(0.1, .3), xycoords='figure fraction',
                 horizontalalignment='left', verticalalignment='top',
                 fontsize=35)
    
    us_map = fig.get_figure()
    us_map.savefig(output_path+"us_"+str(year)+'_murders.png',
                   dpi=150, bbox_inches='tight')
    us_map.tight_layout()

# Create gif, images should be in order due to name
image_files = glob.glob("images/geo-us-murder-rate/*")
image_files.sort()
images = [imageio.imread(image) for image in image_files]
imageio.mimwrite('images/murders-us-overtime.gif', images,
                 fps=1, palettesize=128)
