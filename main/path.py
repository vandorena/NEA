from boats import Boat

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
            "air_pressure":[]
        }

    def get_previous_point(self):
        if self._started == False:
            return 
