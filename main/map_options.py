import numpy as np
import math
from globals import mapwidth,mapheight

class Map_methods:

    def __init__(self) -> None:
        pass

    def lat_lon_mercator(lat,lon)-> tuple:
        x = (lon + 180) * (mapwidth/360)
        y = (mapheight*0.5)-(mapwidth*(np.log(np.tan( np.pi * 0.25+ (math.radians(lat))*0.5))/(2*np.pi)))
        return x,y

    def mercator_lat_lon(x,y)->tuple:

        return lat,lon