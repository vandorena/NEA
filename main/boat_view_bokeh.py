from globals import CURRENT_BOATS, selected_boat, BUTTON_STYLE
import globals
import bokeh
from bokeh.io import curdoc
from bokeh.layouts import row,column
from bokeh.plotting import figure
from bokeh.models import Button,Div,CustomJS,ColumnDataSource, DataTable, DateFormatter, TableColumn, Plot, Dropdown
import requests
from math import radians,sin,cos
from boats_bokeh import find_boats

found_boat = False

def view_boat(doc):
    global found_boat


    def create_boat_list()-> list:
        find_boats()
        boat_list =[]
        for i in range(0,len(CURRENT_BOATS["boat_list"])):
            boatname = CURRENT_BOATS["boat_list"][i]
            print(boatname)
            print("im stuck")
            print(CURRENT_BOATS[boatname])
            ntuple = (boatname)
            boat_list.append(ntuple)
        return boat_list






    def find_y(list):
        #"""expects list of [radius,heading]"""
        radius = float(list[0])
        heading = float(list[1])
        # print(heading)
        return radius * cos(radians(heading))
    
    def find_x(list):
        #"""expects list of [radius,heading]"""
        radius = float(list[0])
        heading = float(list[1])
        return radius * sin(radians(heading))
    
    
    # print(f"{globals.selected_boat.data}")
    boat_object = globals.selected_boat
    color_list = ["yellow","red","blue","green","purple","orange","black","pink","brown"]
    plot = figure( width = 1500, height = 900,match_aspect=True)

    boat_menu = create_boat_list()

    def select_boat(event):
        globals.selected_boat = CURRENT_BOATS[event.item]
        boat_object = CURRENT_BOATS[event.item]
        print(selected_boat)
        print("got this :)")
        found_boat = True
        
    
    add_boat = Button(
        label="Homepage",
        button_type=BUTTON_STYLE["type"][0],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    add_boat.js_on_event('button_click',CustomJS(code="window.location.href='/'"))

    boat_dropdown = Dropdown(label="Select Boat" , button_type="warning", menu=boat_menu)
    boat_dropdown.on_event("menu_item_click",select_boat)

    if boat_object is not None:
        for i in range(0,len(boat_object.data["wind_list"])):
            current_wind = boat_object.data["wind_list"][i]
            listholder = []
            for j in range(0,len(boat_object.data[current_wind])):
                #print(f"current_wind_len = {len(boat_object.data[current_wind])}")
                listholder.append([boat_object.data[current_wind][j],boat_object.data["heading_list"][j]])
            xs = list(map(find_x,listholder))
            ys= list(map(find_y, listholder))
            #print("xs:", xs)
            #print("ys:", ys)
            mod = i%9
            source = ColumnDataSource(data={'x':xs,'y':ys})
            plot.line(source=source,legend_label=f"{current_wind} knts", color=color_list[mod],line_width=2)
    # print(boat_object.data["heading_list"])



    back_button = Button(label="Home Page",button_type=BUTTON_STYLE["type"][0],width=BUTTON_STYLE["width"],height=BUTTON_STYLE["height"],icon=BUTTON_STYLE["icons"][0])
    back_button.js_on_event('button_click',CustomJS(code="window.location.href='/'"))

    if found_boat:
        layout = row(plot,back_button)
    else:
        layout = row(add_boat,boat_dropdown)
    
    doc.add_root(layout)

