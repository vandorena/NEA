from ecmwf.opendata import Client
import datetime
import os
import globals

class Grib_Modifiers:
    """Parent Class for respective API modifiers, dealing with the NOAA and ECMWF Models, """

    def __init__(self) -> None:
        self._current_client = None
        self._current_address = None
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

    def change_source(self):
        """Method to change the request server, from ecmwf to azure, and vice versa"""
        if self._current_client.source == "ecmwf":
            self._current_client.source = "azure"
        else:
            self._current_client.source = "ecmwf"
    

class GRIB:

    def __init__(self, file_name:str) -> None:
        """File_name includes the .grib,.grib2 or .grb extension"""
        self._path = rf"../gribs/{file_name}"
        self._data = {
            "latitudes" :[],
            "longitudes" :[],
            "data":[]
        }
        self._datetime = None

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