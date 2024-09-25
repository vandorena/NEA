from ecmwf.opendata import Client
import datetime
import os
import globals
from eccodes import codes_grib_new_from_file, codes_get_values, codes_get, codes_release

class Incompatible_Grid_Type(Exception):
    """"Exception relating to the type of Grid, raised if the type of Grid used by the Grib message is not 'regular_ll' """

class Grib_Modifiers:
    """Parent Class for respective API modifiers, dealing with the NOAA and ECMWF Models, """

    def __init__(self) -> None:
        self._current_client = None
        self._current_folder = None
        self._update_folder_path()
        self._request = None

    def _update_folder_path(self):
        "Updates Folder Path to current time"
        current_datetime = datetime.datetime.now()
        os.mkdir(rf"..\gribs\{current_datetime.date()}")
        self._current_folder = f"..\gribs\{current_datetime.date()}\{current_datetime.hour}-{current_datetime.minute}-{current_datetime.second}.grib2"
        self._current_folder = rf"{self._current_folder}"
    

class ECMWF_API(Grib_Modifiers):
    """ECMWF API grib options, Default Client is Physics driven - IFS, default server is ecmwf, with options for azure"""

    def __init__(self) -> None:
        super().__init__()
        self._current_client = globals.BASECLIENT_PHYSICS
        self._request = {
            "time": self._get_time(),
            "step": 48,
                         }


    def _change_client(self):
        """Accessor Method to Change the Current Client, no parameters"""
        if self._check_client == "DATA":
            self._current_client = globals.BASECLIENT_PHYSICS
        else:
            self._current_client = globals.BASECLIENT_DATA
    
    def _check_client(self):
        "Method to see the current client, returns 'DATA' or 'PHYSICS' relating to AIFS and IFS models respectively"
        if self._current_client == globals.BASECLIENT_DATA:
            return "DATA"
        else:
            return "PHYSICS"

    def _get_time(self) -> int:
        current_datetime = datetime.datetime.now()
        if current_datetime.hour >= 0 and current_datetime.hour < 6:
            return "0"
        elif current_datetime.hour >= 6 and current_datetime.hour < 12:
            return "6"
        elif current_datetime.hour >= 12 and current_datetime.hour <18:
            return "12"
        else:
            return "18"
        
    def make_request(self):
        self._update_folder_path()
        client = self._current_client
        client.retrieve(
            source=f"{self._current_client.source}",
            model=f"{self._current_client.model}",
            type = "fc",
            param=["ws","u","v",""],
            target=self._current_folder,
            infer_stream_keyword=True,
        )

    def change_source(self):
        """Method to change the request server, from ecmwf to azure, and vice versa"""
        if self._current_client.source == "ecmwf":
            self._current_client.source = "azure"
        else:
            self._current_client.source = "ecmwf"
    

class GRIB:

    def __init__(self, file_name:str) -> None:
        """File_name includes the .grib,.grib2 or .grb extension"""
        self._path = rf"gribs/{file_name}"
        self._data = {
            "latitudes" :[],
            "longitudes" :[],
            "times":[],
            "data":[]
        }
        self._data_list = None
        self._datetime = None

    def create_distributed_array(self,number_of_points: int,first_point: int,last_point: int)->list:
        step = (last_point - first_point)/number_of_points
        points = [first_point]
        while points[-1] < last_point:
            new_point = points[-1] + step
            points.append()
            if points[-1] >= last_point:
                break
        return points

    def create_grid(self):

        with open(self._path, "rb") as file:
            current_message = codes_grib_new_from_file(file)
            gridtype = codes_get(current_message,"typeOfGrid")
            if gridtype != "regular_ll":
                raise Incompatible_Grid_Type("Incompatible Grid Type")
            else:
                number_of_longitudes = codes_get(current_message,"Ni")
                number_of_latitudes = codes_get(current_message,"Nj")
                first_long = codes_get(current_message,"longitudeOfFirstGridPointInDegrees")
                last_long = codes_get(current_message,"longitudeOfLastGridPointInDegrees")
                first_lat = codes_get(current_message,"latitudeOfFirstGridPointInDegrees")
                last_lat = codes_get(current_message,"latitudeOfLastGridPointInDegrees")
                self._data["latitudes"] = self.create_distributed_array(number_of_latitudes,first_lat,last_lat)
                self._data["longitudes"] = self.create_distributed_array(number_of_longitudes,first_long,last_long)
            file.close()

    def read_all(self):
        self.create_grid
        with open(self._path, 'rb') as file:
            big_list = []
            end_file = False

            while not end_file:

                current_message = codes_grib_new_from_file(file)
                
                if current_message == None:
                    end_file = True
            file.close()



    def _data_digest(self):
        pass
        

if __name__ == "__main__":
    client = Client()

    current_datetime = datetime.datetime.now()
    os.mkdir(rf"..\gribs\{current_datetime.date()}")
    current_folder = f"..\gribs\{current_datetime.date()}\{current_datetime.hour}-{current_datetime.minute}-{current_datetime.second}.grib2"
    current_folder = rf"{current_folder}"

    client.retrieve(
        step=240,
        type="fc",
        param="msl",
        target=current_folder,
    )