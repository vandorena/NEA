from boats import Boat
from globals import CURRENT_BOATS, BUTTON_STYLE
from bokeh.models import Button
from bokeh.layouts import row, column
from bokeh.models import CustomJS

def find_boats():
    with open("..\Boats\Boat_saves.txt","r") as file:
        boats = file.readlines()
    for i in range(0,len(boats)):
        line_content = boats[i].split()
        boat = Boat(line_content[0])
        CURRENT_BOATS["boat_list"].append(line_content[0])
        boat.add_polar(line_content[1])
        CURRENT_BOATS[line_content[0]] = boat
        boat = None

def boats(doc):
    find_boats()
    add_boat = Button(label="Add a New Boat",button_type=BUTTON_STYLE["type"][0],width=BUTTON_STYLE["width"],height=BUTTON_STYLE["height"],icon=BUTTON_STYLE["icons"][0])
    add_boat.js_on_event('button_click',CustomJS(code="window.location.href='/new_boat"))


if __name__ == "__main__":
    find_boats()