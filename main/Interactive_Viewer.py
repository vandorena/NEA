from bokeh.plotting import figure, show, curdoc
from bokeh.models import ColumnDataSource, Slider, Button, Dropdown
from bokeh.models.callbacks import CustomJS
from bokeh.layouts import column,row
from boats_bokeh import find_boats
import globals
from globals import BUTTON_STYLE


def viewer(doc):

    start_x = 0
    start_y = 0

    end_x = 0
    end_y = 0

    start_x_changed = False
    start_y_changed = False
    end_x_changed = False
    end_y_changed =False

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

    def update_boat(event):
        globals.selected_boat = globals.CURRENT_BOATS[event.item]
        print(globals.selected_boat)#

    def gcr_routing(event):
        nonlocal start_x,start_y,end_x,end_y

    def full_routing(event):
        pass

    def gcr_grib_routing(event):
        pass        

    def full_grib_routing(event):
        pass

    plot = figure(x_range=(-2000000, 2000000), y_range=(1000000, 7000000),
            x_axis_type="mercator", y_axis_type="mercator", height=500,width=1000)

    plot.add_tile("CartoDB Positron", retina=True)

    great_circle_source = ColumnDataSource(data={'x':[], 'y':[]})
    plot.line('x','y', source = great_circle_source, color="red", legend_label="Great Circle Route")
    boat_list = create_boat_list()

    boat_dropdown = Dropdown(label="Select Boat" , button_type="warning", menu=boat_list)
    boat_dropdown.on_event("menu_item_click", update_boat)

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



    layout1 = column(button_Start_Routing_Full,button_Start_Routing_GCR,button_Start_Routing_Full_GRIB,button_Start_Routing_GCR_Grib,boat_dropdown)
    layout_main = row(plot,layout1)
    doc.add_root(layout_main)



