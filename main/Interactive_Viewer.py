from bokeh.plotting import figure, show, curdoc
from bokeh.models import ColumnDataSource, Slider, Button, Dropdown, Div, FileInput
from bokeh.models.callbacks import CustomJS
from bokeh.layouts import column,row, layout
from boats_bokeh import find_boats
import globals
from globals import BUTTON_STYLE
from grib_manager_bokeh import find_gribsV2


def viewer(doc):

    start_x = 0
    start_y = 0

    end_x = 0
    end_y = 0

    start_x_changed = False
    start_y_changed = False
    end_x_changed = False
    end_y_changed =False

    grib_uploaded = False

    def create_boat_list()-> list:
        find_boats()
        boat_list =[]
        for i in range(0,len(globals.CURRENT_BOATS["boat_list"])):
            boatname = globals.CURRENT_BOATS["boat_list"][i]
            print(boatname)
            print(globals.CURRENT_BOATS[boatname])
            ntuple = (boatname)
            boat_list.append(ntuple)
        return boat_list
    
    def create_grib_list()-> list:
        find_gribsV2()
        grib_list =[]
        for i in range(0,len(globals.CURRENT_GRIBS["grib_list"])):
            gribname = globals.CURRENT_GRIBS["grib_list"][i]
            print(gribname)
            print(globals.CURRENT_BOATS[gribname])
            ntuple = (gribname)
            grib_list.append(ntuple)
        return grib_list

    def update_boat(event):
        nonlocal current_boat
        globals.selected_boat = globals.CURRENT_BOATS[event.item]
        print(globals.selected_boat)
        current_boat.text = f"Current Boat: {event.item}"

    def update_grib(event):
        nonlocal current_grib
        globals.selected_grib = globals.CURRENT_GRIBS[event.item]
        print(globals.selected_grib)
        current_grib.text = f"Current GRIB: {event.item}"

    def gcr_routing(event):
        nonlocal start_x,start_y,end_x,end_y

    def full_routing(event):
        pass

    def gcr_grib_routing(event):
        pass        

    def full_grib_routing(event):
        pass

    plot = figure(x_range=(-2000000, 2000000), y_range=(1000000, 7000000),
            x_axis_type="mercator", y_axis_type="mercator", width = 1500, height = 900)

    plot.add_tile("CartoDB Positron", retina=True)

    great_circle_source = ColumnDataSource(data={'x':[], 'y':[]})
    plot.line('x','y', source = great_circle_source, color="red", legend_label="Great Circle Route")
    
    boat_list = create_boat_list()
    grib_list = create_grib_list()

    boat_dropdown = Dropdown(label="Select Boat" , button_type="warning", menu=boat_list)
    boat_dropdown.on_event("menu_item_click", update_boat)

    grib_dropdown = Dropdown(label="Select Grib" , button_type="warning", menu=grib_list)
    grib_dropdown.on_event("menu_item_click", update_grib)

    current_boat = Div(text="You have not selected a boat", height= 70, width = 300)
    current_grib = Div(text="You have not selected a GRIB file", height  = 70, width= 300)


    grib_file_input = FileInput(accept="<.grib>,<.grib2>,<.grb>")

    button_Start_Routing_Full= Button(
        label="Start Routing",
        button_type=BUTTON_STYLE["type"][1],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    button_Start_Routing_Full.on_event('button_click', full_routing)

    button_Start_Routing_Full_GRIB= Button(
        label="Start Routing",
        button_type=BUTTON_STYLE["type"][2],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    button_Start_Routing_Full_GRIB.on_event('button_click', full_grib_routing)

    button_Start_Routing_GCR= Button(
        label="Find Great Circle Route",
        button_type=BUTTON_STYLE["type"][1],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    button_Start_Routing_GCR.on_event('button_click', gcr_routing)

    button_Start_Routing_GCR_Grib= Button(
        label="Find Great Circle Route using GRIB",
        button_type=BUTTON_STYLE["type"][2],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    button_Start_Routing_GCR_Grib.on_event('button_click', gcr_grib_routing)

    button_home= Button(
        label="Homepage",
        button_type=BUTTON_STYLE["type"][3],
        width=(BUTTON_STYLE["width"]//3),
        height=(BUTTON_STYLE["height"]//2),
        icon=BUTTON_STYLE["icons"][0]
        )
    button_home.js_on_event('button_click', CustomJS(code="window.location.href='/'"))

    button_enable_grib = Button(
        label="Enable Grib Mode",
        button_type=BUTTON_STYLE["type"][3],
        width=(BUTTON_STYLE["width"]//3),
        height=(BUTTON_STYLE["height"]//2),
        icon=BUTTON_STYLE["icons"][0]
        )
    
    def enable_grib(event):
        update_root(enable_grib=True)

    button_enable_grib.on_event("button_click",enable_grib)

    def update_root(enable_grib: bool):
        doc.clear()
        if not enable_grib:
            bottom_row = row(button_home, button_enable_grib)
            layout1 = column(current_boat, button_Start_Routing_Full,button_Start_Routing_GCR,boat_dropdown,bottom_row)
        else:
            bottom_row = row(button_home, button_disable_grib)
            layout1 = column(current_boat, button_Start_Routing_Full_GRIB, button_Start_Routing_GCR_Grib, boat_dropdown,grib_file_input,bottom_row)

        
        layout_main = row(plot,layout1)
        doc.add_root(layout_main)

    def update_root_false():
        update_root(False)
    
    button_disable_grib = Button(
        label="Disable Grib Mode",
        button_type=BUTTON_STYLE["type"][3],
        width=(BUTTON_STYLE["width"]//3),
        height=(BUTTON_STYLE["height"]//2),
        icon=BUTTON_STYLE["icons"][0]
        )
    
    button_disable_grib.on_event("button_click",update_root_false)
    
    update_root(False)

  



