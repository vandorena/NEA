from boats import Boat
from globals import CURRENT_BOATS, BUTTON_STYLE, selected_boat
from bokeh.models import Button
from bokeh.layouts import row, column
from bokeh.models import CustomJS

def find_boats():
    with open(r"..\Boats\Boat_saves.txt","r") as file:
        boats = file.readlines()
    for i in range(0,len(boats)):
        line_content = boats[i].split()
        boat = Boat(line_content[0])
        CURRENT_BOATS["boat_list"].append(line_content[0])
        boat.add_polar(line_content[1])
        CURRENT_BOATS[line_content[0]] = boat
        boat = None

def boat_button(boat):
    selected_boat = boat
    CustomJS(code="window.location.href='/view_boat")


def boats(doc):
    """Need to work on how to dynamically create buttons based on how many boats are there."""
    find_boats()
    


    add_boat = Button(label="Add a New Boat",button_type=BUTTON_STYLE["type"][0],width=BUTTON_STYLE["width"],height=BUTTON_STYLE["height"],icon=BUTTON_STYLE["icons"][0])
    add_boat.js_on_event('button_click',CustomJS(code="window.location.href='/new_boat"))

    button_list = [add_boat]
    for i in range(0,len(CURRENT_BOATS["boat_list"])):
        button = Button(label=CURRENT_BOATS["boat_list"][i])
        button.on_event("click",boat_button(CURRENT_BOATS["boat_list"][i]))
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
    find_boats()