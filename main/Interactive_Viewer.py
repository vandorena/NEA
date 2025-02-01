from bokeh.plotting import figure, show, curdoc
from bokeh.models import ColumnDataSource, Slider, Button, Dropdown, Div, FileInput, TapTool, TextInput, DatetimePicker
from bokeh.models.callbacks import CustomJS
from bokeh.layouts import column,row, layout
from boats_bokeh import find_boats
from boats import Boat
import globals
from globals import BUTTON_STYLE
from grib_manager_bokeh import find_gribsV2
from bokeh.events import Tap
import numpy as np
from global_land_mask.globe import is_ocean
import datetime
import pandas
from path import Path
from Grib_Options import GRIB
from routing_model import Routing_Model, ContinuedOutWaterException
from libweatherrouting_routing import Routing
from libweatherrouting_linearbestisorouter import LinearBestIsoRouter
from global_land_mask import globe
from libweatherrouting_mock_grib import mock_grib

class NotWaterError(Exception):
    "Exception Governing if a point is not in water"

def viewer(doc):

    start_time = (datetime.datetime.now() + datetime.timedelta(minutes=2))
    
    routing_timedelta = 1

    start_x = 0
    start_y = 0

    default_boat = Boat("Imoca60")
    default_boat.add_polar_v2("Imoca60.pol")
    globals.selected_boat = default_boat

    end_x = 0
    end_y = 0

    prev_start_x = 0
    prev_start_y = 0

    prev_end_x = 0
    prev_end_y = 0

    tap_count = 0

    start_x_changed = False
    start_y_changed = False
    start_time_changed = False
    end_x_changed = False
    end_y_changed =False

    grib_uploaded = False

    input_warning = False
    water_warning = False

    land_hit = False
    number_of_points = 2
    intermediate_points = []
    current_intermediate_point = 0
    intermediate_point_start_time = None
    current_intermediate_point_changed = False
    intermediate_gcr_flag = False
    intermediate_isometric_flag = False

    x_input_nonlocal = ""
    y_input_nonlocal = ""

    plot_colors = ["yellow","red","blue","green","purple","orange","black","pink","brown"]
    current_color = 0

    grib_mode = False

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


    def check_current_path():
        nonlocal start_x,start_y,end_x,end_y,start_time, number_of_points,intermediate_points, current_intermediate_point_changed, current_intermediate_point
        cur_boat = globals.selected_boat
        cur_path = globals.current_path
        if cur_path is not None:
            cur_path_start_lat = cur_path.start_lattitude
            cur_path_start_lon = cur_path.start_longitude
            cur_path_end_lat = cur_path.end_lattitude
            cur_path_end_lon = cur_path.end_longitude
            cur_path_start_time = cur_path.start_time
            cur_path_start_x, cur_path_start_y = lat_lon_to_web_mercator(cur_path_start_lat,cur_path_start_lon)
            cur_path_end_x, cur_path_end_y = lat_lon_to_web_mercator(cur_path_end_lat,cur_path_end_lon)
            cur_path_boat = cur_path.current_boat
        else:
            cur_path_start_x,cur_path_start_y = 1,1
            cur_path_end_x,cur_path_end_y = 2,2
            cur_path_boat = cur_boat
        if (cur_path_start_x != start_x or cur_path_start_y != start_y or cur_path_end_x != end_x or cur_path_end_y != end_y or cur_path_start_time or cur_path_boat != cur_boat) and number_of_points == 2:
            print("Wrong Way on line 103")
            start_lat,start_lon = web_mercator_to_lat_lon(start_x,start_y)
            end_lat, end_lon = web_mercator_to_lat_lon(end_x,end_y)
            try:
                globals.current_path = Path(start_time=start_time,start_lattitude=start_lat,start_longitude = start_lon,end_latitude=end_lat,end_longitude=end_lon,boat=cur_boat)
            except ValueError:
                globals.current_path = Path(start_time=datetime.datetime.now(),start_lattitude=start_lat,start_longitude = start_lon,end_latitude=end_lat,end_longitude=end_lon,boat=cur_boat)
        elif current_intermediate_point_changed:
            current_intermediate_point_changed = False
            if current_intermediate_point == 0:
                print("only once here")
                start_flag = True
                start_lat, start_lon = web_mercator_to_lat_lon(start_x,start_y)
                end_lat , end_lon = web_mercator_to_lat_lon(intermediate_points[current_intermediate_point][0],intermediate_points[current_intermediate_point][1])
            elif current_intermediate_point == (len(intermediate_points)):
                start_flag = False
                cur_point_lat, cur_point_lon = web_mercator_to_lat_lon(end_x,end_y)
            else:
                start_flag = False
                cur_point_lat, cur_point_lon = web_mercator_to_lat_lon(intermediate_points[current_intermediate_point][0],intermediate_points[current_intermediate_point][1])
            if start_flag:
                try:
                    globals.current_path = Path(start_time=start_time, start_lattitude=start_lat,start_longitude=start_lon, end_latitude=end_lat,end_longitude=end_lon,boat=cur_boat)
                except ValueError:
                    globals.current_path = Path(start_time =datetime.datetime.now(), start_lattitude=start_lat,start_longitude=start_lon, end_latitude=end_lat,end_longitude=end_lon,boat=cur_boat)
            else:
                print("It got here")
                print(f"before {globals.current_path.start_lattitude}, {globals.current_path.start_longitude}   end { globals.current_path.end_lattitude}, {globals.current_path.end_longitude}")
                if intermediate_gcr_flag == True:
                    globals.current_path.start_lattitude = globals.current_path.path_data["great_circle_lat"][-1]
                    globals.current_path.start_longitude = globals.current_path.path_data["great_circle_lon"][-1]
                    globals.current_path.end_lattitude = cur_point_lat
                    globals.current_path.end_longitude = cur_point_lon
                    globals.current_path.start_time = globals.current_path.path_data["great_circle_times"][-1]
                elif intermediate_isometric_flag == True:
                    globals.current_path.start_lattitude = globals.current_path.path_data["lat"][-1]
                    globals.current_path.start_longitude = globals.current_path.path_data["lon"][-1]
                    globals.current_path.end_lattitude = cur_point_lat
                    globals.current_path.end_longitude = cur_point_lon
                    globals.current_path.start_time = globals.current_path.path_data["times"][-1]
                print(f"After {globals.current_path.start_lattitude}, {globals.current_path.start_longitude}   end { globals.current_path.end_lattitude}, {globals.current_path.end_longitude}")
               


    def create_boat_list()-> list:
        find_boats()
        boat_list =[]
        for i in range(0,len(globals.CURRENT_BOATS["boat_list"])):
            boatname = globals.CURRENT_BOATS["boat_list"][i]
            #print(boatname)
            #print(globals.CURRENT_BOATS[boatname])
            ntuple = (boatname)
            boat_list.append(ntuple)
        return boat_list
    
    def create_grib_list()-> list:
        find_gribsV2()
        grib_list =[]
        for i in range(0,len(globals.CURRENT_GRIBS["grib_list"])):
            gribname = globals.CURRENT_GRIBS["grib_list"][i]
            #print(gribname)
            #print(globals.CURRENT_BOATS[gribname])
            ntuple = (gribname)
            grib_list.append(ntuple)
        return grib_list

    def update_boat(event):
        nonlocal current_boat
        globals.selected_boat = globals.CURRENT_BOATS[event.item]
        #print(globals.selected_boat)
        current_boat.text = f"Current Boat: {event.item}"

    def update_grib(event):
        nonlocal current_grib
        globals.selected_grib = globals.CURRENT_GRIBS[event.item]
        #print(globals.selected_grib)
        current_grib.text = f"Current GRIB: {event.item}"

    def update_x_input(attr,old,new):
        nonlocal x_input_nonlocal
        x_input_nonlocal = new

    def update_y_input(attr,old,new):
        nonlocal y_input_nonlocal
        y_input_nonlocal = new

    def gcr_routing(event):
        nonlocal start_x,start_y,end_x,end_y

    fastest_route_div = Div(text="")

    def full_routing(event):
        nonlocal routing_timedelta, start_time, end_x, end_y,start_x,start_y,tap_count,number_of_points,grib_mode,current_intermediate_point, intermediate_points, plot, plot_colors,current_color,current_boat,intermediate_gcr_flag,intermediate_point_start_time,land_hit, current_intermediate_point_changed
        #try:
        end_lat,end_lon = web_mercator_to_lat_lon(end_x,end_y)
        start_lat, start_lon = web_mercator_to_lat_lon(start_x,start_y)
        #print("please help me, it should be coming here")
        #try:
        while tap_count == number_of_points:
            print("Begann routing")
            if grib_mode:
                cur_grib = globals.selected_grib.filename_holder
            else:
                cur_grib = None
                cur_grib = mock_grib(13,120,1)
            track = intermediate_points + [(end_lat,end_lon)]
            cur_boat = globals.selected_boat
            routing_object = Routing(algorithm=LinearBestIsoRouter, polar=cur_boat,track=track,grib=cur_grib,startDatetime=start_time,startPosition=(start_lat,start_lon))
            print("Object is made")
            print(f"Cur grib is {cur_grib} and mode is {grib_mode}")
            while not routing_object.end:
                result = routing_object.step(timedelta=routing_timedelta)
#                   print("ay it did a step")
            print("It finished routing")
            #print(result.path)
            path_pos_list = []
            for isopoint in result.path:
                path_pos_list.append(isopoint.pos)
            lats, lons = zip(*path_pos_list)
            xs,ys = zip(*map(lat_lon_to_web_mercator,lats,lons))
            #print(f"xs and ys {xs},{ys}")
            source = ColumnDataSource({'x':xs,'y':ys})
            plot.line(source=source,legend_label=f"Fastest Route", color=plot_colors[(current_color%len(plot_colors))],line_width=2)
            plot.scatter(source=source,color=plot_colors[((current_color+4)%len(plot_colors))-1],size=4)
            fastest_route_div.text = f"{result.path}"
            current_color +=1
            break
        #except BaseException:
         #   print("Ummm")
          #  pass

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

    def update_routing_timedelta(attr,old,new):
        nonlocal routing_timedelta
        routing_timedelta = new
        globals.current_timestep= new*60

    routing_timedelta_slider = Slider(start=1,end=8, step=0.5, value=routing_timedelta, title="Chose Routing Timestep")
    routing_timedelta_slider.on_change("value", update_routing_timedelta)

    input_warning_div = Div(text="")
    land_warning_div = Div(text="")

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

    button_Start_Routing_GCR_Grib= Button(
        label="Find Great Circle Route using GRIB",
        button_type=BUTTON_STYLE["type"][2],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    

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

    water_warning_div = Div(text="")

    point_enter_button = Button(
        label="Create Starting Point",
        button_type=BUTTON_STYLE["type"][2],
        width=(BUTTON_STYLE["width"]),
        height=(BUTTON_STYLE["height"]//2),
        icon=BUTTON_STYLE["icons"][0]
        )
    

    def enable_grib(event):
        nonlocal grib_mode
        grib_mode = True
        update_root(enable_grib=True)

    def round_to_minute(dt:datetime.datetime):
        pandas_datetime = pandas.to_datetime(dt)
        rounded_pandas_datetime = pandas_datetime.round("1Min")
        return rounded_pandas_datetime.to_pydatetime()

    def add_x_days(dt:datetime.datetime,x:int):
        return dt+datetime.timedelta(days=x)

    def update_num_of_points(attr,old,new):
        nonlocal number_of_points, tap_count,plot
        number_of_points = new
        if tap_count > 1:
            plot.renderers = []
            plot.add_tile("CartoDB Positron", retina=True)
            tap_count = 0


    button_enable_grib.on_event("button_click",enable_grib)

    start_time_picker = DatetimePicker(title="Select Start Time",value=start_time, min_date=round_to_minute(datetime.datetime.now()), max_date=add_x_days(round_to_minute(datetime.datetime.now()),globals.max_days_future))
    
    start_time_div = Div(text=f"<b> Start Time is {start_time}</b><br>")

    route_point_slider = Slider(title="Number of Points", value=number_of_points, start=2,end=15)
    route_point_slider.on_change("value", update_num_of_points)

    
    def update_lines():
        pass

    def update_div():
        nonlocal start_x,start_y, end_x , end_y, start_x_changed,start_y_changed,end_x_changed,end_y_changed,land_hit,x_input_div,y_input_div, input_warning,water_warning,start_time_changed,start_time,start_time_div
        #print(f"start_x_changed: {start_x_changed}, start_y_changed: {start_y_changed}, end_x_changed: {end_x_changed}, end_y_changed: {end_y_changed}")
        if not start_x_changed and not start_y_changed and not end_x_changed and not end_y_changed:
            explainer_div.text = "<h2>Select a start and end point</h2><br>"
            x_input_div.text = "<h2>Enter your starting X coordinate below (longitude):</h2><br>"
            y_input_div.text ="<h2>Enter your starting Y coordinate below (latitude):</h2><br>"
        elif start_x_changed and start_y_changed and not end_x_changed and not end_y_changed:
            y_holder_1 , x_holder_1 = web_mercator_to_lat_lon(start_x,start_y)
            explainer_div.text = (f"<h2> You have not selected an end point</h2><br>"
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
            x_input_div.text = f"<h2> Input is disabled, click map to enable and reset. </h2><br>"
            y_input_div.text = ""

        else:
            print("This shouldn't do this Interactive Viewer.py line 188")
        if input_warning:
            input_warning_div.text = "<h1> Only number inputs are allowed.</h1><br> <b> Ensure all inputs are of decimal form, i.e. 51.231323</b><br>"
            input_warning = False
        else:
            input_warning_div.text = ""
        if water_warning:
            water_warning_div.text = "<h1> You can only place points in water. </h1> <br>"
            water_warning = False
        else:
            water_warning_div.text = ""
        if start_time_changed:
            start_time_changed = False
            start_time_div.text=f"<b>Start time is: {start_time.strftime('%Y-%m-%d %H:%M:%S')}</b><br> "
        if land_hit:
            land_hit = False
            cur_path = globals.current_path
            land_warning_div.text = f"Land was hit at ({cur_path.path_data['great_circle_lat'][-2]},{cur_path.path_data['great_circle_lon'][-2]}) and again at ({cur_path.path_data['great_circle_lat'][-1]},{cur_path.path_data['great_circle_lon'][-1]})"


    
    def manual_input(event):
        nonlocal tap_count, number_of_points,intermediate_points,start_x,start_y,end_x,end_y,start_x_changed,start_y_changed,end_x_changed,end_y_changed,input_warning, x_input_nonlocal,y_input_nonlocal,x_input,y_input,water_warning
        original_tap_count = tap_count
        try:
            lon,lat = float(x_input_nonlocal),float(y_input_nonlocal)
            if not is_ocean(lat,lon):
                water_warning = True
                raise ValueError
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
            elif tap_count > 1 and tap_count < number_of_points:
                intermediate_points.append((x,y))
                plot.scatter(x=[x],y=[y],size=8,fill_color="orange",line_color="yellow",line_width=1)
            elif tap_count == number_of_points:
                pin_point_source.data= {'x':[],'y':[],'color':[]}
                end_x = x
                end_y = y
                end_x_changed = True
                end_y_changed = True
                plot.scatter(x=[end_x],y=[end_y],size=10,fill_color = 'blue',line_color="yellow",line_width=1)
                update_div()
                update_lines()
            
            elif tap_count == (number_of_points+1):
                tap_count = original_tap_count
            x_input.value = ""
            y_input.value = ""
        except ValueError:
            tap_count = original_tap_count
            input_warning = True
            update_div()
    
    def on_tap(event):
        nonlocal fastest_route_div, tap_count, start_x,start_y,end_x,end_y,start_x_changed,start_y_changed,end_x_changed,end_y_changed,water_warning, number_of_points,intermediate_points
        original_tap_count = tap_count
        x,y = event.x,event.y
        water_overide = False
        try:
            tap_count +=1
            lat,lon = web_mercator_to_lat_lon(x,y)
            if not is_ocean(lat,lon) and tap_count !=3:
                raise NotWaterError
            if tap_count == 1:
                pin_point_source.data = {'x':[], 'y':[], 'color':[]}
                start_x =x
                start_y= y
                plot.scatter(x=[start_x],y=[start_y],size=10,fill_color="red",line_color="yellow",line_width=1)
                start_x_changed = True
                start_y_changed = True
                update_div()
                update_lines()
            elif tap_count > 1 and tap_count < number_of_points:
                intermediate_points.append((x,y))
                print(f"Intermediate points are {intermediate_points}")
                plot.scatter(x=[x],y=[y],size=8,fill_color="orange",line_color="yellow",line_width=1)
            elif tap_count == number_of_points:
                pin_point_source.data= {'x':[],'y':[],'color':[]}
                end_x = x
                end_y = y
                mag_delt_x = ((end_x-start_x)**2 + (end_y-start_y)**2)**(0.5)
                if mag_delt_x < 50000:
                    water_overide = True
                    raise NotWaterError # In this case used as an elegant break
                end_x_changed = True
                end_y_changed = True
                plot.scatter(x=[end_x],y=[end_y],size=10,fill_color = 'blue',line_color="yellow",line_width=1)
                update_div()
                update_lines()
                
            elif tap_count == (number_of_points+1):
                pin_point_source.data = {'x':[],'y':[],'colors':[]}
                plot.renderers = []
                plot.add_tile("CartoDB Positron", retina=True)
                tap_count = 0
                prev_start_x = start_x
                prev_start_y = start_y
                prev_end_x = end_x
                prev_end_y = end_y
                start_x = 0
                end_x = 0
                start_y = 0
                end_y = 0
                start_x_changed = False
                start_y_changed = False
                end_x_changed = False
                end_y_changed = False
                fastest_route_div.text = ""
                intermediate_points = []
                update_div()
                update_lines()
        except NotWaterError:
            water_warning = True
            if water_overide:
                water_warning = False
                water_overide = False
            tap_count = original_tap_count
            update_div()

    def update_start_time(attr,old,new):
        nonlocal start_time
        start_time = new
        start_time_changed = True
        update_datetime_picker(start_time)
        update_div()

    def find_gcr_single():
        nonlocal routing_timedelta,plot, start_x,start_y ,end_x,end_y,current_color,plot_colors, tap_count, number_of_points, current_intermediate_point, intermediate_gcr_flag, intermediate_points, current_intermediate_point_changed
        if number_of_points == 2:
            try:
                while tap_count == 2:
                    check_current_path()
                    cur_path = globals.current_path
                    if grib_mode:
                        cur_grib = globals.selected_grib
                    else:
                        cur_grib = GRIB("dummy.grib2")
                    routing = Routing_Model(path=cur_path,grib=cur_grib,timestep=routing_timedelta)
                    if grib_mode:
                        routing.create_big_circle_route()
                    else:
                        try:
                            routing.create_big_circle_route_online_v2()
                        except ContinuedOutWaterException:
                            land_hit = True
                            print(f"Hit land with {cur_path.path_data}")
                            update_div()
                    lats = cur_path.path_data['great_circle_lat']
                    lons = cur_path.path_data['great_circle_lon']
                    xs,ys = zip(*map(lat_lon_to_web_mercator,lats,lons))
                    print(f"xs and ys {xs},{ys}")
                    source = ColumnDataSource({'x':xs,'y':ys})
                    plot.line(source=source,legend_label=f"Great Circle Route between ({cur_path.start_lattitude},{cur_path.start_longitude}) and ({cur_path.end_lattitude},{cur_path.end_longitude})", color=plot_colors[(current_color%len(plot_colors))],line_width=2)
                    plot.scatter(source=source,color=plot_colors[(current_color%len(plot_colors))-1],size=4)
                    current_color +=1
                    break
            except BaseException:
                print("There was an error ,l ine 470 of interactive viewer")
        else:
            end_lat,end_lon = web_mercator_to_lat_lon(end_x,end_y)
            start_lat, start_lon = web_mercator_to_lat_lon(start_x,start_y)
            print("please help me, it should be coming here")
            #try:
            while tap_count == number_of_points:
                if grib_mode:
                    cur_grib = globals.selected_grib
                else:
                    cur_grib = GRIB("dummy.grib2")
                while current_intermediate_point != (len(intermediate_points)+1): # Not sure of this
                    intermediate_gcr_flag = True
                    current_intermediate_point_changed = True
                    check_current_path()
                    cur_path = globals.current_path
                    routing = Routing_Model(path=cur_path,grib=cur_grib,timestep=routing_timedelta)
                    if grib_mode:
                        routing.create_big_circle_route()
                    else:
                        try:
                            routing.create_big_circle_route_online_v2()
                        except ContinuedOutWaterException:
                            land_hit = True
                            print(f"Hit land with {cur_path.path_data}")
                            update_div()
                    lats = cur_path.path_data['great_circle_lat']
                    lons = cur_path.path_data['great_circle_lon']
                    xs,ys = zip(*map(lat_lon_to_web_mercator,lats,lons))
                    print(f"xs and ys {xs},{ys}")
                    source = ColumnDataSource({'x':xs,'y':ys})
                    plot.line(source=source,legend_label=f"Great Circle Route between ({start_lat},{start_lon}) and ({end_lat},{end_lon})", color=plot_colors[(current_color%len(plot_colors))],line_width=2)
                    plot.scatter(source=source,color=plot_colors[(current_color%len(plot_colors))-1],size=4)
                    current_intermediate_point += 1
                    if cur_path.path_data["great_circle_lat"][-1] == end_lat and cur_path.path_data["great_circle_lon"][-1] == end_lon:
                        break
                current_color +=1
                break
            #except BaseException:
             #   print("There was an error with multiple gcrs of interactive viewer")
                        


    plot.on_event(Tap,on_tap)
    point_enter_button.on_event("button_click",manual_input)
    start_time_picker.on_change('value',update_start_time)

    manual_inputs = column(water_warning_div,input_warning_div,x_input_div,x_input,y_input_div,y_input,point_enter_button,start_time_picker,route_point_slider,routing_timedelta_slider)

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
        nonlocal grib_mode
        grib_mode = False
        update_root(False)

    def update_datetime_picker(start_time):
        start_time_picker.value = start_time
    
    button_disable_grib = Button(
        label="Disable Grib Mode",
        button_type=BUTTON_STYLE["type"][3],
        width=(BUTTON_STYLE["width"]//3),
        height=(BUTTON_STYLE["height"]//2),
        icon=BUTTON_STYLE["icons"][0]
        )
    
    button_Start_Routing_GCR.on_event('button_click', find_gcr_single)
    button_Start_Routing_GCR_Grib.on_event('button_click', find_gcr_single)

    button_disable_grib.on_event("button_click",update_root_false)
    
    update_root(False)

  



