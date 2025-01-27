import asyncio
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

from datacode import df1
from GTFS_core_data import routes_df, agency_df, stops_df, stop_times_df, calendar_df, calendar_dates_df, shapes_df, trips_df,shape_route_df, route_type_df

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
    
    ui.card_header("General Information", style="text-align: center; font-size: 24px;")
    with ui.layout_columns(col_widths={"sm": (3,3,3,3)}):

        with ui.value_box(
            showcase=faicons.icon_svg("calendar-days", width="50px"),
            theme="bg-gradient-green-red",
        ):
            "Start Date"

            @render.ui  
            def datestartfun():  
                return "November 17, 2024"  
            

        with ui.value_box(
            showcase=faicons.icon_svg("calendar-days", width="50px"),
            theme="bg-gradient-orange-red",
        ):
            "End Date"

            @render.ui  
            def dateendfun():  
                return "December 22, 2024"  
            


        with ui.value_box(
            showcase=faicons.icon_svg("road", width="50px"),
            theme="bg-gradient-yellow-purple",
        ):
            "Number of routes"

            @render.ui  
            def routefun():  
                return "215"  
            

        with ui.value_box(
            showcase=faicons.icon_svg("train-subway", width="50px"),
            theme="bg-gradient-blue-purple",
        ):
            "Number of Stops"

            @render.ui  
            def stopfun():  
                return "9308"  

############################################

with ui.layout_columns(
    col_widths={"sm": (4, 8)}
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
            mode_color_mapping = {
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
            else:
                ax = shape_route_df

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
                bottom: 20px; left: 20px; width: 200px; height: auto; 
                background-color: white; z-index:9999; font-size:14px;
                border-radius: 5px; padding: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            ">
            <b>Legend</b><br>
            ''' + ''.join([f'<div style="display: flex; align-items: center;"><div style="width: 15px; height: 15px; background: {color}; margin-right: 5px;"></div>{mode}</div>' for mode, color in mode_color_mapping.items()]) + '</div>'

            m.get_root().html.add_child(folium.Element(legend_html))

            return m


with ui.layout_columns(col_widths={"sm": (8,4)}, height='500px'):



    with ui.navset_card_underline(id="tab", placement='above', title="GTFS Feeds"):

        

        with ui.nav_panel("agency"): 

            with ui.card():
                

                @render.data_frame
                def sample_sales_data1():
                        
                    return render.DataGrid(agency_df.head(100), selection_mode="row", filters=True)
            
            
            



        with ui.nav_panel("Calendar"):

            with ui.card():
                

                @render.data_frame
                def sample_sales_data2():
                        
                    return render.DataGrid(calendar_df.head(100), selection_mode="row", filters=True)
            

        with ui.nav_panel("Calendar_dates"):

            with ui.card():
                

                @render.data_frame
                def sample_sales_data3():
                        
                    return render.DataGrid(calendar_dates_df.head(100), selection_mode="row", filters=True)
            


        with ui.nav_panel("Routes"):

            with ui.card():
                

                @render.data_frame
                def sample_sales_data4():
                        
                    return render.DataGrid(routes_df, selection_mode="row", filters=True)
            



        with ui.nav_menu("Other links"):
             with ui.nav_panel("Stops"):
        #         "Page D content"
                with ui.card():
                    

                    @render.data_frame
                    def sample_sales_data5():
                            
                        return render.DataGrid(stops_df.head(100), selection_mode="row", filters=True)
 
             with ui.nav_panel("Stop times"):
        #         "Page D content"
                with ui.card():
                    

                    @render.data_frame
                    def sample_sales_data6():
                            
                        return render.DataGrid(stop_times_df.head(100), selection_mode="row", filters=True)
    

    with ui.card():
        ui.card_header("Sales by time of day")
        @render.plot
        def plot_sales_by_time():
            df = df1
            sales_by_hour = df['hour'].value_counts().reindex(np.arange(0,24), fill_value=0)

            heatmap_data = sales_by_hour.values.reshape(24,1)
            sns.heatmap(heatmap_data,
                        annot=True,
                        fmt="d",
                        cmap="Blues",
                        cbar=False,
                        xticklabels=[],
                        yticklabels=[f"{i}:00" for i in range(24)])
            

            #plt.title("Number of Orders by Hour of Day")
            plt.xlabel("Order Count", color='#4C78A8', fontname='Arial')
            plt.ylabel("Hour of Day", color='#4C78A8', fontname='Arial')

            plt.yticks(color='#4C78A8', fontname='Arial')
            plt.xticks(color='#4C78A8', fontname='Arial')




