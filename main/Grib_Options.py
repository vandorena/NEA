from ecmwf.opendata import Client
import datetime
import os
import globals
from eccodes import codes_grib_new_from_file, codes_get_values, codes_get, codes_release
import numpy as np
from itertools import islice

class Bad_Grib(Exception):
    """Exception for a bad grib"""

class Incompatible_Extension(Bad_Grib):
    """Exception raised when an incompatible extension is used"""

class Incompatible_Grid_Type(Bad_Grib):
    """Exception relating to the type of Grid, raised if the type of Grid used by the Grib message is not 'regular_ll' """

class Incompatible_level_information(Bad_Grib):
    """Exception for gribs containing messages with multiple levels"""

class Point_not_in_weather_values(Bad_Grib):
    """Exception for a ._data weather value having an incomplete set of a data when being read"""

class Invalid_grib_extension(Bad_Grib):
    """Exception for a filename with an incompatible file extension"""

class LineNotInFile(FileNotFoundError):
    """Exception for when a line is not found in the file"""

class Grib_Modifiers:
    """Parent Class for respective API modifiers, dealing with the NOAA and ECMWF Models, """

    def __init__(self) -> None:
        self._current_client = None
        self._current_folder = None
        self._update_folder_path()
        self._request = None
    
    def _get_time(self, time = None) -> int:
        if time == None:
            current_datetime = datetime.datetime.now()
        else:
            current_datetime = time
        if current_datetime.hour >= 0 and current_datetime.hour < 6:
            return "0"
        elif current_datetime.hour >= 6 and current_datetime.hour < 12:
            return "6"
        elif current_datetime.hour >= 12 and current_datetime.hour <18:
            return "12"
        else:
            return "18"
        
    def _update_folder_path(self, time=None):
        "Updates Folder Path to current time"
        if time is None:
            current_datetime = datetime.datetime.now()
            try:
                os.mkdir(os.path.join("gribs",f"{current_datetime.date()}"))
            except FileExistsError:
                print("FileExists")
            self._current_folder = os.path.join("gribs",f"{current_datetime.date().year}-{current_datetime.date().month}-{current_datetime.date().day}",f"{current_datetime.hour}-{current_datetime.minute}-{current_datetime.second}.grib2")
        else:
            try:
                os.mkdir(os.path.join("gribs",f"{time.date()}"))
            except FileExistsError:
                print("FileExists")
            self._current_folder = os.path.join("gribs",f"{time.date().year}-{time.date().month}-{time.date().day}",f"{time.hour}-{time.minute}-{time.second}.grib2")

class ECMWF_API(Grib_Modifiers):
    """ECMWF API grib options, Default Client is Physics driven - IFS, default server is ecmwf, with options for azure"""

    def __init__(self, time:datetime = None) -> None:
        super().__init__()
        self._current_client = globals.BASECLIENT_PHYSICS
        if time is None:
            self._request = {
            "time": self._get_time(),
            "step": 48,
                         }
            today = datetime.datetime.today()
            self.time = datetime.datetime(year = today.year, month = today.month, day = today.day,hour=int(self._get_time()),minute=0)
        else:
            self.time = time


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

    
        
    
        
    def make_request(self):
        if self.time != datetime.datetime.now():
            self._update_folder_path(self.time)
        else:
            self.time = datetime.datetime.now()
            self._update_folder_path()
        client = self._current_client
        client.retrieve(
            time = self._get_time(self.time),
            source=f"{self._current_client.source}",
            model=f"{self._current_client.model}",
            type = "fc",
            param=["10u","10v"],
            target=self._current_folder,
            infer_stream_keyword=True,
        )

    def change_source(self):
        """Method to change the request server, from ecmwf to azure, and vice versa"""
        if self._current_client.source == "ecmwf":
            self._current_client.source = "azure"
        else:
            self._current_client.source = "ecmwf"

class ICON(Grib_Modifiers):
    def __init__(self):
        super().__init__()


    def get_file_url(self,time: datetime = None):
        run_path = f"{time.strftime('%Y%m%d')}{self._get_time(time=time)}"

class GRIB:

    def __init__(self, file_name:str, file_name_flag = None) -> None:
        """File_name includes the .grib,.grib2 or .grb extension"""
        self._filename = file_name
        self.filename_holder = file_name
        if self._filename != "dummy.grib2":
            self.ni = 0
            self.nj = 0
            self._extension = self._get_extension()
            self._filename_flag = file_name_flag
            if file_name_flag is None:
                self._path = os.path.join("main","GRIBS",file_name)
            else:
                self._path = file_name
            # Maybe find the index of the . and backindex to change file ext to .txt, then store .txt after finding if it exisits. THis would make asymmetric encode, and would result in quicker read times for all gribs, this would resuce inconsistencies
            self._path_ok = True
            print(self._path)
            if not os.path.exists(self._path):
                self._path_ok = False
                print(1)
                
                raise FileNotFoundError(f"Couldn't find a grib file at {self._path}")
            else:
                print(2)
                if not self._check_txt_path():
                    print(1)
                    print(self._filename)
                    if self._check_grib_path():
                        self._data = {
                            "index": [],
                            "short_name_list":[],
                            "times":[],
                            "level_list": [],
                            "time_list": [],
                            "date_list":[],
                        }
                        self._data_list = None
                        self._datetime = None
                        self._read_all()
                        self._translate_to_txt()
                        print(self._data["time_list"])
                    else:
                        raise FileNotFoundError(f"Could not find a grib file with the filename {self._filename}")
                else:
                    self._data = {}
                    self.read_metadata()
                    print(self._data)
                    print("yay")

    def _check_grib_path(self)->bool:
        pathcheck = os.path.exists(self._path)
        return pathcheck
    
    def _get_extension(self)->str:
        if self._filename[-4]==".":
            return ".grb"
        elif self._filename[-5]==".":
            return ".grib"
        elif self._filename[-6]==".":
            return ".grib2"
        else:
            raise Incompatible_Extension(f"The extension in {self._filename} is not equal to '.grib','.grb' or '.grib2'")
        

    def _check_txt_path(self)->bool:
        self._create_txt_path()
        if self._filename_flag is None:
            checkpath = os.path.join("main","GRIBS",self._filename)
        values = os.path.exists(checkpath)
        self._restore_filename()
        return values
        
    def _restore_filename(self):
        if ".txt" in self._filename:
            print(self._filename)
            self._filename = self._filename[:-4]
            print(self._filename)
            self._filename = self._filename + self._extension
            print(self._filename)
        return


    def _create_txt_path(self, path_flag: bool=False)->None:
        if self._filename[-5:] == ".grib":
            self._filename = self._filename[:-5]
        elif self._filename[-4:] == ".grb" or self._filename[-4:] == ".txt":
            self._filename = self._filename[:-4]
        elif self._filename[-6:] == ".grib2":
            self._filename = self._filename[:-6]
        else:
            raise Invalid_grib_extension(f"Extension of {self._filename} is invalid")
        self._filename = self._filename +  ".txt"
        if path_flag == True:
            self._path = os.path.join("main","GRIBS",self._filename)
        return

    def _translate_to_txt(self):
        self._create_txt_path()
        with open(os.path.join("main","GRIBS",self._filename),"a") as file:
            index_metadata = " ".join(f"{index} " for index in self._data["index"] )
            file.write(index_metadata +"\n")
            shotname_metadata = " ".join(f"{sn} " for sn in self._data["short_name_list"])
            file.write(shotname_metadata + "\n")
            time_metadata = " ".join(f"{time} " for time in self._data["time_list"])
            file.write(time_metadata + "\n")
            date_metadata = " ".join(f"{date} " for date in self._data["date_list"])
            file.write(date_metadata + "\n")
            level_metadata = " ".join(f"{level} " for level in self._data["level_list"])
            file.write(level_metadata  + "\n")
            latitude_metadata = " ".join(f"{latitude} " for latitude in self._data["latitudes"])
            file.write(latitude_metadata + "\n")
            longitude_metadata = " ".join(f"{longitude} " for longitude in self._data["longitudes"])
            file.write(longitude_metadata + "\n")
            for i in range(0,len(self._data["latitudes"])):
                for j in range(0,len(self._data["longitudes"])):
                    append_string = " ".join(f"{self._data[index][i][j]} " for index in self._data["index"])
                    file.write(append_string+"\n")
        for index in self._data["index"]:
            self._data[index] = None
        self._restore_filename()

    def _create_distributed_array(self,number_of_points: int,first_point: int,last_point: int)->list:
        if number_of_points ==1:
            return [first_point]
        if first_point == last_point:
            return [first_point]*number_of_points
        step = (last_point - first_point)/(number_of_points-1)
        points = [first_point]
        for i in range(1,number_of_points):
            new_point = first_point + (i*step)
            points.append(new_point)
            
        print(points)
        print(f"Number_of_points{number_of_points}")
        return points

    def _create_grid(self):
        if "latitudes" in self._data and "longitudes" in self._data:
            return
        else:
            with open(self._path, "rb") as file:
                current_message = codes_grib_new_from_file(file)
                gridtype = codes_get(current_message,"typeOfGrid")
                if gridtype != "regular_ll":
                    raise Incompatible_Grid_Type("Incompatible Grid Type")
                else:
                    self.ni = codes_get(current_message,"Ni")
                    self.nj = codes_get(current_message,"Nj")
                    print(f"ni:{self.ni},nj:{self.nj}")
                    first_long = codes_get(current_message,"longitudeOfFirstGridPointInDegrees")
                    last_long = codes_get(current_message,"longitudeOfLastGridPointInDegrees")
                    self._last_long = last_long
                    first_lat = codes_get(current_message,"latitudeOfFirstGridPointInDegrees")
                    last_lat = codes_get(current_message,"latitudeOfLastGridPointInDegrees")
                    self._data["latitudes"] = self._create_distributed_array(self.nj,first_lat,last_lat)
                    self._data["longitudes"] = self._create_distributed_array(self.ni,first_long,last_long)

    
    def _read_all(self):
        """Assumes all messages are single level"""
        self._create_grid()
        with open(self._path, 'rb') as file:
            big_list = []
            index_check_list = []
            while True:
                current_message = codes_grib_new_from_file(file)
                if current_message is None:
                    break
                try:
                    values = codes_get_values(current_message)
                    name = codes_get(current_message,"shortName") # str
                    date = codes_get(current_message,"date") #int
                    time = codes_get(current_message,"time") #int
                    if codes_get(current_message,"bottomLevel") == codes_get(current_message,"topLevel"):
                        current_ni = codes_get(current_message,"Ni")
                        current_nj = codes_get(current_message,"Nj")
                        first_long = codes_get(current_message,"longitudeOfFirstGridPointInDegrees")
                        last_long = codes_get(current_message,"longitudeOfLastGridPointInDegrees")
                        first_lat = codes_get(current_message,"latitudeOfFirstGridPointInDegrees")
                        last_lat = codes_get(current_message,"latitudeOfLastGridPointInDegrees")
                        level = codes_get(current_message,"bottomLevel") #int
                        current_id_value = [current_ni,current_nj,first_long,first_lat,last_lat,last_long,name,date,time,level]
                        if current_id_value in index_check_list:
                            break
                        else:
                            index_check_list.append(current_id_value)
                        print(f"Dealing with : name: {name} , date: {date}, time: {time}, level: {level}")
                        print(f"Message Info: Ni {current_ni}, nj {current_nj}, First Point ({first_long}, {first_lat}), Last Point ({last_long}, {last_lat})")
                        big_list.append(np.append(values, [level,time,date,name]))
                    else:
                        raise Incompatible_level_information("Message has multiple Levels")
                except Exception:
                    file.close()
                    raise Bad_Grib("Grib is corrupt")     
        self._data_digest(big_list)
        self._format_lat_lon()

    def _find_line_index(self,lat,lon)->int:
        try:
            lat_index = self._find_closest_lat(lat)
            lon_index = self._find_closest_lon(lon)
        except Exception:
            raise Point_not_in_weather_values
        print(type(lat_index))
        print(lat_index)
        print(type(self._data["longitudes"]))
        value = ( lat_index * (len(self._data["longitudes"])) ) + lon_index +7
        return value
    
    def read_metadata(self):
        self._create_txt_path()
        with open(os.path.join("main","GRIBS",self._filename),"r") as file:
            for i in range(7):
                current_line = file.readline()
                if i == 0:
                    self._data["index"] = current_line.split()
                elif i ==1:
                    self._data["short_name_list"] = current_line.split()
                elif i ==2:
                    self._data["time_list"] = current_line.split()
                elif i ==3:
                    self._data["date_list"] = current_line.split()
                elif i == 4:
                    self._data["level_list"] = current_line.split()
                elif i == 5:
                    self._data["latitudes"] = current_line.split()
                elif i == 6:
                    self._data["longitudes"] = current_line.split()

    def _find_twd_tws(self,list):
        u = list[0]
        v = list[1]
        tws = (u**2 + v**2)**(0.5)
        twd = np.degrees(np.arctan2(v,u))
        if twd < 0:
            twd +=360
        return twd,tws


    def getWindAt(self,t,lat:float,lon:float)->list:
        line_number = self._find_line_index(lat,lon)
        self._create_txt_path()
        with open(os.path.join("main","GRIBS",self._filename),"r") as file:
            single_line = next(islice(file,line_number,line_number+1),None)
            if single_line != None:
                print(type(single_line))
                self._restore_filename()
                return self._find_twd_tws(list(map(float,single_line.split())))
            else:
                raise LineNotInFile(f"File does not contain a line: {line_number}")
        self._restore_filename()

    def _format_lat_lon(self):
        self._data["latitudes"] = list(map(float,self._data["latitudes"]))
        self._data["longitudes"] = list(map(float,self._data["longitudes"]))

    def _find_closest_lat(self,lat:float)->float:
        """Assumes list is sorted, and assumes will be in list range, and assumes list exists"""
        self._format_lat_lon()
        index = None
        print("latitudess")
        print(self._data["latitudes"])
        if lat in self._data["latitudes"]:
            print("oop")
            index = self._data["latitudes"].index(lat)
        else:
            print("evppp")
        
            for i in range(1,len(self._data["latitudes"])):
                if float(self._data["latitudes"][i-1]) < lat and float(self._data["latitudes"][i]) > lat:
                    index = i
                    print(f"got a new_index {i}")
                    break
        if index is None:
            raise Exception("i dont know whats up")
        return index
    
    def _find_closest_lon(self,lat:float)->float:
        """Assumes list is sorted, and assumes will be in list range, and assumes list exists returns index"""
        self._format_lat_lon()
        index = None
        print("")
        print("pas")
        print(self._data["longitudes"])
        print("Hha")
        if lat in self._data["longitudes"]:
            print("1")
            index = self._data["longitudes"].index(lat)
        else:
            print("sss")
            for i in range(1,len(self._data["longitudes"])):
                if float(self._data["longitudes"][i-1]) < lat and float(self._data["longitudes"][i]) > lat:
                    index = i
                    break
        if index is None:
            raise Exception("i dont know whats up")
        return index

    def read_point_weather(self, lat:float,lon:float) -> dict:
        """expect self._data values to be npndarrays 2d"""
        try:
            lattitude = self._find_closest_lat(lat)
            longitude = self._find_closest_lon(lon)
        except Exception:
            raise Point_not_in_weather_values(f"The point was not found in the grib")
        point_data_dict = {
            "index":[],
            }
        print("index")
        print(self._data["index"])
        print(self._data)
        for i in range(0,len(self._data["index"])):
            if self._data[self._data["index"][i]][lattitude,longitude] != None:
                point_data_dict[self._data["index"][i]] = self._data[self._data["index"][i]][lattitude,longitude]
                point_data_dict["index"].append(self._data["index"][i])
            else:
                raise Point_not_in_weather_values(f"The point at {lattitude},{longitude} index was not found in {self._data['index'][i]}")
        return point_data_dict


        

    def _reshape_array(self,values: np.ndarray):
        expected_size = self.ni * self.nj
        if values.size != expected_size:
            raise(ValueError(f"Cannot reshape an array of {values.size} into shape({self.nj},{self.ni})"))
        return np.reshape(values.copy(),(self.nj,self.ni))
        
    def _digest_per_values(self,values:np.ndarray):
        short_name = values[-1]
        date = values[-2]
        time = values[-3]
        level = values[-4]
        reshaped_values = self._reshape_array(values[:-4].copy())

        index = f"{short_name}_{date}_{time}_{level}"
        if index not in self._data["index"]:
            self._update_metadata(short_name,date,time,level)
            self._data["index"].append(index)
            self._data[index] = reshaped_values
        return

    def _update_metadata(self, short_name: str , date: int, time:int , level:int)->None:
        if short_name not in self._data["short_name_list"]:
            self._data["short_name_list"].append(short_name)
        if level not in self._data["level_list"]:
            self._data["level_list"].append(level)
        if date not in self._data["date_list"]:
            self._data["date_list"].append(date)
        if time not in self._data["time_list"]:
            self._data["time_list"].append(time)
            print(self._data["time_list"])
        try:
            if not os.path.exists(os.path.join("main","GRIBS","log.txt")):
                print("No")
                print(self._data[self._data["index"][1]] )
                print(self._data[self._data["index"][3]] )
                print(self._data["longitudes"][0])
                print(self.ni)
                print(self._data["longitudes"][-1])
                print(self._last_long)
                with open(os.path.join("main","GRIBS","log.txt"),"w") as file:
                    file.write(self._data[self._data["index"][1]])
                    file.write("\n \n\n\n")
                    file.write(self._data[self._data["index"][3]])

        except BaseException:
            pass

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
    grib = GRIB(r"thebib.grib2")