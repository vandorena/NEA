from boats import Boat
from globals import CURRENT_BOATS, BUTTON_STYLE, selected_boat
from bokeh.models import Button, Dropdown
from bokeh.layouts import row, column
from bokeh.models import CustomJS
from bokeh.io import curdoc
import os


def find_boats():
    global CURRENT_BOATS
    with open(os.path.join("Boats","Boat_saves.txt"),"r") as file:
        boats = file.readlines()
    for i in range(0,len(boats)):
        line_content = boats[i].split()
        boat = Boat(line_content[0])
        CURRENT_BOATS["boat_list"].append(line_content[0])
        boat.add_polar(line_content[1])
        CURRENT_BOATS[line_content[0]] = boat
        boat = None

def boat_button(boat):
    global selected_boat 
    selected_boat = boat
    return CustomJS(code="window.location.href='/view_boat'")


def boats(doc):
    
    """Need to work on how to dynamically create buttons based on how many boats are there."""


    def create_boat_list()-> list:
        find_boats()
        boat_list =[]
        for i in range(0,len(CURRENT_BOATS["boat_list"])):
            boatname = CURRENT_BOATS["boat_list"][i]
            print(boatname)
            print(CURRENT_BOATS[boatname])
            ntuple = (boatname)
            boat_list.append(ntuple)
        return boat_list
    
    boat_menu = create_boat_list()

    def select_boat(event):
        global selected_boat
        selected_boat = CURRENT_BOATS[event.item]
        print(selected_boat)
        print("got this :)")

    
    add_boat = Button(
        label="Add a New Boat",
        button_type=BUTTON_STYLE["type"][0],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    add_boat.js_on_event('button_click',CustomJS(code="window.location.href='/new_boat'"))

    boat_dropdown = Dropdown(label="Select Boat" , button_type="warning", menu=boat_menu)
    boat_dropdown.on_event("menu_item_click", select_boat)
    boat_dropdown.js_on_event("menu_item_click",CustomJS(code="window.location.href='/view_boat'"))

    layout1 = row(add_boat,boat_dropdown)
    doc.add_root(layout1)
    



#find_boats()
##curdoc().clear()
#boats(curdoc())