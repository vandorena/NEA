from boats import Boat

class LogArrayLengthException(Exception):
    """Error Raised as Array given to log function, is not of same dimensions as the Path's data"""

class StringSlicingFailureforPathClass(Exception):
    """Error raised when there is a indexerror in the string slice"""
class Path:

    def __init__(self,start_lattitude: float = 0, start_longitude: float = 0,end_latitude: float=0, end_longitude: float = 0, boat: Boat=Boat) -> None:
        
        self.start_lattitude = start_lattitude
        self.end_lattitude = start_longitude
        self.start_longitude = start_longitude
        self.end_longitude = end_longitude

        self._current_point_lat = start_lattitude
        self._current_point_lon = start_longitude

        self.current_boat = boat
        self._started = False
        self._ended = False
        
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
        self._started = True

    def set_end(self):
        self._ended = True
    def get_previous_point(self) -> tuple:
        if self._started == False:
            return self.start_lattitude, self.start_longitude
        else:
            previous_x = self.path_data["lat"][-1]
            previous_y = self.path_data["lon"][-1]
            return previous_x, previous_y
        
    def log(self,data_array: list):
        """Expects a list of 12 values.
        lat, lon, time, speed, windspeed,wind_direction, wave_height, wave_direction, air_pressure, current_direction, current_speed"""
        if len(data_array) == len(self.path_data_names):
            for i in range(0,len(self.path_data_names)):
                current_value = self.path_data_names[i]
                self.path_data[current_value].append(data_array[i])
        else:
            raise LogArrayLengthException
        
    def getXgetY(self)-> tuple:
        return self.path_data["lat"],self.path_data["lon"]
    
    def _find_index_matcher_list(self,lat,lon) -> list:
        """Assumes both in self.path_data"""
        lat_elements_to_check = len(self.path_data["lat"])
        lon_elements_to_check = len(self.path_data["lon"])
        current_lat_list = self.path_data["lat"]
        current_lon_list = self.path_data["lon"]
        lat_index = []
        lon_index = []
        match_index = []
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
