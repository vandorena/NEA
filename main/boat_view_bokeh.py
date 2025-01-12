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
            #print(boatname)
            #print("im stuck")
            #print(CURRENT_BOATS[boatname])
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
    
    color_list = ["yellow","red","blue","green","purple","orange","black","pink","brown"]
    

    boat_menu = create_boat_list()

    def update():
        if found_boat and globals.selected_boat:
            boat_object = globals.selected_boat
            plot = figure( width = 1500, height = 900,match_aspect=True)
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

            selected_boat_div = Div(text=f"You have currently selected: {boat_object.data['name']}")
            polar_diagram_explainer_div = Div(text="")
            polar_diagram_explainer_div.text =   """This plot shows how far your boat will go in any direction, \n
            or windspeed over the course of one hour."""
            polar_diagram_explainer_div_2 = Div(text="wind is coming from the top.")

            back_button = Button(label="Home Page",button_type=BUTTON_STYLE["type"][0],width=BUTTON_STYLE["width"],height=BUTTON_STYLE["height"],icon=BUTTON_STYLE["icons"][0])
            back_button.js_on_event('button_click',CustomJS(code="window.location.href='/'"))

            boat_dropdown = Dropdown(label="Select Boat" , button_type="warning", menu=boat_menu)

            def select_boat(event):
                global found_boat
                globals.selected_boat = CURRENT_BOATS[event.item]
               # print(selected_boat)
                #print("got this :)")
                found_boat = True
                update()

            boat_dropdown.on_event("menu_item_click",select_boat)

            doc.clear()
            doc.add_root(row(plot,column(selected_boat_div,polar_diagram_explainer_div,polar_diagram_explainer_div_2,back_button,boat_dropdown)))
        else:
            add_boat = Button(
            label="Homepage",
            button_type=BUTTON_STYLE["type"][0],
            width=BUTTON_STYLE["width"],
            height=BUTTON_STYLE["height"],
            icon=BUTTON_STYLE["icons"][0]
            )
            add_boat.js_on_event('button_click',CustomJS(code="window.location.href='/'"))

            boat_dropdown = Dropdown(label="Select Boat" , button_type="warning", menu=boat_menu)

            def select_boat(event):
                global found_boat
                globals.selected_boat = CURRENT_BOATS[event.item]
                #print(selected_boat)
                #print("got this :)")
                found_boat = True
                update()

            boat_dropdown.on_event("menu_item_click",select_boat)

            boat_selection_explainer_div = Div(text="Select a boat below:")

            doc.clear()
            doc.add_root(column(add_boat,boat_selection_explainer_div,boat_dropdown))
    update()

