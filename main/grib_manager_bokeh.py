import os,datetime
from globals import CURRENT_TIME,CURRENT_SUBFOLDERS
from bokeh.models import Button,CustomJS
from bokeh.layouts import row, column

def find_gribs():
    global CURRENT_TIME,CURRENT_SUBFOLDERS
    grib_folder_list = os.listdir("gribs")
    for i in range(0,len(grib_folder_list)):
        if grib_folder_list[i][:5] == f"{CURRENT_TIME.year}-" and grib_folder_list[i][7] == "-":
            CURRENT_SUBFOLDERS["subfolder_list"].append(grib_folder_list[i])
            new_folder_gribs = os.listdir(rf"..//gribs//{grib_folder_list[i]}")
            for i in range(0,len(new_folder_gribs)):
                if new_folder_gribs[i][-6:] != ".grib2":
                    new_folder_gribs.remove(new_folder_gribs[i])
            CURRENT_SUBFOLDERS[grib_folder_list[i]] = new_folder_gribs

def grib_button(grib_name):
    pass

def gribs(doc):
    global CURRENT_SUBFOLDERS
    
    button_list = []
    for i in range(0,len(CURRENT_SUBFOLDERS["subfolder_list"])):
        grib_name = CURRENT_SUBFOLDERS["subfolder_list"][i]
        button = Button(label=grib_name)
        button.js_on_event("button_click",grib_button(grib_name))
        button_list.append(button)

    length_button_list = len(button_list)

    row1=[]
    row2=[]
    row3=[]

    for i in range(0,length_button_list):
        if i % 3 == 0:
            row1.append(button_list[i])
        elif i % 3 == 1:
            row2.append(button_list[i])
        else:
            row3.append(button_list[i])
    
    first_row = row(row1)
    second_row = row(row2)
    third_row = row(row3)

    layout = column(first_row,second_row,third_row)

    doc.add_root(layout)

if __name__ == "__main__":
    find_gribs()
    print(globals.CURRENT_SUBFOLDERS)