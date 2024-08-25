import os
import pygrib


print(f"Current working directory: {os.getcwd()}")


# Define the relative path to the GRIB file
path = '/gribs/test.grib'

# Get the absolute path for debugging purposes
absolute_path = os.path.abspath(path)
print(f"Attempting to open GRIB file at: {absolute_path}")

# Open the GRIB file
grib_file = pygrib.open(path)

# Loop through all messages in the GRIB file
for message in grib_file:
    print(f"Message: {message}")
    print(f"Short name: {message.shortName}")
    print(f"Parameter name: {message.name}")
    print(f"Data date: {message.dataDate}")
    print(f"Data time: {message.dataTime}")
    print(f"Level type: {message.typeOfLevel}")
    print(f"Level: {message.level}")
    
    # Retrieve the actual data
    data, lats, lons = message.data()
    print(f"Data shape: {data.shape}")
    print(f"Latitude range: {lats.min()} to {lats.max()}")
    print(f"Longitude range: {lons.min()} to {lons.max()}")
    print()

# Close the GRIB file
grib_file.close()
