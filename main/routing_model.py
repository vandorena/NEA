from path import Path
from boats import Boat
from Grib_Options import GRIB, ECMWF_API
from globals import selected_grib
from math import radians, asin,sqrt,cos,degrees, pi, atan
from datetime import datetime
from global_land_mask import globe
import numpy as np
from haversine import inverse_haversine

class PathError(Exception):
    "BaseClass for Exceptions relating to path functions"

class Routing_Model:
    
    def __init__(self, path: Path,grib:GRIB) -> None:
        self._current_path = path
        self._current_grib = grib
        self._current_bearing = -1

    def _create_path(self):
        start_latitude = float(input("Enter the starting lattitude: "))
        start_longitude = float(input("Enter the starting longitude: "))
        end_latitude = float(input("Enter the end lattitude: "))
        end_longitude = float(input("Enter the end longitude: "))
        boat = Boat()
        boat.add_polar(r"Boats/") #Fix this
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
        self._current_path.append_great_circle_point(degrees(lat_s),degrees(lon_s),self._current_path.start_time)
        end_point = False
        bearing = self._angle_to_destination_gcr(delta_lat,delta_lon)
        while not end_point:
            lat,lon = self._route_single_point(bearing,True)
            self._current_path.path_data["great_circle_lat"].append(lat)
            self._current_path.path_data["great_circle_lon"].append(lon)
            

    def _straight_line_distance(self, gcr_flag:  bool=False, timestep: int=30):
        """Timestep is expected int for mintures returns distance in nautical miles"""
        if not gcr_flag:
            lat = self._current_path.path_data["lat"][-1]
            lon = self._current_path.path_data["lon"][-1]
            time = self._current_path.path_data["times"][-1]
        else:
            lat = self._current_path.path_data["great_circle_lat"][-1]
            lon = self._current_path.path_data["great_circle_lon"][-1]
            time = self._current_path.path_data["great_circle_times"][-1]
        u,v = self.find_windspeed_info(lat,lon,time)
        ws_mag = self._windspeed_magnitude_in_knts(u,v)
        twa = self._find_twa(v,u)
        boatspeed = self._current_path.current_boat.find_polar_speed(ws_mag,twa)
        distance_nm = boatspeed * (timestep)/60
        return distance_nm
    
    def _distance_from_current_to_point(self, gcr_flag: bool=False):
        lat_e = radians(self._current_path.end_lattitude)
        lon_e = radians(self._current_path.end_longitude)
        if gcr_flag == True:
            current_lat = radians(self._current_path.path_data["great_circle_lat"][-1])
            current_lon = radians(self._current_path.path_data["great_circle_lon"][-1])
        else:
            current_lat = radians(self._current_path.path_data["lat"][-1])
            current_lon = radians(self._current_path.path_data["lon"][-1])
        delta_lat = lat_e - current_lat
        delta_lon = lon_e - current_lon
        earth_radius = 6.3781*(10**6) #in meters
        #HaversineFormula
        distance = (2* earth_radius)* asin(sqrt((1-cos(delta_lat)+((cos(current_lat)*cos(lat_e))*(1-cos(delta_lon))))/(2)))
        
        

    def _route_single_point(self, bearing: int, gcr_flag: bool=False,timestep:int=30):
        if not gcr_flag:
            distance_nm = self._straight_line_distance(timestep=timestep)
            current_point = (self._current_path.path_data["lat"][-1], self._current_path.path_data["lon"][-1])
        else:
            distance_nm = self._straight_line_distance(gcr_flag=True,timestep=timestep) 
            current_point = (self._current_path.path_data["great_circle_lat"][-1], self._current_path.path_data["great_circle_lon"][-1])
        new_lat,new_lon = inverse_haversine(current_point,(1.852*distance_nm),radians(bearing))
        return new_lat,new_lon

    def _windspeed_magnitude_in_knts(self,u:float,v:float)->float:
        "returns windspeed in knots"
        windspeed = sqrt(u**2 + v**2)
        knts = windspeed * 1.94384
        return knts

    def find_windspeed_info(self,lat,lon,dtime:datetime)->tuple:
        grib_values_at_point = self._current_grib.read_single_line(lat,lon)
        current_index = self._current_grib["index"]
        if dtime.hour not in self._current_grib._data["times"]:
            self._get_new_grib(dtime)
        for i in range(0,len(current_index)):
            if current_index[i]== "u":
                u = grib_values_at_point[i]
            if current_index[i] == "v":
                v = grib_values_at_point[i]
        return u,v
        
    def _get_new_grib(self,dtime:datetime):
        ECWMF_Client = ECMWF_API(time=dtime)
        ECWMF_Client.make_request()
        self._current_grib = GRIB(ECWMF_Client._current_folder)
        pass


    def _find_twa(self,v:float,u:float):
        value = self._angle_to_destination_gcr(v,u)
        bearing = radians(self._current_bearing)
        angle = value - bearing
        if angle > radians(180):
            angle = degrees(angle)
            angle = angle - 360
        elif degrees(angle) < -180:
            angle = degrees(angle)  + 360
        else:
            angle = degrees(angle)
        return angle

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