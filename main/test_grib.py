from Grib_Options import GRIB
import os

print(os.listdir())
my_grib = GRIB("Uploaded_at_11:37_on_6-2-2025.grib2")
print(my_grib.read_single_line(0,63))