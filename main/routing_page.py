import bokeh
from bokeh.io import curdoc
from bokeh.models import Button, Div, Dropdown, Paragraph, DatetimeRangeSlider
from globals import selected_boat,selected_grib,BUTTON_STYLE,CURRENT_BOATS,CURRENT_SUBFOLDERS, CURRENT_ROUTINGS
from bokeh.layouts import column,row
from boats_bokeh import find_boats
from grib_manager_bokeh import find_gribs
from bokeh.events import MenuItemClick

routing_started = False

def main(doc):
    global routing_started
    infinite_while = False
    while not infinite_while:
        if routing_started == True:
            post(doc)
        else:
            pre(doc)



def post(doc):
    global selected_boat,CURRENT_ROUTINGS
    boat_Div = Div(text=f"<p><b>{selected_boat}</p></b>")
    grib_Div = Div(test=f"<p><b>{selected_grib}</p></b>")

    current_routing = CURRENT_ROUTINGS[CURRENT_ROUTINGS["routing_list"][-1]]

    datetime_slider = DatetimeRangeSlider(start=current_routing.start_datetime,end=current_routing.path_data["times"][-1])

    
    navigation_buttons = create_navigation_buttons()
    right_column = (navigation_buttons,boat_Div,grib_Div)



def pre(doc):
    start_routing_button = Button(
        label="Start Routing",
        button_type=BUTTON_STYLE["type"][2],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    
    
    grib_dropdown = Dropdown(label="Select Grib",style="default",menu=create_menu_gribs())
    grib_dropdown.on_event(MenuItemClick,update_grib_selected)
    
    boat_dropdown = Dropdown(label="Select Boat",style="default",menu=create_menu_boats())
    boat_dropdown.on_event(MenuItemClick,update_boats_selected)

    para = Paragraph("<h1>Route Information</h1><br><h2>No Route Selected</h2>")

    navigation_buttons = create_navigation_buttons()
    right_column = column(navigation_buttons,boat_dropdown,grib_dropdown,start_routing_button,para)

def update_grib_selected(event):
    global selected_grib
    selected_grib = event.item

def update_boats_selected(event):
    global selected_boat
    selected_boat = event.item

def create_menu_boats():
    find_boats()
    menu = []
    for i in range(0, len(CURRENT_BOATS["boat_list"])):
        tuple_add = (CURRENT_BOATS["boat_list"][i],CURRENT_BOATS["boat_list"][i])
        menu.append(tuple_add)
    return menu

def create_menu_gribs():
    find_gribs()
    menu = []
    for i in range(0, len(CURRENT_SUBFOLDERS["subfolder_list"])):
        tuple_add = (CURRENT_SUBFOLDERS["subfolder_list"][i],CURRENT_SUBFOLDERS["subfolder_list"][i])
        menu.append(tuple_add)
    return menu

def create_navigation_buttons():
    grib_page_button = Button(
        label="Grib Page",
        button_type=BUTTON_STYLE["type"][0],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    
    boat_page_button = Button(
        label="Boat Page",
        button_type=BUTTON_STYLE["type"][0],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    
    main_page_button = Button(
        label="Main Page",
        button_type=BUTTON_STYLE["type"][0],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    
    nav = row(grib_page_button,boat_page_button,main_page_button)

    return nav