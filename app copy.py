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
            height: 60px;
        }


        .logo-container {
            margin-right: 5px;
            height: 100%;
            padding: 10px;
        
        }

        .logo-container img {
            height: 40px;
        }

        .title-container h2 {
            color: white;
            padding: 5px;
            margin: 0;
        
        }


        body {

            background-color: #5DADE2;
        
        
        }


        .modebar{
            display: none;
        
        }

    """
)



def style_plotly_chart(fig, yaxis_title):
    fig.update_layout(
        xaxis_title='',
        yaxis_title=yaxis_title,
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        coloraxis_showscale=False,
        font=dict(
            family='Arial',
            size=12,
            color='#4C78A8'
        )
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig

ui.page_opts(window_title="Sales Dashboard - Video 5 0f 5", fillable=False)





with ui.div(class_="header-container"):
    with ui.div(class_="logo-container"):

        @render.image  
        def image():
            here = Path(__file__).parent
            img = {"src": here / "images/shiny-logo.png"}  
            return img 

    with ui.div(class_="title-container"):
        ui.h2("Sales Dashboard - Video 5 of 5")
############################################
# with ui.card():
#     ui.card_header("General Information")
#     with ui.layout_columns(col_widths={"sm": (4,4)}):

#         with ui.value_box(
#             showcase=faicons.icon_svg("train-subway", width="50px"),
#             theme="bg-gradient-orange-red",
#         ):
#             "Save"

#             @render.ui  
#             def save():  
#                 return f"${(1 - 200 / 100) * 70:.1f} Billion"  

#         with ui.value_box(
#             showcase=faicons.icon_svg("hand-holding-dollar", width="50px"),
#             theme="bg-gradient-blue-purple",
#         ):
#             "Donate"

#             @render.ui  
#             def donate():  
#                 return f"${400 / 100 * 70:.1f} Billion"  

############################################







with ui.card():
    ui.card_header("Sales by city 2023")


    with ui.layout_sidebar():  

        
        with ui.sidebar(bg="#f8f8f8",open='open'):  
       

            ui.input_selectize(  
                "city",  
                "Select a city:",  
                ['Dallas (TX)', 'Boston (MA)', 'Los Angeles (CA)', 'San Francisco (CA)', 'Seattle (WA)', 'Atlanta (GA)', 'New York City (NY)', 'Portland (OR)', 'Austin (TX)', 'Portland (ME)'],  
                multiple=False,
                selected = 'Boston (MA)'
            ),


        
        @render_altair
        def sales_over_times():
            df = df1
            sales = df.groupby(['city', 'month'])['quantity_ordered'].sum().reset_index()
            sales_by_city = sales[sales['city'] == input.city()]
            
            month_orders = list(calendar.month_name[1:])

            font_props = alt.Axis(labelFont='Arial',labelColor='#4C78A8',titleFont='Arial', titleColor='#4C78A8', tickSize=0, labelAngle=0)
            sales_by_city['month'] = pd.Categorical(sales_by_city['month'], categories=month_orders, ordered=True)
            
            chart = alt.Chart(sales_by_city).mark_bar(color='#3485BF').encode(
                x=alt.X('month', sort=month_orders, title='Month', axis=font_props),
                y=alt.Y('quantity_ordered', title='Quantity Ordered', axis=font_props),
                tooltip=['month', 'quantity_ordered']
            ).properties(
                title=f"Sales over time -- {input.city()}"
            ).configure_axis(
                    grid=False
            ).configure_title(
                font='Arial',
                color='#4C78A8'
            )
            
            return chart


with ui.layout_columns(col_widths={"sm": (7,5)}):



    with ui.navset_card_underline(id="tab", placement='above', footer=ui.input_slider("n", "Number of Items", 0, 20, 5)):  
        with ui.nav_panel("Top Sellers", icon= icon_svg("chart-line")): 
            
            
            @render_plotly
            def plot_top_sellers():
                df = df1.copy()
                top_sales = df.groupby('product')['quantity_ordered'].sum().nlargest(input.n()).reset_index()
                fig = px.bar(top_sales, x='product', y='quantity_ordered',
                             color='quantity_ordered',color_continuous_scale='Blues')
                #fig.update_traces(marker_color=color())

                fig = style_plotly_chart(fig, 'Quantity Ordered')



                return fig



        with ui.nav_panel("Top Sellers Value", icon= icon_svg("chart-line")):

           @render_plotly
           def plot_top_sellers_value():
                df = df1.copy()
                
                top_values = df.groupby('product')['value ($)'].sum().nlargest(input.n()).reset_index()
                fig = px.bar(top_values, x='product', y='value ($)',
                                color='value ($)',color_continuous_scale='Blues')
                    #fig.update_traces(marker_color=color())

                fig = style_plotly_chart(fig, 'Total Sales ($)')

                return fig


        with ui.nav_panel("Loswet Sellers", icon= icon_svg("chart-line")):

            @render_plotly
            def plot_low_sellers():
                df = df1.copy()
                top_sales = df.groupby('product')['quantity_ordered'].sum().nsmallest(input.n()).reset_index()
                fig = px.bar(top_sales, x='product', y='quantity_ordered',
                                color='quantity_ordered',color_continuous_scale='Reds')
                    #fig.update_traces(marker_color=color())

                fig = style_plotly_chart(fig, 'Quantity Ordered')

                return fig



        with ui.nav_panel("Lowest Sellers Value", icon= icon_svg("chart-line")):


           @render_plotly
           def plot_low_sellers_value():
                df = df1.copy()
                
                top_values = df.groupby('product')['value ($)'].sum().nsmallest(input.n()).reset_index()
                fig = px.bar(top_values, x='product', y='value ($)',
                                color='value ($)',color_continuous_scale='Reds')
                    #fig.update_traces(marker_color=color())

                fig = style_plotly_chart(fig, 'Total Sales ($')

                return fig


        # with ui.nav_menu("Other links"):
        #     with ui.nav_panel("D"):
        #         "Page D content"

    

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




    
   
with ui.card():
    ui.card_header("Sales by Location Map")
    "Content Here"

    @render.ui

    def plot_us_heatmap():
        df = df1
        

        heatmap_data = df[['lat','long','quantity_ordered']].values
        
        map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
        
        blue_gradient = {
            0.0: "rgb(227, 242, 253)",  # #E3F2FD
            0.2: "rgb(187, 222, 251)",  # #BBDEFB
            0.4: "rgb(100, 181, 246)",  # #64B5F6
            0.6: "rgb(66, 165, 245)",   # #42A5F5
            0.8: "rgb(33, 150, 243)",   # #2196F3
            1.0: "rgb(25, 118, 210)"    # #1976D2
        }


        HeatMap(heatmap_data).add_to(map)


        return map


with ui.card():
    ui.card_header("Sample Sales Dates")

    @render.data_frame
    def sample_sales_data():
            
        return render.DataGrid(df1.head(100), selection_mode="row", filters=True)
    
  
