import os,datetime
CURRENT_TIME = datetime.datetime.now()

CURRENT_GRIBS = {
    "grib_list":[]
}

CURRENT_SUBFOLDERS ={
    "subfolder_list":[]
}

def find_gribs():
    grib_folder_list = os.listdir("..//gribs")
    for i in range(0,len(grib_folder_list)):
        print(grib_folder_list[i][:5])
        print(grib_folder_list[i])
        if grib_folder_list[i][:5] == f"{CURRENT_TIME.year}-" and grib_folder_list[i][7] == "-":
            print("Ya")

find_gribs()