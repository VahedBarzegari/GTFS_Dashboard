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
route_df1 = routes
routes_df=routes_df[['route_id','agency_id','route_short_name','route_long_name']]
calendar_df = calendar
calendar_dates_df = calendar_dates
agency_df = agency
stops_df = stops
stops_df = stops_df[['stop_id','stop_code','stop_name','stop_lat','stop_lon']]
stop_times_df = stop_times
stop_times_df = stop_times_df[['trip_id','arrival_time','departure_time','stop_id','stop_sequence']]
trips_df = trips
trips_df = trips_df[['route_id','trip_id','trip_headsign','block_id','shape_id']]
shapes_df = shapes

# Define a mapping for route_type values to their corresponding transportation modes
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

# Check if 'route_type' column exists in the 'routes' dataframe
if 'route_type' in routes.columns:
    # Count the occurrences of each route type
    route_type_counts = routes['route_type'].value_counts().reset_index()
    route_type_counts.columns = ['Mode ID', 'Number of Routes']

    # Map Mode ID to Mode Name
    route_type_counts['Mode'] = route_type_counts['Mode ID'].map(route_type_mapping)

    # Drop the "Mode ID" column and reset index
    route_type_df = route_type_counts[['Mode', 'Number of Routes']].reset_index(drop=True)

    # Add Row ID starting from 1
    route_type_df.insert(0, 'Row ID', range(1, len(route_type_df) + 1))



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



#####
unique_service_ids = trips['service_id'].unique()

if "calendar" in dataframes:
    calendar_exist = True

if "calendar_dates" in dataframes:
    calendar_dates_exist = True


if calendar_exist:
    # Filter calendar DataFrame to keep only the service_ids in unique_service_ids
    calendar = calendar[calendar['service_id'].isin(unique_service_ids)]
    calendar.reset_index(drop=True, inplace=True)

    calendar['start_timestamp'] = pd.to_datetime(calendar['start_date'], format='%Y%m%d')
    calendar['start_timestamp'] = calendar['start_timestamp'].dt.date

    calendar['end_timestamp'] = pd.to_datetime(calendar['end_date'], format='%Y%m%d')
    calendar['end_timestamp'] = calendar['end_timestamp'].dt.date

    column_order = ['service_id','monday','tuesday','wednesday','thursday','friday','saturday','sunday','start_timestamp','end_timestamp','start_date','end_date']
    calendar = calendar[column_order]

if  calendar_dates_exist:
    # Filter calendar_dates DataFrame to keep only the service_ids in unique_service_ids
    calendar_dates = calendar_dates[calendar_dates['service_id'].isin(unique_service_ids)]
    calendar_dates.reset_index(drop=True, inplace=True)
    calendar_dates['timestamp'] = pd.to_datetime(calendar_dates['date'], format='%Y%m%d')
    calendar_dates['timestamp'] = calendar_dates['timestamp'].dt.date

    column_order = ['service_id','date','timestamp','exception_type']
    calendar_dates = calendar_dates[column_order]






if calendar_exist:
    # Convert int64 to datetime objects
    start_date1 = pd.to_datetime(calendar['start_timestamp'].min())
    end_date1 = pd.to_datetime(calendar['end_timestamp'].max())
    d1 = calendar['service_id']
if calendar_dates_exist:
    # Convert int64 to datetime objects
    start_date2 = pd.to_datetime(calendar_dates['timestamp'].min())
    end_date2 = pd.to_datetime(calendar_dates['timestamp'].max())
    d2 = calendar_dates['service_id']

if calendar_exist & calendar_dates_exist:
    start_date = min (start_date1,start_date2)
    end_date = max(end_date1,end_date2)
elif calendar_exist:
    start_date = start_date1
    end_date = end_date1
elif calendar_dates_exist:
    start_date = start_date2
    end_date = end_date2



# Generate a range of dates between start_date and end_date
date_range = pd.date_range(start_date, end_date)

# Create a DataFrame with date and day columns
df = pd.DataFrame({'date': date_range, 'day': date_range.day_name().str.lower()})

# Assuming start_date and end_date are datetime objects
formatted_start_date = start_date.strftime("%B %d, %Y")
formatted_end_date = end_date.strftime("%B %d, %Y")



if calendar_exist & calendar_dates_exist:
    # Concatenate the two Series
    combined_series = pd.concat([d1, d2])
elif calendar_exist:
    combined_series = d1
elif calendar_dates_exist:
    combined_series = d2

# Get unique values and create a DataFrame with a reset index
d = pd.DataFrame({'service_id': combined_series.unique()}).reset_index(drop=True)
for i in range (len(d)):
    tem = d.loc[i,'service_id']
    df[tem] = 0
dfcopy = df.copy()




service_id_counts = trips['service_id'].value_counts()
h = 2+len(d)
for i in range (len(df)):
    a = df.iloc[i,0].date()
    b = df.iloc[i,1]
    
    if calendar_exist:
        for k in range (len(calendar)):
            if (a >= calendar.iloc[k,8]) & (a <= calendar.iloc[k,9]) & (calendar.loc[k,b]==1):
                c = calendar.iloc[k,0]
                df.loc[i,c] = 1
                dfcopy.loc[i,c] = service_id_counts.at[c]

if calendar_dates_exist:
    for w in range(len(calendar_dates)):
        m = calendar_dates.iloc[w,0]
        n = datetime.strptime(str(calendar_dates.iloc[w,1]), '%Y%m%d').date() 
        l = calendar_dates.iloc[w,3]

        desired_row = df[df['date'].dt.date == n]
        q = desired_row.index[0]
        if l==1:
            if m in service_id_counts.index:
                
                df.loc[q,m] = 1
                dfcopy.loc[q,m] = service_id_counts.at[m]
        elif l ==2:
            df.loc[q,m] = 0
            dfcopy.loc[q,m] = 0
df_tempo = df.copy()
df['Number_of_Active_services'] = df.iloc[:, 2:h].sum(axis=1)
df['Number_of_Active_Trips'] = dfcopy.iloc[:,2:h].sum(axis=1)



 
# Create an empty list to store the results
result_list = []

# Iterate through rows
for index, row in df_tempo.iterrows():
    # Filter columns where the value is 1
    active_services = row.index[row.eq(1)].tolist()
    
    # Append the result to the list
    result_list.append({'date': row['date'],'day': row['day'], 'active_services': active_services})


# If you want to save the result to a file, you can use the following code
result_df = pd.DataFrame(result_list)
mergedresult_df = pd.merge(result_df, df[['Number_of_Active_services','Number_of_Active_Trips', 'date']], on='date', how='left')




# Assuming mergedresult_df is your dataframe

# Convert lists in 'active_services' column to tuples
mergedresult_df['active_services_tuple'] = mergedresult_df['active_services'].apply(tuple)

# Group by the new column 'active_services_tuple'
grouped = mergedresult_df.groupby('active_services_tuple')

# Aggregate dates within each group
dates_by_services = grouped['date'].agg(list)

# Create a dictionary to store categories
categories = {}
category_count = 1

# Loop through each group
for services, dates in dates_by_services.items():
    
    
    category_key = f'{category_count}'
    categories[category_key] = {'active_services': list(services), 'dates': dates}
    # Assign this category to each date in the group
    for date in dates:
        mergedresult_df.loc[mergedresult_df['date'] == date, 'category'] = category_key
    category_count += 1


# Drop the temporary column
mergedresult_df.drop(columns=['active_services_tuple'], inplace=True)



mergedresult_df = mergedresult_df[['date','active_services']]

mergedresult_df['date'] = pd.to_datetime(mergedresult_df['date'])


#mergedresult_df.to_csv('Date_Classification.csv', index=False)

Date_Classification_df = mergedresult_df


column_order=['trip_id','arrival_time','departure_time','stop_id','stop_sequence']
newstop_times = stop_times[column_order]

mergedstop_times = pd.merge(newstop_times, trips[['service_id', 'trip_id']], on='trip_id', how='left')

column_order=['service_id','trip_id','arrival_time','departure_time','stop_id','stop_sequence']
mergedstop_times = mergedstop_times[column_order]


mergedstop_times = pd.merge(mergedstop_times, trips[['route_id', 'trip_id']], on='trip_id', how='left')
column_order=['route_id','service_id','trip_id','arrival_time','departure_time','stop_id','stop_sequence']
mergedstop_times = mergedstop_times[column_order]
mergedstop_times = pd.merge(mergedstop_times, stops[['stop_id', 'stop_lat','stop_lon']], on='stop_id', how='left')

mergedstop_times = pd.merge(mergedstop_times, trips[['trip_id', 'shape_id']], on='trip_id', how='left')
mergedstop_times = pd.merge(mergedstop_times, trips[['trip_id', 'block_id']], on='trip_id', how='left')
column_order=['route_id','service_id','trip_id','block_id','shape_id','arrival_time','departure_time','stop_id','stop_lat','stop_lon','stop_sequence']
mergedstop_times = mergedstop_times[column_order]


modified_stop_times_df = mergedstop_times

#mergedstop_times.to_csv('modified_stop_times.csv', index=False)