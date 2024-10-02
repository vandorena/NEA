from ecmwf.opendata import Client
import datetime
import os
import globals
from eccodes import codes_grib_new_from_file, codes_get_values, codes_get, codes_release
import numpy as np

class Bad_Grib(Exception):
    """Exception for a bad grib"""

class Incompatible_Grid_Type(Bad_Grib):
    """Exception relating to the type of Grid, raised if the type of Grid used by the Grib message is not 'regular_ll' """

class Incompatible_level_information(Bad_Grib):
    """Exception for gribs containing messages with multiple levels"""

class Point_not_in_weather_values(Bad_Grib):
    """Exception for a ._data weather value having an incomplete set of a data when being read"""

class Invalid_grib_extension(Bad_Grib):
    """Exception for a filename with an incompatible file extension"""

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
        os.mkdir(os.path.join("gribs",f"{current_datetime.date()}"))
        self._current_folder = os.path.join("gribs",f"{current_datetime.date()}",f"{current_datetime.hour}-{current_datetime.minute}-{current_datetime.second}.grib2")

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
        self._filename = file_name
        self._path = os.path.join("gribs",file_name)
        # Maybe find the index of the . and backindex to change file ext to .txt, then store .txt after finding if it exisits. THis would make asymmetric encode, and would result in quicker read times for all gribs, this would resuce inconsistencies
        self._path_ok = True
        if not os.path.exists(self._path):
            self._path_ok = False
            raise FileNotFoundError(f"Couldn't find a grib file at {self._path}")
        else:
            if not self._check_txt_path():
                if self._check_grib_path():
                    self._data = {
                        "index": [],
                        "short_name_list":[],
                        "latitudes" :[],
                        "longitudes" :[],
                        "times":[],
                        "level_list": [],
                        "time_list": [],
                        "date_list":[],
                    }
                    self._data_list = None
                    self._datetime = None
                    self._read_all()
                    print(self._data)
                else:
                    raise FileNotFoundError(f"Could not find a grib file with the filename {self._filename}")

    def _check_grib_path(self)->bool:
        checkpath= os.path.join("gribs",self._filename)
        return os.path.exists(checkpath)
        

    def _check_txt_path(self)->bool:
        checkpath = os.path.join("gribs",self._create_txt_path())
        return os.path.exists(checkpath)
        

    def _create_txt_path(self, path_flag: bool=False):
        if self._filename[-5:] == ".grib":
            self._filename = self._filename[:-5]
        elif self._filename[-4:] == ".grb":
            self._filename = self._filename[:-4]
        elif self._filename[-6:] == ".grib2":
            self._filename = self._filename[:-6]
        else:
            raise Invalid_grib_extension(f"Extension of {self._filename} is invalid")
        self_filename = self._filename +  ".txt"
        if path_flag == True:
            self._path = os.path.join("gribs",self._filename)
        return

    def _translate_to_txt(self):
        self._create_txt_path()

    def _create_distributed_array(self,number_of_points: int,first_point: int,last_point: int)->list:
        step = (last_point - first_point)/number_of_points
        points = [first_point]
        while points[-1] < last_point:
            new_point = points[-1] + step
            points.append(new_point)
            if points[-1] >= last_point:
                break
        return points

    def _create_grid(self):

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
                self._data["latitudes"] = self._create_distributed_array(number_of_latitudes,first_lat,last_lat)
                self._data["longitudes"] = self._create_distributed_array(number_of_longitudes,first_long,last_long)

    
    def _read_all(self):
        """Assumes all messages are single level"""
        self._create_grid()
        with open(self._path, 'rb') as file:
            big_list = []
            end_file = False

            while not end_file:
                try:
                    current_message = codes_grib_new_from_file(file)
                    if current_message == None:
                        end_file = True
                        break
                    values = codes_get_values(current_message)
                    name = codes_get(current_message,"shortName")
                    date = codes_get(current_message,"date")
                    time = codes_get(current_message,"time")
                    if codes_get(current_message,"bottomLevel") == codes_get(current_message,"topLevel"):
                        values = np.append(values, codes_get(current_message,"bottomLevel"))
                    else:
                        raise Incompatible_level_information("Message has multiple Levels")
                    values = np.append(values, [time, date, name])
                    big_list.append(values)
                except Exception:
                    file.close()
                    raise Bad_Grib("Grib is corrupt")
            
            
        self._data_digest(big_list)

    def _find_closest_lat(self,lat:float)->float:
        """Assumes list is sorted, and assumes will be in list range, and assumes list exists"""
        if lat in self._data["latitudes"]:
            return self._data["latitudes"].index(lat)
        else:
            for i in range(1,len(self._data["latitudes"])):
                if self._data["latitudes"][i-1] < lat and self._data["latitudes"][i] > lat:
                    return i

    def _find_closest_lon(self,lat:float)->float:
        """Assumes list is sorted, and assumes will be in list range, and assumes list exists returns index"""
        if lat in self._data["longitudes"]:
            return self._data["longitudes"].index(lat)
        else:
            for i in range(1,len(self._data["longitudes"])):
                if self._data["longitudes"][i-1] < lat and self._data["longitudes"][i] > lat:
                    return i


    def read_point_weather(self, lat:float,lon:float,) -> dict:
        """expect self._data values to be npndarrays 2d"""
        lattitude = self._find_closest_lat(lat)
        longitude = self._find_closest_lon(lon)
        point_data_dict = {
            "index":[],
            }
        for i in range(0,len(self._data["index"])):
            if self._data[self._data["index"][i]][lattitude,longitude] != None:
                point_data_dict[self._data["index"][i]] = self._data[self._data["index"][i]][lattitude,longitude]
                point_data_dict["index"].append(self._data["index"][i])
            else:
                raise Point_not_in_weather_values(f"The point at {lattitude},{longitude} index was not found in {self._data["index"][i]}")
        return point_data_dict


        

    def _reshape_array(self,values: np.ndarray):
        nj = len(self._data["latitudes"])
        ni = len(self._data["longitudes"])
        expected_size = nj*ni
        
        if values.size != expected_size:
            raise(ValueError(f"Cannot reshape an array of {values.size} into shape({nj},{ni})"))
        return np.reshape(values,(nj,ni))
        
    def _digest_per_values(self,values:np.ndarray):
        short_name = values[-1]
        date = values[-2]
        time = values[-3]
        level = values[-4]
        values = values[:-4]

        if short_name not in self._data["short_name_list"]:
            self._data["short_name_list"].append(short_name)
        if level not in self._data["level_list"]:
            self._data["level_list"].append(level)
        if time not in self._data["time_list"]:
            self._data["time_list"].append(time)
        if date not in self._data["date_list"]:
            self._data["date_list"].append(date)
        index = short_name + date + time + level# all type str
        self._data["index"].append(index)
        self._data[index] = self._reshape_array(values)
        return


    def _data_digest(self,big_list:list):
        for values in big_list:
            self._digest_per_values(values)
        print(self._data["short_name_list"])
        print(self._data["index"])
        

if __name__ == "__main__":
    # client = Client()

    # current_datetime = datetime.datetime.now()
    # os.mkdir(rf"..\gribs\{current_datetime.date()}")
    # current_folder = f"..\gribs\{current_datetime.date()}\{current_datetime.hour}-{current_datetime.minute}-{current_datetime.second}.grib2"
    # current_folder = rf"{current_folder}"

    # client.retrieve(
    #     step=240,
    #     type="fc",
    #     param="msl",
    #     target=current_folder,
    # )
    grib = GRIB(r"thefrib.grib2")
    grib._read_all()