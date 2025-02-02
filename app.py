import ast
import asyncio
from datetime import datetime
from faicons import icon_svg
import faicons
import folium.map
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import folium
from folium.plugins import HeatMap

from pathlib import Path


from GTFS_core_data import routes_df, agency_df, stops_df, stop_times_df, calendar_df, calendar_dates_df, shapes_df, trips_df,shape_route_df, route_type_df,route_df1, Date_Classification_df, modified_stop_times_df

import altair as alt
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from shiny import reactive
from shiny.express import render,input, ui
from shinywidgets import render_plotly, render_altair, render_widget


ui.tags.style(
    """
        .header-container {
        
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: black;
            height: 90px;
        }


        .logo-container {
            margin-right: 5px;
            height: 100%;
            padding: 10px;
        
        }

        .logo-container img {
            height: 60px;
        }

        .title-container h2 {
            color: white;
            padding: 5px;
            margin: 0;
        
        }




        body {

            background-color: #5e41aa;
        
        
        }


        .modebar{
            display: none;
        
        }

    """
)



ui.page_opts(window_title="GTFS DASHBOARD", fillable=False)





with ui.div(class_="header-container"):
    with ui.div(class_="logo-container"):

        @render.image  
        def image():
            here = Path(__file__).parent
            img = {"src": here / "images/TTC-logo.png"}  
            return img 

    with ui.div(class_="title-container"):
        ui.h2("GTFS Dashboard of Toronto")

############################################
with ui.card():
    
    ui.card_header("General Information")
    with ui.layout_columns(col_widths={"sm": (3,3,3,3)}):

        with ui.value_box(
            showcase=faicons.icon_svg("calendar-days", width="50px"),
            theme="bg-gradient-green-red",
        ):
            "Start Date"

            @render.ui  
            def datestartfun():  
                return "January 05, 2025"  
            

        with ui.value_box(
            showcase=faicons.icon_svg("calendar-days", width="50px"),
            theme="bg-gradient-orange-red",
        ):
            "End Date"

            @render.ui  
            def dateendfun():  
                return "February 16, 2025"  
            


        with ui.value_box(
            showcase=faicons.icon_svg("road", width="50px"),
            theme="bg-gradient-yellow-purple",
        ):
            "Number of routes"

            @render.ui  
            def routefun():  
                return "217"  
            

        with ui.value_box(
            showcase=faicons.icon_svg("train-subway", width="50px"),
            theme="bg-gradient-blue-purple",
        ):
            "Number of Stops"

            @render.ui  
            def stopfun():  
                return "9369"  

############################################

with ui.layout_columns(
    col_widths={"sm": (4, 8)}, height='510px'
):

    with ui.card():
        ui.card_header("Mode Choice")

        ui.input_selectize(
            "modechoice",
            "Select a Mode:",
            {"allmodes": "All Modes", "Bus": "Bus","Streetcar": "Streetcar", "Subway": "Subway"},
        )

        ui.br()
        ui.br()
        ui.br()


        with ui.card():

            @render.data_frame
            def sample_mode_type():
                    
                return render.DataGrid(route_type_df.head(100), selection_mode="row", filters=False)
        
        

    with ui.card():
        ui.card_header("Network Layout")

        @render.ui
        @reactive.event(input.modechoice)  # Make map reactive to selection
        def plot_network():
            # Define the mode-to-color mapping
            mode_color_mapping1 = {
                "Streetcar": "#4169E1",  # Blue for Streetcar
                "Subway": "#00FF00",     # Green for Subway
                "Bus": "#FF0000"         # Red for Bus
            }

            selected_mode = input.modechoice() or "allmodes"

            center_lat = shapes_df['shape_pt_lat'].mean()
            center_lon = shapes_df['shape_pt_lon'].mean()

            # Create the map
            m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles=None)

            # Add a tile layer with opacity control
            folium.TileLayer(
                tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                attr='OpenStreetMap',
                name='Custom Background',
                opacity=0.4
            ).add_to(m)

            # Filter data based on selection
            if selected_mode != "allmodes":
                ax = shape_route_df[shape_route_df["modes"] == selected_mode]
                if selected_mode == "Bus":
                    mode_color_mapping = {
                        "Bus": "#FF0000"


                    }

                elif selected_mode == "Subway":
                    mode_color_mapping = {
                        "Subway": "#00FF00"


                    }

                elif selected_mode == "Streetcar":
                    mode_color_mapping = {
                        "Streetcar": "#4169E1"


                    }

            else:
                ax = shape_route_df
                mode_color_mapping = mode_color_mapping1


            ax = ax.sort_values(by='modes')

            # Plot shapes
            for shape_id in ax['shape_id'].unique():
                mode = ax.loc[ax['shape_id'] == shape_id, 'modes'].iloc[0]
                color = mode_color_mapping.get(mode, '#000000')
                shape_data = shapes_df[shapes_df['shape_id'] == shape_id]
                shape_coords = shape_data[['shape_pt_lat', 'shape_pt_lon']].values.tolist()
                folium.PolyLine(shape_coords, color=color).add_to(m)

            # Define the legend
            legend_html = '''
            <div style="
                position: fixed; 
                bottom: 20px; left: 20px; width: 100px; height: auto; 
                background-color: white; z-index:9999; font-size:14px;
                border-radius: 5px; padding: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            ">
            <b>Legend</b><br>
            ''' + ''.join([f'<div style="display: flex; align-items: center;"><div style="width: 15px; height: 15px; background: {color}; margin-right: 5px;"></div>{mode}</div>' for mode, color in mode_color_mapping.items()]) + '</div>'

            m.get_root().html.add_child(folium.Element(legend_html))

            return m


with ui.layout_columns(col_widths={"sm": (4,8)}, height='400px'):


    with ui.card():
        ui.card_header("Explanation")


        @render.ui
        def dynamic_content():
            #if input.tab() == "agency":
            return ui.TagList(
                ui.h6("List of Feeds"),
                ui.tags.ul(  # Unordered list for bullet points
                    ui.tags.li("agency"),
                    ui.tags.li("calendar"),
                    ui.tags.li("calendar_dates"),
                    ui.tags.li("routes"),
                    ui.tags.li("trips"),
                    ui.tags.li("stop_times"),
                    ui.tags.li("shapes"),
                    ui.tags.li("stops"),
                    ui.tags.li("feed_info")

                ),
                ui.p("Explore feed tables or refer to ", 
                    ui.a("ttc.ca", href="https://www.ttc.ca", target="_blank"))
            )
       

    with ui.navset_card_underline(id="tab", placement='above', title="GTFS Feeds"):

        with ui.nav_panel("agency"): 
            with ui.card():
                @render.data_frame
                def sample_sales_data1():
                    return render.DataGrid(agency_df.head(100), selection_mode="row", filters=False)
            
        with ui.nav_panel("Calendar"):
            with ui.card():
                @render.data_frame
                def sample_sales_data2():
                    return render.DataGrid(calendar_df.head(100), selection_mode="row", filters=False)

        with ui.nav_panel("Calendar_dates"):
            with ui.card():
                @render.data_frame
                def sample_sales_data3():
                    return render.DataGrid(calendar_dates_df.head(100), selection_mode="row", filters=False)

        with ui.nav_panel("Routes"):
            with ui.card():
                @render.data_frame
                def sample_sales_data4():
                    return render.DataGrid(routes_df, selection_mode="row", filters=True)

        with ui.nav_menu("Other feeds"):
            with ui.nav_panel("Stops"):
                with ui.card():
                    @render.data_frame
                    def sample_sales_data5():
                        return render.DataGrid(stops_df.head(100), selection_mode="row", filters=True)

            with ui.nav_panel("Stop times"):
                with ui.card():
                    @render.data_frame
                    def sample_sales_data6():
                        return render.DataGrid(stop_times_df.head(100), selection_mode="row", filters=True)

            with ui.nav_panel("Trips"):
                with ui.card():
                    @render.data_frame
                    def sample_sales_data7():
                        return render.DataGrid(trips_df.head(100), selection_mode="row", filters=True)

      #else:
                #return ui.h3("kiiiiiir")

with ui.card():
    ui.card_header("Data of the selected date")
    with ui.layout_columns(col_widths=(5, 7), height='900px'):
        with ui.card():

            with ui.card():
                ui.card_header("Select Date")
                ui.input_date("date", "", min='2025-01-05', max='2025-02-16')  

                

            

                Date_Classification_df['date'] = pd.to_datetime(Date_Classification_df['date']).dt.date  

                @render.data_frame
                def sample_sales_data61():
                    selected_date = input.date()  # Ensure date selection updates the table

                    # Fetch active services
                    active_services = Date_Classification_df.loc[Date_Classification_df['date'] == selected_date, 'active_services'].values
                    filtered_stop_time = pd.DataFrame()  # Initialize as empty DataFrame

                    if len(active_services) > 0:
                        active_services = active_services[0]  

                        if isinstance(active_services, str):  
                            active_services = ast.literal_eval(active_services)  # Convert string to list
                        
                        if not isinstance(active_services, list):  
                            active_services = [active_services]  # Ensure it's a list

                        filtered_stop_time = modified_stop_times_df[modified_stop_times_df['service_id'].isin(active_services)]



                    

                    if len(filtered_stop_time)>0:
                        # Calculate the required values
                        num_routes_busiest_day = filtered_stop_time['route_id'].nunique()
                        num_stops_busiest_day = filtered_stop_time['stop_id'].nunique()
                        num_trips_busiest_day = filtered_stop_time['trip_id'].nunique()
                        num_blocks_busiest_day = filtered_stop_time['block_id'].nunique()

                        dfsa1 = filtered_stop_time.groupby('route_id').agg({
                            'trip_id': 'nunique',
                            'block_id': 'nunique',

                        }).reset_index()

                        dfsa2 = filtered_stop_time.groupby('trip_id').agg({
                            'stop_sequence': 'max',

                        }).reset_index()
                        


                        ave_trip_per_route = int(round(dfsa1['trip_id'].mean()))
                        ave_block_per_route = int(round(dfsa1['block_id'].mean()))
                        ave_stop_per_trip = int(round(dfsa2['stop_sequence'].mean()))
                    else:
                        num_routes_busiest_day = "Unknown"
                        num_stops_busiest_day = "Unknown"
                        num_trips_busiest_day = "Unknown"
                        num_blocks_busiest_day = "Unknown"
                        ave_trip_per_route = "Unknown"
                        ave_block_per_route = "Unknown" 
                        ave_stop_per_trip = "Unknown"                 

                    # Create a DataFrame
                    summary_df = pd.DataFrame({
                        'Metric': ['Number of active routes', 'Number of active stops', 'Number of trips', 'Number of blocks', 'Average Number of Trips per Route', 'Average Number of Blocks per Route', 'Average Number of Stops per Trip'],
                        'Value': [num_routes_busiest_day, num_stops_busiest_day, num_trips_busiest_day, num_blocks_busiest_day, ave_trip_per_route, ave_block_per_route, ave_stop_per_trip]
                    })

                    return render.DataGrid(summary_df.head(100), selection_mode="row", filters=False)



            # # Compare selected date with 2024-12-12 (converted to a date object)
            # if selected_date == datetime(2024, 12, 12).date():
            #     return type(selected_date)
            # else:
            #     return "400"

            # Dynamically render the result
            with ui.card():
                
                ui.card_header("Top Routes")
                Date_Classification_df['date'] = pd.to_datetime(Date_Classification_df['date']).dt.date  

                @render.data_frame
                def sample_sales_data71():
                    if input.date():
                        selected_date = input.date()  # Ensure date selection updates the table

                        # Fetch active services
                        active_services = Date_Classification_df.loc[Date_Classification_df['date'] == selected_date, 'active_services'].values
                        filtered_stop_time = pd.DataFrame()  # Initialize as empty DataFrame

                        if len(active_services) > 0:
                            active_services = active_services[0]  

                            if isinstance(active_services, str):  
                                active_services = ast.literal_eval(active_services)  # Convert string to list
                            
                            if not isinstance(active_services, list):  
                                active_services = [active_services]  # Ensure it's a list

                            filtered_stop_time = modified_stop_times_df[modified_stop_times_df['service_id'].isin(active_services)]

                        route_dataframe = filtered_stop_time.groupby('route_id').agg({
                            'trip_id': 'nunique',
                            'block_id': 'nunique',

                        }).reset_index()



                        route_dataframe = route_dataframe.merge(route_df1[['route_id','route_short_name','route_long_name','route_type']],on='route_id',how='left')
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
                        route_dataframe['mode'] = route_dataframe['route_type'].map(route_type_mapping)

                        route_dataframe = route_dataframe.drop('route_type', axis= 1)

                        if input.sort()== "1":

                            sorted_routes = route_dataframe.sort_values(by="trip_id", ascending=False).reset_index(drop=True)
                        else:
                            sorted_routes = route_dataframe.sort_values(by="block_id", ascending=False).reset_index(drop=True)
                        

                        sorted_routes.rename(columns={"trip_id": "no. of trips", "block_id": "no. of blocks"}, inplace=True)
                        sorted_routes.rename(columns={"route_short_name": "short name", "route_long_name": "route name"}, inplace=True)
                        sorted_routes = sorted_routes.drop('short name',axis=1)
                        sorted_routes = sorted_routes.drop('route_id',axis=1)
                        sorted_routes = sorted_routes[['route name','no. of trips', 'no. of blocks','mode']]
                        top_routes = sorted_routes.iloc[:input.n(), :]

                        return render.DataGrid(top_routes.head(100), selection_mode="row", filters=False)

            ui.input_slider("n", "Number of Routes", 1, 10, 5)
            ui.input_radio_buttons(  
                "sort",  
                "",  
                {"1": "Sort by Trips", "2": "Sort by Blocks"},  
            )
         
        with ui.card():

            with ui.card():
                ui.card_header("Day Period")
         


                @render.plot
                def plot_day_period():

                    if input.date():


                        Date_Classification_df['date'] = pd.to_datetime(Date_Classification_df['date']).dt.date


                        selected_date = input.date()  # Ensure date selection updates the table

                        # Fetch active services
                        active_services = Date_Classification_df.loc[Date_Classification_df['date'] == selected_date, 'active_services'].values
                        filtered_stop_time = pd.DataFrame()  # Initialize as empty DataFrame

                        if len(active_services) > 0:
                            active_services = active_services[0]  

                            if isinstance(active_services, str):  
                                active_services = ast.literal_eval(active_services)  # Convert string to list
                            
                            if not isinstance(active_services, list):  
                                active_services = [active_services]  # Ensure it's a list

                            filtered_stop_time = modified_stop_times_df[modified_stop_times_df['service_id'].isin(active_services)]


                        # Assuming 'time_column' is the column containing the time in the format '12:25:04'
                        filtered_stop_time.loc[:, 'arivalTime_seconds'] = filtered_stop_time['arrival_time'].apply(
                            lambda x: sum(int(i) * 60**(2 - idx) for idx, i in enumerate(x.split(':')))
                        )
                        filtered_stop_time.loc[:, 'departureTime_seconds'] = filtered_stop_time['departure_time'].apply(
                            lambda x: sum(int(i) * 60**(2 - idx) for idx, i in enumerate(x.split(':')))
                        )
                        column_order=['route_id','service_id','trip_id','block_id','shape_id','arrival_time','arivalTime_seconds','departureTime_seconds','stop_id','stop_lat','stop_lon','stop_sequence']

                        filtered_trips = filtered_stop_time[column_order]


                        # Start and end time intervals
                        start_time_intervals = [filtered_trips['arivalTime_seconds'].min(), 6 * 3600, 9 * 3600, 15 * 3600, 17 * 3600, 19 * 3600, 22 * 3600]
                        end_time_intervals = start_time_intervals[1:] + [filtered_trips['arivalTime_seconds'].max()]  

                        # Initialize dictionaries to store results
                        trips_in_day_period = {}
                        selected_trips_dict = {}

                        # Iterate through time intervals
                        for start, end in zip(start_time_intervals, end_time_intervals):
                            # Select trips that start within the current interval
                            selected_trips = filtered_trips[
                                (filtered_trips['arivalTime_seconds'] >= start) & 
                                (filtered_trips['arivalTime_seconds'] < end) & 
                                (filtered_trips['stop_sequence'] == 1)
                            ]
                            
                            # Count the number of unique trips within the interval
                            num_trips = selected_trips['trip_id'].nunique()
                            
                            # Calculate the duration of the interval
                            duration = (end - start)/3600

                            last_time_interval = int(start_time_intervals[-1]/3600)

                            if start == last_time_interval*3600:
                                duration = round(selected_trips['arivalTime_seconds'].max()/3600)-start/3600

                            
                            # Store the selected trips in the dictionary
                            day_period_key = f'{start//3600:02d}:00 - {end//3600:02d}:00' if start < last_time_interval * 3600 else f'{start//3600:02d}:00 - End of Service'
                            trips_in_day_period[day_period_key] = {'num_trips': num_trips, 'duration': duration,'num_trip_per_hour': round(num_trips/duration)}
                            


                        # Extract intervals and trips per hour for plotting
                        intervals = list(trips_in_day_period.keys())
                        num_trips_per_hour = [data['num_trip_per_hour'] for data in trips_in_day_period.values()]

                        # Find the index of the maximum value (number of trips per hour)
                        max_index = num_trips_per_hour.index(max(num_trips_per_hour))

                        # Create the bar plot
                        #plt.figure(figsize=(8, 6))  # Set the figure size
                        bars = plt.bar(intervals, num_trips_per_hour, color='skyblue', edgecolor='black', width=0.5)

                        # Highlight the maximum bar in red
                        bars[max_index].set_color('red')
                        bars[max_index].set_edgecolor('black')


                        # Customize the font and appearance
                        plt.xlabel("Day Period", fontsize=12, fontfamily='Times New Roman')
                        plt.ylabel("Number of Trips per Hour", fontsize=12, fontfamily='Times New Roman')
                        plt.xticks(rotation=30, fontsize=10, fontfamily='Times New Roman')  # Rotate the x-axis labels for better readability
                        plt.yticks(fontsize=10, fontfamily='Times New Roman')

                        # Add grid lines for better readability
                        plt.grid(axis='y', linestyle='--', alpha=0.7)

            with ui.card():
                ui.card_header("Trip Frequency of Routes")
                
                
                
                Date_Classification_df['date'] = pd.to_datetime(Date_Classification_df['date']).dt.date  

               
                @render.plot
                def sample_sales_data711():
                    if input.date():
                        selected_date = input.date()  # Ensure date selection updates the table

                        # Fetch active services
                        active_services = Date_Classification_df.loc[Date_Classification_df['date'] == selected_date, 'active_services'].values
                        filtered_stop_time = pd.DataFrame()  # Initialize as empty DataFrame

                        if len(active_services) > 0:
                            active_services = active_services[0]  

                            if isinstance(active_services, str):  
                                active_services = ast.literal_eval(active_services)  # Convert string to list
                            
                            if not isinstance(active_services, list):  
                                active_services = [active_services]  # Ensure it's a list

                            filtered_stop_time = modified_stop_times_df[modified_stop_times_df['service_id'].isin(active_services)]

                        route_dataframe = filtered_stop_time.groupby('route_id').agg({
                            'trip_id': 'nunique',
                            'block_id': 'nunique',

                        }).reset_index()



                        route_dataframe = route_dataframe.merge(route_df1[['route_id','route_short_name','route_long_name','route_type']],on='route_id',how='left')
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
                        route_dataframe['mode'] = route_dataframe['route_type'].map(route_type_mapping)

                        route_dataframe = route_dataframe.drop('route_type', axis= 1)


                    

                   

                        # Create the plot
                        
                        hist_values, bins, patches = plt.hist(route_dataframe['trip_id'], bins=10, color='orange', edgecolor='black')

                        # Add labels above each bar
                        for patch, value in zip(patches, hist_values):
                            x = patch.get_x() + patch.get_width() / 2
                            y = value
                            plt.text(x, y + 0.5, f'{int(value)}', ha='center', va='bottom', fontsize=8)

                        # Customize labels and title
                        plt.xlabel('Number of Trips', fontsize=12)
                        plt.ylabel('Number of Routes', fontsize=12)
                        





