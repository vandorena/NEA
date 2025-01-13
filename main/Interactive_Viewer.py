from bokeh.plotting import figure, show, curdoc
from bokeh.models import ColumnDataSource, Slider, Button, Dropdown, Div, FileInput, TapTool, TextInput
from bokeh.models.callbacks import CustomJS
from bokeh.layouts import column,row, layout
from boats_bokeh import find_boats
import globals
from globals import BUTTON_STYLE
from grib_manager_bokeh import find_gribsV2
from bokeh.events import Tap
import numpy as np

def viewer(doc):

    start_x = 0
    start_y = 0

    end_x = 0
    end_y = 0

    tap_count = 0

    start_x_changed = False
    start_y_changed = False
    end_x_changed = False
    end_y_changed =False

    grib_uploaded = False

    input_warning = False

    x_input_nonlocal = ""
    y_input_nonlocal = ""

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

    def update_x_input(attr,old,new):
        nonlocal x_input_nonlocal
        x_input_nonlocal = new

    def update_y_input(attr,old,new):
        nonlocal y_input_nonlocal
        y_input_nonlocal = new

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
    
    plot.add_tools(TapTool())

    pin_point_source = ColumnDataSource(data={'x':[],'y':[],'color':[]})
    plot.scatter(x='x',y='y',source=pin_point_source,color='color',size=10)

    great_circle_source = ColumnDataSource(data={'x':[], 'y':[]})
    plot.line(x='x',y='y', source = great_circle_source, color="red", legend_label="Great Circle Route")

    optimum_route_source = ColumnDataSource(data={'x':[],'y':[]})
    plot.line(x='x',y='y',source=optimum_route_source,color='pink')
    
    boat_list = create_boat_list()
    grib_list = create_grib_list()

    boat_dropdown = Dropdown(label="Select Boat" , button_type="warning", menu=boat_list)
    boat_dropdown.on_event("menu_item_click", update_boat)

    grib_dropdown = Dropdown(label="Select Grib" , button_type="warning", menu=grib_list)
    grib_dropdown.on_event("menu_item_click", update_grib)

    current_boat = Div(text="You have not selected a boat", height= 70, width = 300)
    current_grib = Div(text="You have not selected a GRIB file", height  = 70, width= 300)

    input_warning_div = Div(text="")

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
    
    explainer_div = Div(text="<h1>Select a start and end point</h1><br>")

    x_input_div = Div(text="<h2>Enter your starting X coordinate below (longitude):</h2><br>")
    x_input = TextInput(title = 'X:')
    x_input.on_change('value',update_x_input)

    y_input_div = Div(text="<h2>Enter your starting Y coordinate below (latitude):</h2><br>")
    y_input = TextInput(title = 'Y:')
    y_input.on_change('value',update_y_input)

    point_enter_button = Button(
        label="Create Starting Point",
        button_type=BUTTON_STYLE["type"][2],
        width=(BUTTON_STYLE["width"]),
        height=(BUTTON_STYLE["height"]//2),
        icon=BUTTON_STYLE["icons"][0]
        )
    

    def enable_grib(event):
        update_root(enable_grib=True)

    button_enable_grib.on_event("button_click",enable_grib)

    def web_mercator_to_lat_lon(x:float,y:float):
        radius_of_earth_Spherical_Projection = 6378137
        new_x_lon = np.degrees(x / radius_of_earth_Spherical_Projection)
        new_y_lat = np.degrees(2 * np.arctan(np.exp(y / radius_of_earth_Spherical_Projection)) - np.pi / 2)
        return new_y_lat, new_x_lon

    def lat_lon_to_web_mercator(lat:float,lon:float):
        radius_of_earth_Spherical_Projection = 6378137
        x = np.radians(lon) * radius_of_earth_Spherical_Projection
        y = radius_of_earth_Spherical_Projection * np.log(np.tan((np.radians(lat)+np.pi/2)/2))
        return x,y

    def update_lines():
        pass

    def update_div():
        nonlocal start_x,start_y, end_x , end_y, start_x_changed,start_y_changed,end_x_changed,end_y_changed,x_input_div,y_input_div
        #print(f"start_x_changed: {start_x_changed}, start_y_changed: {start_y_changed}, end_x_changed: {end_x_changed}, end_y_changed: {end_y_changed}")
        if not start_x_changed and not start_y_changed and not end_x_changed and not end_y_changed:
            explainer_div.text = "<h1>Select a start and end point</h1><br>"
            x_input_div.text = "<h2>Enter your starting X coordinate below (longitude):</h2><br>"
            y_input_div.text ="<h2>Enter your starting Y coordinate below (latitude):</h2><br>"
        elif start_x_changed and start_y_changed and not end_x_changed and not end_y_changed:
            y_holder_1 , x_holder_1 = web_mercator_to_lat_lon(start_x,start_y)
            explainer_div.text = (f"<h1> You have not selected an end point</h1><br>"
                             f"<b>Starting Latitude:</b> {y_holder_1:.5f} <br>"
                             f"<b>Starting Longitude:</b> {x_holder_1:.5f} <br>")
            x_input_div.text = f"<h2> Input your end point's X coordinate (longitude): </h2><br>"
            y_input_div.text = f"<h2> Input your end point's Y coordinate (latitude): </h2><br>"
        elif start_x_changed and start_y_changed and end_x_changed and end_y_changed:
            y_holder_1, x_holder_1 = web_mercator_to_lat_lon(start_x,start_y)
            y_holder_2, x_holder_2 = web_mercator_to_lat_lon(end_x,end_y)
            explainer_div.text = (f"<b>Starting Latitude:</b> {y_holder_1:.5f} <br>"
                                  f"<b>Starting Longitude:</b> {x_holder_1:.5f} <br>"
                                  f"<b>End Latitude:</b> {y_holder_2:.5f}<br>"
                                  f"<b>End Longitude;</b> {x_holder_2:.5f}<br>")
            x_input_div.text = f"<h1> Input is disabled, click map to enable and reset. </h1><br>"
            y_input_div.text = ""

        else:
            print("This shouldn't do this Interactive Viewer.py line 188")
        if input_warning:
            input_warning_div.text = "<h1> Only number inputs are allowed.</h1><br> <b> Ensure all inputs are of decimal form, i.e. 51.231323</b><br>"
        else:
            input_warning_div.text = ""

    def manual_input(event):
        nonlocal tap_count, start_x,start_y,end_x,end_y,start_x_changed,start_y_changed,end_x_changed,end_y_changed,input_warning, x_input_nonlocal,y_input_nonlocal,x_input,y_input
        original_tap_count = tap_count
        try:
            lon,lat = float(x_input_nonlocal),float(y_input_nonlocal)
            tap_count += 1
            x,y = lat_lon_to_web_mercator(lat,lon)
            if tap_count == 1:
                pin_point_source.data = {'x':[], 'y':[], 'color':[]}
                start_x = x
                start_y= y
                plot.scatter(x=[start_x],y=[start_y],size=10,fill_color="red",line_color="yellow",line_width=1)
                start_x_changed = True
                start_y_changed = True
                update_div()
                update_lines()
            elif tap_count == 2:
                pin_point_source.data= {'x':[],'y':[],'color':[]}
                end_x = x
                end_y = y
                end_x_changed = True
                end_y_changed = True
                plot.scatter(x=[end_x],y=[end_y],size=10,fill_color = 'blue',line_color="yellow",line_width=1)
                update_div()
                update_lines()
            
            elif tap_count == 3:
                tap_count = original_tap_count
            x_input.value = ""
            y_input.value = ""
        except ValueError:
            tap_count = original_tap_count
            input_warning = True
            update_div()
    
    def on_tap(event):
        nonlocal tap_count, start_x,start_y,end_x,end_y,start_x_changed,start_y_changed,end_x_changed,end_y_changed
        lon,lat = event.x,event.y
        tap_count +=1
        if tap_count == 1:
            pin_point_source.data = {'x':[], 'y':[], 'color':[]}
            start_x = lon
            start_y= lat
            plot.scatter(x=[start_x],y=[start_y],size=10,fill_color="red",line_color="yellow",line_width=1)
            start_x_changed = True
            start_y_changed = True
            update_div()
            update_lines()
        elif tap_count == 2:
            pin_point_source.data= {'x':[],'y':[],'color':[]}
            end_x = lon
            end_y = lat
            end_x_changed = True
            end_y_changed = True
            plot.scatter(x=[end_x],y=[end_y],size=10,fill_color = 'blue',line_color="yellow",line_width=1)
            update_div()
            update_lines()
            
        elif tap_count == 3:
            pin_point_source.data = {'x':[],'y':[],'colors':[]}
            plot.renderers = []
            plot.add_tile("CartoDB Positron", retina=True)
            tap_count = 0
            start_x = 0
            end_x = 0
            start_y = 0
            end_y = 0
            start_x_changed = False
            start_y_changed = False
            end_x_changed = False
            end_y_changed = False
            update_div()
            update_lines()

    plot.on_event(Tap,on_tap)
    point_enter_button.on_event("button_click",manual_input)

    manual_inputs = column(x_input_div,x_input,y_input_div,y_input,point_enter_button)

    def update_root(enable_grib: bool):
        doc.clear()
        if not enable_grib:
            bottom_row = row(button_home, button_enable_grib)
            layout1 = column(explainer_div,current_boat, button_Start_Routing_Full,button_Start_Routing_GCR,boat_dropdown,manual_inputs,bottom_row)
        else:
            bottom_row = row(button_home, button_disable_grib)
            layout1 = column(explainer_div,current_boat, button_Start_Routing_Full_GRIB, button_Start_Routing_GCR_Grib, boat_dropdown,grib_file_input,manual_inputs,bottom_row)

        
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

  



