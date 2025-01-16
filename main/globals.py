import datetime
from ecmwf.opendata import Client

NETWORK_STATUS = False
current_timestep = 180 #In minutes integer
SETTINGS = {
    "setting_list" : [],
    "number_of _points":1000,
    "maximum_wind_speed": 30, #in knots
    "maximum_wave_height": 10, #in meters
    "maximum_distance_from_centerline" : 5 #in degrees
    }
current_path = None
max_days_future = 3
# Routings are Path objects
CURRENT_BOATS = {
    "boat_list":[]
    }
selected_boat = None
selected_grib = None
CURRENT_TIME = datetime.datetime.now()
CURRENT_SUBFOLDERS ={
    "subfolder_list":[]
}
CURRENT_GRIBS = {
    "grib_list":[],
}
BASECLIENT_DATA = Client(
    source="ecmwf",
    model="aifs",
    resol="0p25",
    preserve_request_order=False,
    infer_stream_keyword=True,
)
BASECLIENT_PHYSICS = Client(
    source="ecmwf",
    model="ifs",
    resol="0p25",
    preserve_request_order=False,
    infer_stream_keyword=True,
)
ICON_LIST=[None]
mapwidth = 500
mapheight = 500
BUTTON_STYLE ={
    "width":300,
    "height":100,
    "font_size":80,
    "type": ["default","primary","success","warning","danger","light"],
    "height_policy": "fixed",
    "icons": ICON_LIST,
    "margins":(5,5,5,5),
    "styles" :{},
    "syncable":True
}