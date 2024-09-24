from path import Path
from boats import Boat
from Grib_Options import GRIB

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
        self._current_path = Path(start_latitude,start_longitude,end_latitude,end_longitude)

    def run_isometric(self):
        pass