from path import Path
from boats import Boat
from Grib_Options import GRIB, ECMWF_API
from globals import selected_grib
from math import radians, asin,sqrt,cos,degrees, pi, atan
from datetime import datetime
from global_land_mask import globe
import numpy as np

class PathError(Exception):
    "BaseClass for Exceptions relating to path functions"

class Routing_Model:
    
    def __init__(self, path: Path,grib:GRIB) -> None:
        self._current_path = path
        self._current_grib = grib

    def _create_path(self):
        start_latitude = float(input("Enter the starting lattitude: "))
        start_longitude = float(input("Enter the starting longitude: "))
        end_latitude = float(input("Enter the end lattitude: "))
        end_longitude = float(input("Enter the end longitude: "))
        boat = Boat
        self._current_path = Path(boat,start_latitude,start_longitude,end_latitude,end_longitude)
        self._current_grib = selected_grib

    def _check_in_water(self,lat,lon) -> bool:
        return globe.is_ocean(lat,lon)

    def create_big_circle_route(self):
        lat_s, lon_s , lat_e , lon_e = map(radians,[self._current_path.start_lattitude,self._current_path.start_longitude,self._current_path.end_lattitude,self._current_path.end_longitude])
        delta_lat = lat_e - lat_s
        delta_lon = lon_e - lon_s
        earth_radius = 6.3781*(10**6) #in meters
        #HaversineFormula
        distance = (2* earth_radius)* asin(sqrt((1-cos(delta_lat)+((cos(lat_s)*cos(lat_e))*(1-cos(delta_lon))))/(2)))
        self._current_path.append_great_circle_point(degrees(lat_s),degrees(lon_s))
        
    def _windspeed_magnitude_in_knts(self,u:float,v:float)->float:
        "returns windspeed in knots"
        windspeed = sqrt(u**2 + v**2)
        knts = windspeed * 1.94384
        return knts

    def find_windspeed_info(self,lat,lon,dtime:datetime):
        pass
        grib_values_at_point = self._current_grib.read_single_line(lat,lon)
        current_index = self._current_grib["index"]
        if dtime.hour not in self._current_grib._data["times"]:
            self._get_new_grib(dtime)
        for i in range(0,len(current_index)):
            if current_index[i]== "u":
                u = grib_values_at_point[i]
            if current_index[i] == "v":
                v = grib_values_at_point[i]
            
        
    def _get_new_grib(self,dtime:datetime):
        ECWMF_Client = ECMWF_API(time=dtime)
        ECWMF_Client.make_request()
        self._current_grib = GRIB(ECWMF_Client._current_folder)
        # make object
        #asssign-object
        pass


    def _find_twa(self,v:float,u:float):
        value = self._angle_to_destination_gcr(v,u)
        return value

    def _angle_to_destination_gcr(self,delta_lat:float,delta_lon:float)->float:
        "Returns an angle bearing in radians, can work with v and u components of wind speed"
        if delta_lon == 0:
            if delta_lat > 0:
                return 0
            elif delta_lat < 0:
                return pi
            else:
                raise PathError(f"Start and end points are the same {delta_lon} {delta_lat}")
        elif delta_lat == 0:
            if delta_lon > 0:
                return (pi/2)
            elif delta_lon < 0:
                return (1.5*pi)
            else:
                raise PathError(f"Start and end points are the same {delta_lon} {delta_lat}")
        else:
            if delta_lon > 0 and delta_lat > 0:
                value = atan((delta_lon/delta_lat))             
            elif delta_lon >0 and delta_lat < 0:
                value = pi - atan((delta_lon/delta_lat))
            elif delta_lon < 0 and delta_lat > 0:
                value = (1.5*pi) + atan((delta_lat/delta_lon))
            elif delta_lon < 0 and delta_lat < 0:
                value = pi + atan((delta_lon/delta_lat))
            return value
        

    def run_isometric(self):
        pass