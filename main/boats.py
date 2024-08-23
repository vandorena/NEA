import numpy as np

class PolarFileError(Exception):
    """Exception Raised when the Polar File is non homogenous"""
class Boat:

    def __init__(self,name: str) -> None:
        self.data = {
            "name":name
        }

    def add_polar(self,filename:str):
        with open(filename,"r") as file:
            line_array = file.readlines()
        wind_speeds = []
        speeds = []
        headings = []
        for i in range(0,len(line_array)):
            values = line_array[i].split()
            speedholder = []
            heading_count = 0
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
        
        self.data["wind_list"] = wind_speeds 
        self.data["heading_list"] = headings
        for i in range(0,len(wind_speeds)):
            self.data[wind_speeds[i]] = speeds[i]
        return

    def _list_to_int(self,list:list):
        new_list = []
        for i in range(0,len(list)):
            new_list.append(int(list[i]))
        return new_list
    
    def _binary_list_class_search(self,input_list: list, search_term: int):
        list_length = len(input_list)
        current_index = list_length//2
        found = False
        current_comparision = 0
        max_comparison = np.log2(list_length)
        count = 1
        found_index = -1
        while not found:
            if current_comparision <= max_comparison:
                if input_list[current_index] == search_term:
                    found_index = current_index
                    found = True
                else:
                    count +=1
                    if input_list[current_index] < search_term:
                        current_index = current_index + list_length//(2**count)
                    else:
                        current_index = current_index - list_length//(2**count)
            else:
                for i in range(0,list_length):
                    if input_list[i-1] < search_term and input_list[i] > search_term:
                        found_index = i
                        found = True
        return found_index
                
    def find_polar_speed(self,windspeed,heading):
        reference_windspeeds = self._list_to_int(self.data["wind_list"])
        reference_headings = self._list_to_int(self.data["heading_list"])
        speed_index = self._binary_list_class_search(reference_windspeeds,windspeed)
        heading_index = self._binary_list_class_search(reference_headings,heading)
        boatspeed = self.data[self.data["wind_list"][speed_index]][heading_index]
        return boatspeed
        
        
