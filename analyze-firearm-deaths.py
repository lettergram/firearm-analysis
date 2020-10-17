import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter  
import pandas as pd
import geopandas
import imageio

def create_us_map(geo_us_data, column_to_analyze, title, gif_name, image_dir, color_map):

    # Create a snapshot of each year
    years = state_data.sort_values(by=['Year']).dropna(
        subset=[column_to_analyze]
    )['Year'].unique()
    
    country_data = {}
    for year in years:
        year_filter = geo_us_data['Year'] == year
        country_data[year] = geo_us_data.where(year_filter).dropna(
            subset=[column_to_analyze]
        )

    # Generate figures
    ymin, ymax = 0, max(geo_us_data.dropna(
        subset=[column_to_analyze]
    )[column_to_analyze])
    
    for year in years:

        print(column_to_analyze + ", Generating " + str(year))
        
        # Assumes matplotlib backend
        fig = country_data[year].plot(column=column_to_analyze,
                                      cmap=color_map,
                                      figsize=(20,10), legend=True,
                                      vmin=ymin, vmax=ymax,
                                      norm=plt.Normalize(vmin=ymin, vmax=ymax))

        # Zoom to Continental U.S.
        fig.set_xlim(-125, -67)
        fig.set_ylim(24, 49)
    
        fig.axis('off')
    
        fig.set_title(title, fontdict={'fontsize': '28', 'fontweight' : '4'})

        fig.annotate(year, xy=(0.1, .3), xycoords='figure fraction',
                     horizontalalignment='left', verticalalignment='top',
                     fontsize=35)
    
        us_map = fig.get_figure()
        us_map.savefig(image_dir+"us_"+str(year)+'.png',
                       dpi=65, bbox_inches='tight')
        us_map.tight_layout()

    # Create gif, images should be in order due to name
    image_files = glob.glob(image_dir+"*")
    image_files.sort()
    images = [imageio.imread(image) for image in image_files]
    imageio.mimwrite(gif_name, images, fps=1, palettesize=128)


# Load the FBI & CDC homicde data
data_file = 'data/fbi-cdc-deaths-state-yearly.csv'
state_data = pd.read_csv(data_file).dropna(how='all')

# Import map data & merge with states
# https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
pd.set_option('display.max_columns', None) 
geo_us_data = geopandas.read_file('data/geo-data')
geo_us_data = geo_us_data.rename(columns={'NAME': 'STATE'})
geo_us_data = geo_us_data.merge(state_data, on='STATE')

# Firearm owners
column_to_analyze = 'Firearm Owners per 100k inhabitants'
title = 'Firearm Owners per 100,000 Inhabitants, United States'
image_dir = 'images/geo-us-firearm-owners/'
gif_name = 'images/firearm-owners-overtime.gif'
color_map = 'GnBu'
create_us_map(geo_us_data, column_to_analyze,
              title, gif_name, image_dir, color_map)

# Homicides per Firearm Owners
column_to_analyze = 'Homicides per Firearm Owner'
title = 'Homicides per Firearm Owner, United States'
image_dir = 'images/homicides-per-firearm/'
gif_name = 'images/homicides-per-firearm-overtime.gif'
color_map = 'OrRd'
create_us_map(geo_us_data, column_to_analyze,
              title, gif_name, image_dir, color_map)


# Handgun Murder Rate
column_to_analyze = 'Handgun Rate'
title = 'Handgun Homicide Rate per 100,000 Inhabitants, United States'
image_dir = 'images/homicide-rate-handgun/'
gif_name = 'images/homicide-rate-handgun.gif'
color_map = 'OrRd'
create_us_map(geo_us_data, column_to_analyze,
              title, gif_name, image_dir, color_map)


# Handgun Murder Rate
column_to_analyze = 'Homicides per 100k Inhabitants'
title = 'Homicides per 100k Inhabitants, United States'
image_dir = 'images/geo-us-homicide-rate/'
gif_name = 'images/homicide-rate-us.gif'
color_map = 'OrRd'
create_us_map(geo_us_data, column_to_analyze,
              title, gif_name, image_dir, color_map)



# Load the FBI & CDC homicde data
data_file = 'data/cdc-deaths-US-State-Race-Yearly.csv'
state_data = pd.read_csv(data_file).dropna(how='all')

# Import map data & merge with states
# https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
pd.set_option('display.max_columns', None) 
geo_us_data = geopandas.read_file('data/geo-data')
geo_us_data = geo_us_data.rename(columns={'NAME': 'STATE'})
geo_us_data = geo_us_data.merge(state_data, on='STATE')



column_to_analyze = 'Homicides per 100k Inhabitants'
title = 'Homicides per 100k Inhabitants, United States'
image_dir = 'images/geo-us-homicide-rate/'
gif_name = 'images/homicide-rate-us.gif'
color_map = 'OrRd'
create_us_map(geo_us_data, column_to_analyze,
              title, gif_name, image_dir, color_map)
