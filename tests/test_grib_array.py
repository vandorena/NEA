import numpy as np
import eccodes


grib_file_name = r"gribs/thefrib.grib2"


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
    

def read_single_message(grin_file):

    with open(grin_file, "rb") as file:

        current_message = eccodes.codes_grib_new_from_file(file)
        print(eccodes.codes_get_values(current_message))
        print(eccodes.codes_get(current_message,'Ni'))
        print(eccodes.codes_get(current_message, 'date'))
        print(eccodes.codes_get(current_message,"time"))
        #print(eccodes.codes_get_values(current_message)[0:100])
        print(eccodes.codes_get(current_message,"typeOfGrid"))
        print(eccodes.codes_get(current_message,"latitudeOfLastGridPointInDegrees"))
        print(eccodes.codes_get(current_message,"shortName"))
        #print(eccodes.codes_get(current_message,"significanceOfReferenceTime"))
        #print(eccodes.codes_get(current_message,"gribLs"))
        print(type(eccodes.codes_get(current_message,"topLevel")))
        type(eccodes.codes_get(current_message,"bottomLevel"))
        #print(eccodes.codes_get(current_message,"w"))
        #print(eccodes.codes_get(current_message, "levels"))
        return
    
#print(f"{read_single_message(grib_file_name)}")

read_single_message(grib_file_name)