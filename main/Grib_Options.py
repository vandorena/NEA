from ecmwf.opendata import Client
import datetime

BASECLIENT_PHYSICS = Client(
    source="ecmwf",
    model="ifs",
    resol="0p25",
    preserve_request_order=False,
    infer_stream_keyword=True,
)

BASECLIENT_DATA = Client(
    source="ecmwf",
    model="aifs",
    resol="0p25",
    preserve_request_order=False,
    infer_stream_keyword=True,
)

class Grib_Modifiers:
    """Parent Class for respective API modifiers, dealing with the NOAA and ECMWF Models, """

    def __init__(self) -> None:
        self._current_client = None
        self._current_address = None
        self._current_folder = None
        self._update_folder_path()

    def _update_folder_path(self):
        "Updates Folder Path to current time"
        self._current_folder = f"C:\Users\Alex\Documents\Work\A-Levels-6th-Form\gribs\{datetime.date}\{datetime.time.hour}-{datetime.time.minute}-{datetime.time.second}"
    

class ECMWF_API(Grib_Modifiers):
    """ECMWF API grib options, Default Client is Physics driven - IFS, default server is ecmwf, with options for azure"""

    def __init__(self) -> None:
        super().__init__()
        self._current_client = BASECLIENT_PHYSICS


    def _change_client(self):
        """Accessor Method to Change the Current Client, no parameters"""
        if self._check_client == "DATA":
            self._current_client = BASECLIENT_PHYSICS
        else:
            self._current_client = BASECLIENT_DATA
    
    def check_client(self):
        "Method to see the current client, returns 'DATA' or 'PHYSICS' relating to AIFS and IFS models respectively"
        if self._current_client == BASECLIENT_DATA:
            return "DATA"
        else:
            return "PHYSICS"
        
    def change_source(self):
        """Method to change the request server, from ecmwf to azure, and vice versa"""
        if self._current_client.source == "ecmwf":
            self._current_client.source = "azure"
        else:
            self._current_client.source = "ecmwf"
    