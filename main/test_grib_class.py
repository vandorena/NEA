from Grib_Options import GRIB

grib = GRIB("thefrib.grib2")
print(grib.read_single_line(80,70))