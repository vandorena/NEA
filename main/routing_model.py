from path import Path
from boats import Boat
from Grib_Options import GRIB, ECMWF_API
from globals import selected_grib, upwind_twa
from math import radians, asin,sqrt,cos,degrees, pi, atan, atan2, sin
from datetime import datetime,timedelta
from global_land_mask import globe
import numpy as np
from haversine import inverse_haversine, haversine, Unit
import open_meteo
import random
import globals

class PathError(Exception):
    "BaseClass for Exceptions relating to path functions"

class OutWaterException(Exception):
    "Exception to break if a point is not in water"

class ContinuedOutWaterException(OutWaterException):
    "Exception raised when land is continuously detected"

class Routing_Model:
    
    def __init__(self, path: Path,grib:GRIB, timestep) -> None:
        "Timestep is expected as int in hours"
        self._current_path = path
        self._current_grib = grib
        self._current_bearing = -1
        self._angle_step = pi/6
        self._upwind_tack = False
        self.timestep = timestep*60

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

    def create_big_circle_route(self,ignore_exception:bool=False):
        lat_s, lon_s , lat_e , lon_e = map(radians,
        [self._current_path.start_lattitude,
         self._current_path.start_longitude,
         self._current_path.end_lattitude,
        self._current_path.end_longitude])
        delta_lat = lat_e - lat_s
        delta_lon = lon_e - lon_s
        earth_radius = 6.3781*(10**6) #in meters
        #HaversineFormula
        distance = (2* earth_radius)* asin(sqrt((1-cos(delta_lat)+((cos(lat_s)*cos(lat_e))*(1-cos(delta_lon))))/(2)))
        start_time = self._current_path.start_time
        self._current_path.path_data["great_circle_times"].append(start_time)
        self._current_path.append_great_circle_point(degrees(lat_s),degrees(lon_s))
        end_point = False
        self._current_bearing = degrees(self._angle_to_destination_gcr(delta_lat,delta_lon))
        gcr_distances = []
        self._current_path._gcr_time = 0
        land_list = []
        while not end_point:
            lat,lon = self._route_single_point(True)
            if not self._check_in_water(lat,lon) and not ignore_exception:
                raise OutWaterException(f"point at {lat},{lon} is land ")
            elif not self._check_in_water(lat,lon) and ignore_exception:
                raise ContinuedOutWaterException
            #elif not self._check_in_water(lat,lon) and ignore_exception:
             #   land_list.append([lat,lon])
            self._current_path.path_data["great_circle_lat"].append(lat)
            self._current_path.path_data["great_circle_lon"].append(lon)
            self._current_path.path_data["great_circle_times"].append(start_time + timedelta(minutes = 30))
            self._current_path._gcr_time += 30
            gcr_distances.append(self._distance_from_current_to_end(gcr_flag=True))
            if gcr_distances[-1] < 100 or gcr_distances[-1]>gcr_distances[-2]:
                gcr_distances = 0
                if ignore_exception:
                    self._current_path._gcr_time = 1000000
                else:
                    self._current_path._gcr_time += 30
                end_point = True
        if not ignore_exception:
            return
        #else: 
         #   return land_list

    


    def _straight_line_distance(self, gcr_flag:  bool=False):
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
        twa = self._find_twa(u,v)
        boatspeed = self._current_path.current_boat.find_polar_speed(ws_mag,twa)
        distance_nm = boatspeed * (globals.current_timestep)/60
        return distance_nm
    
    def create_big_circle_route_online(self,ignore_exception:bool=False):
        print("Creating Big Cirlce")
        print(self._current_path.start_lattitude)
        print(self._current_path.end_lattitude)
        lat_s, lon_s , lat_e , lon_e = map(radians,[self._current_path.start_lattitude,self._current_path.start_longitude,self._current_path.end_lattitude,self._current_path.end_longitude])
        delta_lat = lat_e - lat_s
        delta_lon = lon_e - lon_s
        earth_radius = 6.3781*(10**6) #in meters
        #HaversineFormula
        distance = (2* earth_radius)* asin(sqrt((1-cos(delta_lat)+((cos(lat_s)*cos(lat_e))*(1-cos(delta_lon))))/(2)))
        start_time = self._current_path.start_time
        self._current_path.path_data["great_circle_times"].append(start_time)
        self._current_path.append_great_circle_point(degrees(lat_s),degrees(lon_s))
        end_point = False
        self._current_bearing = degrees(self._angle_to_destination_gcr(delta_lat,delta_lon))
        gcr_distances = []
        self._current_path._gcr_time = 0
        land_list = []
        while not end_point:
            lat,lon = self._route_single_point_online(True)
            if not self._check_in_water(lat,lon) and not ignore_exception:
                raise OutWaterException(f"point at {lat},{lon} is land ")
            elif not self._check_in_water(lat,lon) and ignore_exception:
                land_list.append([lat,lon])
            self._current_path.path_data["great_circle_lat"].append(lat)
            self._current_path.path_data["great_circle_lon"].append(lon)
            self._current_path.path_data["great_circle_times"].append(start_time + timedelta(minutes = 30))
            self._current_path._gcr_time += 30
            gcr_distances.append(self._distance_from_current_to_end(gcr_flag=True))
            if gcr_distances[-1] < 100:
                gcr_distances = 0
                if ignore_exception:
                    self._current_path._gcr_time = 1000000
                else:
                    self._current_path._gcr_time += 30
                end_point = True
            try:
                if gcr_distances[-1]>gcr_distances[-2]:
                    gcr_distances = 0
                    if ignore_exception:
                        self._current_path._gcr_time = 1000000
                    else:
                        self._current_path._gcr_time += 30
                    end_point = True
            except IndexError:
                print("IndexError")

        if not ignore_exception:
            print(self._current_path.path_data["great_circle_lon"])
            print(self._current_path.path_data["great_circle_lat"])
            return
        else: 
            return land_list

    def create_big_circle_route_online_v2(self):
        start_lat, start_lon = self._current_path.start_lattitude, self._current_path.start_longitude #y
        end_lat, end_lon = self._current_path.end_lattitude, self._current_path.end_longitude
        start_time = self._current_path.start_time #y
        print(start_time)   #y
        self._current_path.append_great_circle_point(start_lat,start_lon,start_time)#y
        end_point = False #y
        gcr_distances = [self._distance_from_current_to_end_v2(True)]
        globals.current_timestep = self.timestep
        self._current_path._gcr_time = 0
        exit_land = False
        while not end_point:
            self._current_bearing = self._angle_to_destinatin_gcr_v2(start_lat=self._current_path.path_data['great_circle_lat'][-1],start_lon=self._current_path.path_data['great_circle_lon'][-1],end_lat=end_lat,end_lon=end_lon) #y
            lat,lon = self._route_single_point_online(True)
            if not self._check_in_water(lat,lon) and exit_land:
                prev_lat_holder, prev_lon_holder = self._current_path.path_data['great_circle_lat'][-1], self._current_path.path_data['great_circle_lon'][-1]
                self._current_path.pop_great_circle_point()
                raise ContinuedOutWaterException(f"point at {lat},{lon} is land and point at {prev_lat_holder},{prev_lon_holder} ")
            if not (self._check_in_water(lat,lon)) and (not exit_land):
                exit_land = True
            self._current_path.append_great_circle_point(lat,lon,(start_time+timedelta(minutes = globals.current_timestep)))
            self._current_path._gcr_time += globals.current_timestep
            gcr_distances.append(self._distance_from_current_to_end_v2(gcr_flag=True))
            print(f"gcr_distances are{gcr_distances}")
            if gcr_distances[-1] > (gcr_distances[-2]):
                self._current_path.pop_great_circle_point()
                end_point = True
                break
        self._current_path.pop_great_circle_point()
        self._current_path.pop_great_circle_point()
        final_time = self.find_time_for_distance(gcr_distances[-2])
        self._current_path.append_great_circle_point(end_lat,end_lon,time=(self._current_path.path_data["great_circle_times"][-1]+timedelta(minutes=final_time)))
                
        
    def decompose_time(self,twa,distnace,ws_mag):
        across = distnace * sin(radians(twa))
        upwind= distnace * cos(radians(twa))
        first_mag = across / sin(radians(upwind_twa))
        delta_upwind = sqrt((first_mag**2) - (across**2))
        final_upwind = upwind-delta_upwind
        final_mag = final_upwind/(cos(radians(upwind_twa)))
        boatspeed = self._current_path.current_boat.find_polar_speed(ws_mag,upwind_twa)
        time = (final_mag + first_mag)/float(boatspeed)
        return time
    
    def find_time_for_distance(self,distance):
        self._current_bearing = self._angle_to_destinatin_gcr_v2(start_lat=self._current_path.path_data["great_circle_lat"][-1],start_lon=self._current_path.path_data["great_circle_lon"][-1],end_lat=self._current_path.end_lattitude,end_lon=self._current_path.end_longitude)
        ws_mag, wind_heading = open_meteo.make_10mvu_request(lat=self._current_path.path_data["great_circle_lat"][-1],lon=self._current_path.path_data["great_circle_lon"][-1],time=self._current_path.path_data["great_circle_times"][-1])
        twa = self._find_twa_mag_bear(radians(wind_heading))
        if twa >= upwind_twa:
            boatspeed = self._current_path.current_boat.find_polar_speed(ws_mag,twa)
            time = distance/float(boatspeed)
        else:
            print("estimate")
            time = self.decompose_time(twa,distance,ws_mag)
        return time

    def upwind_twa_bearing_finder(self,lat,lon,time):
        if self._angle_to_destinatin_gcr_v2():
            pass
        
            
    def _straight_line_distance_online(self, gcr_flag:  bool=False):
        """Timestep is expected int for mintures returns distance in nautical miles"""
        if not gcr_flag:
            lat = self._current_path.path_data["lat"][-1]
            lon = self._current_path.path_data["lon"][-1]
            time = self._current_path.path_data["times"][-1]
        else:
            lat = self._current_path.path_data["great_circle_lat"][-1]
            lon = self._current_path.path_data["great_circle_lon"][-1]
            time = self._current_path.path_data["great_circle_times"][-1]
        ws_mag, wind_heading = open_meteo.make_10mvu_request(lat,lon,time)
        twa = self._find_twa_mag_bear(radians(wind_heading))
        print(f"twa is {twa} at {lat},{lon}")
        if twa < upwind_twa:
            boatspeed = self._current_path.current_boat.find_polar_speed(ws_mag,upwind_twa)
            distance_1 = float(boatspeed) * (int(globals.current_timestep))/60
            distance_nm = distance_1 * cos(radians(upwind_twa))/cos(radians(twa))
        else:
            boatspeed = self._current_path.current_boat.find_polar_speed(ws_mag,twa)
        #print(globals.current_timestep)
        #print("timestep")
            distance_nm = float(boatspeed) * (int(globals.current_timestep))/60
        return distance_nm
    
    def _straight_line_distance_online_only(self, gcr_flag: bool = False):
        boatspeed = self._current_path
        
    
    def _distance_from_current_to_end(self, gcr_flag: bool=False):
        lat_e = self._current_path.end_lattitude
        lon_e = self._current_path.end_longitude
        if gcr_flag == True:
            current_lat = self._current_path.path_data["great_circle_lat"][-1]
            current_lon = self._current_path.path_data["great_circle_lon"][-1]
        else:
            current_lat = self._current_path.path_data["lat"][-1]
            current_lon = self._current_path.path_data["lon"][-1]
        delta_lat = lat_e - current_lat
        delta_lon = lon_e - current_lon
        earth_radius = 6.3781*(10**6) #in meters
        #HaversineFormula
        distance = (2* earth_radius)* asin(sqrt((1-cos(delta_lat)+((cos(current_lat)*cos(lat_e))*(1-cos(delta_lon))))/(2)))
        return distance

    def _distance_from_current_to_end_v2(self, gcr_flag: bool=False):
        lat_e = self._current_path.end_lattitude
        lon_e = self._current_path.end_longitude
        if gcr_flag == True:
            current_lat = self._current_path.path_data["great_circle_lat"][-1]
            current_lon = self._current_path.path_data["great_circle_lon"][-1]
        else:
            current_lat = self._current_path.path_data["lat"][-1]
            current_lon = self._current_path.path_data["lon"][-1]
        distance = haversine((current_lat,current_lon),(lat_e,lon_e), unit = Unit.NAUTICAL_MILES)
        return distance

    def _route_single_point(self, gcr_flag: bool=False,lat:float=None,lon:float=None):
        if not gcr_flag:
            distance_nm = self._straight_line_distance()
            current_point = (lat, lon)
        else:
            distance_nm = self._straight_line_distance(gcr_flag=True) 
            current_point = (self._current_path.path_data["great_circle_lat"][-1], self._current_path.path_data["great_circle_lon"][-1])
        new_lat,new_lon = inverse_haversine(current_point,(1.852*distance_nm),radians(self._current_bearing))
        return new_lat,new_lon
    
    def _route_single_point_online(self, gcr_flag: bool=False,lat:float=None,lon:float=None):
        if not gcr_flag:
            distance_nm = self._straight_line_distance_online()
            current_point = (lat, lon)
        else:
            distance_nm = self._straight_line_distance_online(gcr_flag=True) 
            current_point = (self._current_path.path_data["great_circle_lat"][-1], self._current_path.path_data["great_circle_lon"][-1])
        new_lat,new_lon = inverse_haversine(current_point,(1.852*distance_nm),radians(self._current_bearing))
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
            if current_index[i]== "10u":
                u = grib_values_at_point[i]
            if current_index[i] == "10v":
                v = grib_values_at_point[i]
        return u,v
        
    def _get_new_grib(self,dtime:datetime):
        ECWMF_Client = ECMWF_API(time=dtime)
        ECWMF_Client.make_request()
        self._current_grib = GRIB(ECWMF_Client._current_folder)
        pass


    def _find_twa(self,u:float,v:float):
        value = self._angle_to_destination_gcr(u,v)
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

    def _find_twa_mag_bear(self,wind_heading):
        bearing = self._current_bearing % 360
        wind_heading_ranged = wind_heading % 360
        if wind_heading_ranged > bearing and bearing > 180:
            angle = wind_heading_ranged - bearing
        elif wind_heading_ranged > bearing and bearing < 180:
            if wind_heading_ranged > (180 + bearing):
                angle = 360 - wind_heading_ranged + bearing
            else:
                angle = wind_heading_ranged - bearing
        elif wind_heading_ranged < bearing and bearing > 180:
            angle = bearing - wind_heading_ranged
            if angle > 180:
                angle = 360 - angle
        elif wind_heading_ranged < bearing and bearing < 180:
            angle = bearing - wind_heading_ranged
        elif wind_heading_ranged == bearing:
            angle = 0
        else:
            print(f"Huh twa uncalcualted wind heading {wind_heading_ranged} bearing {bearing}")
        if angle>180:
            print(f"Error twa is > 180 it is  {angle}")
        print(f"Current_TWA is: {angle}")
        return angle

    def _angle_to_destination_gcr(self,delta_lat:float,delta_lon:float)->float:
        "Returns an angle bearing in radians, can work with v and u components of wind speed"
        if delta_lon == 0 and delta_lat == 0:
            raise PathError(f"Start and end points are the same {delta_lon} {delta_lat}")  
        angle = atan2(delta_lon,delta_lat)
        if angle < 0:
            angle += (2* pi)
        return angle
    
    def _angle_to_destinatin_gcr_v2(self,start_lat,end_lat, start_lon,end_lon):
        "Differs from previous by returing in degrees, is no longer 2d and follows spherical earth, returns in degrees"
        delta_lon = end_lon - start_lon
        holder1 = sin(radians(delta_lon)) *  cos(radians(end_lat))
        holder2 = cos(radians(start_lat)) * sin(radians(end_lat)) - sin(radians(start_lat)) * cos(radians(end_lat)) * cos(radians(delta_lon))
        bearing = atan2(holder1,holder2)
        return (degrees(bearing) + 360) % 360

    def run_isometric(self):
        land = []
        try:
            self.create_big_circle_route()
        except OutWaterException:
            land = self.create_big_circle_route(True)
        if len(land) != 0:
            self.visited_points = []
        else:
            self.visited_points = []

    def isometric(self,lat,lon,time:datetime,cur_path: list =None):
        print("1")
        if cur_path is None:
            cur_path = [(lat,lon,time)]
        if self._current_path._gcr_time == 0:
            return []
        points = []
        for bearing in range(0,360,30):
            print("bearing")
            self._current_bearing = bearing
            new_lat,new_lon = self.route_iso_point(self,lat,lon,time)
            new_time = time + timedelta(minutes=globals.current_timestep)
            if not self._check_in_water(new_lat,new_lon):
                if (new_lat,new_lon,new_time) not in self.visited_points:
                    self.visited_points.append((new_lat,new_lon,new_time))
                path = cur_path.append((new_lat,new_lon,new_time))
                self._current_path._gcr_time -= globals.current_timestep
                new_points = self.isometric(new_lat,new_lon,new_time,path)
                points.extend(new_points)
        return points

    def route_iso_point(self,lat,lon,time:datetime):
        u,v = self.find_windspeed_info(lat,lon,time)
        ws_mag = self._windspeed_magnitude_in_knts(u,v)
        twa = self._find_twa(u,v)
        boatspeed = self._current_path.current_boat.find_polar_speed(ws_mag,twa)
        distance_nm = boatspeed * (globals.current_timestep)/60
        current_point = (lat, lon)
        new_lat,new_lon = inverse_haversine(current_point,(1.852*distance_nm),radians(self._current_bearing))
        return (new_lat,new_lon)

    def isometric_online(self,lat,lon,time:datetime,cur_path: list =None):
        print("1")
        if cur_path is None:
            cur_path = [(lat,lon,time)]
        if self._current_path._gcr_time == 0:
            return []
        points = []
        for bearing in range(0,360,30):
            print("bearing")
            self._current_bearing = bearing
            new_lat,new_lon = self.route_iso_point_online(lat,lon,time)
            new_time = time + timedelta(minutes=globals.current_timestep)
            if not self._check_in_water(new_lat,new_lon):
                if (new_lat,new_lon,new_time) not in self.visited_points:
                    self.visited_points.append((new_lat,new_lon,new_time))
                path = cur_path.append((new_lat,new_lon,new_time))
                self._current_path._gcr_time -= globals.current_timestep
                new_points = self.isometric_online(new_lat,new_lon,new_time,path)
                points.extend(new_points)
        return points


    def route_iso_point_online(self,lat,lon,time:datetime):
        print("pointed")
        ws_mag, ws_dir = open_meteo.make_10mvu_request(lat,lon,time)
        twa = self._find_twa_mag_bear(radians(ws_dir))
        while twa < 30:
            self._current_bearing +=30
            if self._current_bearing > 360:
                self._current_bearing -= 360
            twa = self._find_twa_mag_bear(radians(ws_dir))
        boatspeed = self._current_path.current_boat.find_polar_speed(ws_mag,twa)
        distance_nm = float(boatspeed) * (globals.current_timestep)/60
        current_point = (lat, lon)
        new_lat,new_lon = inverse_haversine(current_point,(1.852*distance_nm),radians(self._current_bearing))
        return (new_lat,new_lon)