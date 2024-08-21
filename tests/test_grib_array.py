import numpy as np
import eccodes


grib_file_name = '../gribs/test.grb'


def read_all_grib_messages(grib_file):
    # Open the GRIB file
    with open(grib_file, 'rb') as f:
        # Initialize an empty list to store the data arrays
        data_list = []

        while True:
            # Read the next message from the GRIB file
            gid = eccodes.codes_grib_new_from_file(f)
            if gid is None:
                break

            # Get the data values from the GRIB message
            values = eccodes.codes_get_values(gid)
            
            # Retrieve the grid dimensions (number of points)
            n_lat = eccodes.codes_get(gid, 'Nj')
            n_lon = eccodes.codes_get(gid, 'Ni')

            # Reshape the flat data array into a 2D array
            data_array = np.array(values).reshape(n_lat, n_lon)
            
            # Append the 2D array to the list
            data_list.append(data_array)

            # Release the message from memory
            eccodes.codes_release(gid)

        return data_list
    
    
print(f"{read_all_grib_messages(grib_file_name)}")