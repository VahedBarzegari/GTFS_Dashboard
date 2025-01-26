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

            background-color: #ff7547;
        
        
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
    with ui.layout_columns(col_widths={"sm": (4,4)}):

        with ui.value_box(
            showcase=faicons.icon_svg("train-subway", width="50px"),
            theme="bg-gradient-orange-red",
        ):
            "Save"

            @render.ui  
            def save():  
                return f"${(1 - 200 / 100) * 70:.1f} Billion"  

        with ui.value_box(
            showcase=faicons.icon_svg("hand-holding-dollar", width="50px"),
            theme="bg-gradient-blue-purple",
        ):
            "Donate"

            @render.ui  
            def donate():  
                return f"${400 / 100 * 70:.1f} Billion"  

############################################






