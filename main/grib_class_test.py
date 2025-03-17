from Grib_Options import GRIB

print("Test 1.1")
grib = GRIB("dummy.grib2")
for i in range(0,len(dir(grib))):
    print(eval(f"grib.{dir(grib)[i]}"))

print("Test 2.1")
grib = GRIB("Uploaded_at_7:26_on_9-2-2025.grib2")
print("Test 2.2")
grib = GRIB("ECMWF_W_50k_3d_6h_84N_-38S_37E_-120W_20250209_1750.grib2")
print(dir(grib))
print("Test 3.1")
grib = GRIB("ECMWF_W_50k_3d_6h_84N_-38S_37E_-120W_20250209_1750.grib2")
print(grib.getWindAt(1,23,10))
print("Test 2.3")
grib = GRIB("empty.grib2")