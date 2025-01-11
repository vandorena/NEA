import numpy as np
import os
import math

class PolarFileError(Exception):
    """Exception Raised when the Polar File is non homogenous"""
class PolarFileNoMetadata(PolarFileError):
    """"Excetion Raised when the Polar File has no Metadata"""

class Boat:

    def __init__(self,name: str) -> None:
        self.data = {
            "name":name
        }

    def add_polar(self,filename:str):
        """
        Dictionary format: "name": str , "windspeeds": list of windspeed keys, windspeedkey1: [list of speeds], indexed by headinglist
        """
        #Logic error resulting in speeds being only as long as the number of wind speeds instead of as long as the nuember of headings
        filename = os.path.join("Boats",filename)
        with open(filename,"r") as file:
            line_array = file.readlines()
        wind_speeds = []
        speeds = []
        headings = []
        plr_type = ""
        #print(line_array)
        for i in range(0,len(line_array)):
            values = line_array[i].split()
            print(f"values are {values}")
            speedholder = []
            heading_count = 0
            if i == 0:
                plr_type = values[0]
                if plr_type == "TWA\TWS":
                    wind_speeds = values[1:]
                    print(f"{wind_speeds} areeeee")
            if plr_type == "TWA\TWS" and i!=0:
                headings.append(values[0])
                speeds.append(values[1:])
            if plr_type == "!Expedition" and i !=0:
                for j in range(0,len(values)):
                    if j == 1:
                        wind_speeds.append(values[j])
                    else:
                        if i == 1:
                            if (j%2) == 1:
                                headings.append(float(values[j]))
                            else:
                                speedholder.append(float(values[j]))
                        else:
                            if (j%2) == 1:
                                if float(values[j]) != headings[heading_count]:
                                    raise PolarFileError(f"There is a Heading mismatch at line {i+1}, column {j+1}")
                            else:
                                speedholder.append(float(values[j]))

                speeds.append(speedholder)
        
            elif plr_type == "":
                raise PolarFileNoMetadata(f"There is no metadata in file: {filename}")
        
        self.data["wind_list"] = wind_speeds 
        self.data["heading_list"] = headings
        for i in range(0,len(wind_speeds)):
            print(wind_speeds)
            self.data[wind_speeds[i]] = speeds[i]
        print(self.data)
        return

    def add_polar_v2(self,filename:str):
        filename = os.path.join("Boats",filename)
        with open(filename,"r") as file:
            line_array = file.readlines()
        polar_filetype = None
        polar_filetype=(line_array[0].split())[0]
        if polar_filetype == "TWA\TWS" or polar_filetype=="TWA" or polar_filetype=="TWA/TWS":
            self.parse_TWA_TWS(line_array)
        elif polar_filetype == "!Expedition":
            raise PolarFileError(f"We currently don't support Expedition polar files")
        else:
            raise PolarFileNoMetadata(f"There is no metadata in file: {filename}")
        
    def parse_TWA_TWS(self,lines:list):
        self.data["heading_list"] = []
        for i in range(0,len(lines)):
            current_line = lines[i].split()
            if i == 0:
                self.data["wind_list"] = current_line[1:]
                for j in range(1,len(current_line)):
                    self.data[current_line[j]] = []
            else:
                self.data["heading_list"].append(current_line[0])
                for z in range(1,len(current_line)):
                    current_wind = self.data["wind_list"][z-1]
                    self.data[current_wind].append(current_line[z])
               

    def _list_to_int(self,list:list):
        new_list = []
        for i in range(0,len(list)):
            new_list.append(int(list[i]))
        return new_list
    
    def _binary_list_class_search(self,input_list: list, search_term: int):
        #print(f"boo   {search_term}")
        print(input_list)
        list_length = len(input_list)
        current_index = list_length//2
        found = False
        current_comparision = 0
        max_comparison = np.log2(list_length) -1
        count = 1
        found_index = -1
        while not found:
            if current_comparision <= max_comparison:
                current_comparision += 1
                if input_list[current_index] == math.floor(search_term):
                    print(input_list[current_index])
                    #print("this is input_list")
                    found_index = current_index
                    found = True
                else:
                    count +=1
                    if input_list[current_index] < search_term:
                        current_index = current_index + list_length//(2**count)
                    else:
                        current_index = current_index - list_length//(2**count)
            else:
                for i in range(1,list_length-1):
                    print(i)
    
                    if input_list[i-1] < search_term and input_list[i] > search_term:
                        found_index = i
                        print(f"gttit {found_index}")
                        found = True
            
                        break
                    #print(f"found {found_index}")
                found = True
        return found_index
                
    def find_polar_speed(self,windspeed,heading):
        reference_windspeeds = self._list_to_int(self.data["wind_list"])
        reference_headings = self._list_to_int(self.data["heading_list"])
        speed_index = self._binary_list_class_search(reference_windspeeds,windspeed)
        heading_index = self._binary_list_class_search(reference_headings,heading)
        print(f"heading_index is {heading_index}")
        try:
            boatspeed = self.data[self.data["wind_list"][speed_index]][heading_index]
        except IndexError:
            if heading_index < 0 and heading_index < (len(self.data[self.data["wind_list"][speed_index]])):
                boatspeed = self.data[self.data["wind_list"][speed_index]][heading_index - 1]
            elif heading_index > (len(self.data[self.data["wind_list"][speed_index]])):
                boatspeed = self.data[self.data["wind_list"][speed_index]][len(self.data[self.data["wind_list"][speed_index]])-1]
            else:
                boatspeed = self.data[self.data["wind_list"][speed_index]][heading_index]
        print(self.data[self.data["wind_list"][speed_index]])
        return boatspeed
        
        
