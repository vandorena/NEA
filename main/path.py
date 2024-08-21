

class Path:

    def __init__(self,start_lattitude: float = 0, start_longitude: float = 0,end_latitude: float=0, end_longitude: float = 0) -> None:
        
        self.start_lattitude = start_lattitude
        self.end_lattitude = start_longitude
        self.start_longitude = start_longitude
        self.end_longitude = end_longitude

        self.path_data = {
            "lat":[],
            "lon":[],
            "windspeed":[],
            "wind_direction":[]
            
        }