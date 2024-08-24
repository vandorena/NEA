import os,datetime

CURRENT_TIME = datetime.datetime.now()

CURRENT_SUBFOLDERS ={
    "subfolder_list":[]
}

def find_gribs():
    grib_folder_list = os.listdir("..//gribs")
    for i in range(0,len(grib_folder_list)):
        if grib_folder_list[i][:5] == f"{CURRENT_TIME.year}-" and grib_folder_list[i][7] == "-":
            CURRENT_SUBFOLDERS["subfolder_list"].append(grib_folder_list[i])
            new_folder_gribs = os.listdir(f"..//gribs//{grib_folder_list[i]}")
            for i in range(0,len(new_folder_gribs)):
                if new_folder_gribs[i][-6:] != ".grib2":
                    new_folder_gribs.remove(new_folder_gribs[i])
            CURRENT_SUBFOLDERS[grib_folder_list[i]] = new_folder_gribs

if __name__ == "__main__":
    find_gribs()