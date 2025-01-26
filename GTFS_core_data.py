import os
import zipfile
import pandas as pd
from datetime import datetime, timedelta
import folium

from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D
import folium
from folium import plugins



# Search for the ZIP file in the current directory
zip_files = [f for f in os.listdir('.') if f.endswith('_GTFS.zip')]

# Ensure there is exactly one ZIP file
if len(zip_files) != 1:
    raise FileNotFoundError(f"Expected exactly one ZIP file with pattern '*_GTFS.zip', but found: {zip_files}")

# Path to the found ZIP file
zip_path = zip_files[0]

# Extract City_Name from the ZIP file name (before the first underscore)
City_Name = zip_path.split('_')[0]

# Dictionary to store DataFrames with file names as keys
dataframes = {}

# Open the ZIP file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    # Iterate over all files in the ZIP archive
    for file_name in zip_ref.namelist():
        if file_name.endswith('.txt'):  # Only process text files
            with zip_ref.open(file_name) as file:
                # Read each file into a DataFrame and save to dictionary
                df_name = file_name.split(".")[0]  # Use file name without extension as variable name
                dataframes[df_name] = pd.read_csv(file)
                # Dynamically assign DataFrame to a variable
                globals()[df_name] = dataframes[df_name]




routes_df = routes
calendar_df = calendar
calendar_dates_df = calendar_dates
agency_df = agency
stops_df = stops
stop_times_df = stop_times
trips_df = trips
shapes_df = shapes


shape_route = trips[['route_id', 'shape_id']].drop_duplicates()
shape_route = shape_route.merge(routes[['route_id','route_type','route_color']], on='route_id', how='left')

route_type_mapping = {
    0: "Streetcar",
    1: "Subway",
    2: "Rail",
    3: "Bus",
    4: "Ferry",
    5: "Cable Tram",
    6: "Aerial Lift",
    7: "Funicular",
    11: "Trolleybus",
    12: "Monorail"
}
shape_route['modes'] = shape_route['route_type'].map(route_type_mapping)


shape_route_df = shape_route