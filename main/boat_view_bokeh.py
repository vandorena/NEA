from globals import CURRENT_BOATS, selected_boat, BUTTON_STYLE
import globals
import bokeh
from bokeh.io import curdoc
from bokeh.layouts import row,column
from bokeh.plotting import figure
from bokeh.models import Button,Div,CustomJS,ColumnDataSource, DataTable, DateFormatter, TableColumn, Plot
import requests
from math import radians,sin,cos


def view_boat(doc):
    if globals.selected_boat is None:
        print("Lol you thought")
        text_dummy_div = Div(text="None")
        text_dummy_div.js_on_change("text",CustomJS(code="window.location.href='/boats'"))
        text_dummy_div.text="no"
        doc.add_root(text_dummy_div)
    else:
        print("yay")

        def find_y(list):
            #"""expects list of [radius,heading]"""
            radius = float(list[0])
            heading = float(list[1])
            return radius * sin(radians(heading))
        
        def find_x(list):
            #"""expects list of [radius,heading]"""
            radius = float(list[0])
            heading = float(list[1])
            return radius * cos(radians(heading))
        
        
        print(f"{globals.selected_boat.data}")
        boat_object = globals.selected_boat
        color_list = ["yellow","red","blue","green","purple","orange","black","pink","brown"]
        plot = figure( width = 1500, height = 900)


        for i in range(0,len(boat_object.data["wind_list"])):
            current_wind = boat_object.data["wind_list"][i]
            listholder = []
            for j in range(0,len(boat_object.data[current_wind])):
                listholder.append([boat_object.data[current_wind][i],boat_object.data["heading_list"][i]])
            xs = list(map(find_x,listholder))
            ys= list(map(find_y, listholder))
            print("xs:", xs)
            print("ys:", ys)
            mod = i%9
            source = ColumnDataSource(data={'x':xs,'y':ys})
            plot.line(source=source,legend_label=f"{current_wind} knts", color=color_list[mod])




        back_boats_button = Button(label="Boats Page",button_type=BUTTON_STYLE["type"][0],width=BUTTON_STYLE["width"],height=BUTTON_STYLE["height"],icon=BUTTON_STYLE["icons"][0])
        back_boats_button.js_on_event('button_click',CustomJS(code="window.location.href='/boats"))

        layout = row(plot,back_boats_button)
        doc.add_root(layout)

