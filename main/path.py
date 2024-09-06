from boats import Boat
from datetime import date,datetime

class LogArrayLengthException(Exception):
    """Error Raised as Array given to log function, is not of same dimensions as the Path's data"""

class NotInRouting(Exception):
    """Raised when a searched for Item is not included in the Routing"""

class StringSlicingFailureforPathClass(Exception):
    """Error raised when there is a indexerror in the string slice"""
class Path:

    def __init__(self,start_time: datetime,start_lattitude: float = 0, start_longitude: float = 0,end_latitude: float=0, end_longitude: float = 0, boat: Boat=Boat) -> None:
        
        self.start_lattitude = start_lattitude
        self.end_lattitude = start_longitude
        self.start_longitude = start_longitude
        self.end_longitude = end_longitude
        self.start_time = start_time

        self._current_point_lat = start_lattitude
        self._current_point_lon = start_longitude

        self.current_boat = boat
        self.started = False
        self.ended = False
        
        self.path_data_names = ["lat","lon","times","speeds","windspeed","gust_speed","wind_direction","wave_height", "wave_direction", "air_pressure","ocean_current_direction","ocean_current_speed"]
        self.path_data = {
            "lat":[],
            "lon":[],
            "times":[],
            "speeds":[],
            "windspeed":[],
            "gust_speed":[],
            "wind_direction":[],
            "wave_height":[],
            "wave_direction":[],
            "air_pressure":[],
            "ocean_current_direction": [],
            "ocean_current_speed": [],
        }

    def set_start(self):
        self.started = True

    def set_end(self):
        self.ended = True
    def get_previous_point(self) -> list:
        """Returns a list off previous_x,previous_y,previous_time"""
        if self.started == False:
            return [self.start_lattitude, self.start_longitude,self.start_time]
        else:
            previous_x = self.path_data["lat"][-1]
            previous_y = self.path_data["lon"][-1]
            previous_time = self.path_data["times"][-1]
            return [previous_x, previous_y,previous_time]
        
    def log(self,data_array: list):
        """Expects a list of 12 values.
        lat, lon, time:datetime, assumes time is realtime not timedelta, speed, windspeed,wind_direction, wave_height, wave_direction, air_pressure, current_direction, current_speed"""
        if len(data_array) == len(self.path_data_names):
            for i in range(0,len(self.path_data_names)):
                current_value = self.path_data_names[i]
                self.path_data[current_value].append(data_array[i])
        else:
            raise LogArrayLengthException
        
    def getXgetY(self)-> tuple:
        return self.path_data["lat"],self.path_data["lon"]

    def _find_index_times(self,time)->int:
        if time in self.path_data["times"]:
            return self.path_data["times"].index(time)
        else:
            if time > self.path_data["times"][-1]:
                raise NotInRouting("Time after routing finished")
            elif time < self.start_time:
                raise NotInRouting("Time before Routing Start Time")
            else:
                for i in range(1,len(self.path_data["times"])):
                    if time > self.path_data["times"][i-1] and time < self.path_data["times"][i]:
                        return self.path_data["times"][i]
    
    def _find_index_matcher_list(self,lat,lon) -> list:
        """Assumes both in self.path_data
        Binary Search to find the index of points that go through that latitude of longitude"""
        lat_elements_to_check = len(self.path_data["lat"])
        lon_elements_to_check = len(self.path_data["lon"])
        current_lat_list = self.path_data["lat"]
        current_lon_list = self.path_data["lon"]
        lat_index = []
        lon_index = []
        while lat_elements_to_check != 0:
            held_index = current_lat_list.index(lat)
            lat_index.append(held_index)
            try:
                count_list = current_lat_list[:held_index]
                current_lat_list = current_lat_list[(held_index+1):]
            except IndexError:
                raise StringSlicingFailureforPathClass
            lat_elements_to_check = lat_elements_to_check - len(count_list)
        while lon_elements_to_check != 0:
            held_index = current_lon_list.index(lon)
            lon_index.append(held_index)
            try:
                count_list = current_lon_list[:held_index]
                current_lon_list = current_lon_list[(held_index+1):]
            except IndexError:
                raise StringSlicingFailureforPathClass
            lon_elements_to_check = lon_elements_to_check - len(count_list)
        output = []
        for i in range(0,len(lat_index)):
            for j in range(0,len(lon_index)):
                if lat_index[i] == lon_index[j]:
                    output.append(lat_index[i])
        return output
        


            

    
    def point_query(self,lat,lon) -> tuple:
        """lat and lon must be taken from the lists given by the getXgetY function"""
