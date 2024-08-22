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
                        if (j % 2) == 1:
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

    def find_polar_speed(self,windspeed,heading):
        reference_speeds = self.data["wind_list"]
        reference_headings = self.data["heading_list"]
                    