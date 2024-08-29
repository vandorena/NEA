from globals import CURRENT_BOATS, SELECTED_BOAT, BUTTON_STYLE
import bokeh
from bokeh.models import Button,Div,CustomJS

def check_boat(doc,boat: str):
    boat_object = CURRENT_BOATS[SELECTED_BOAT]
    


    back_boats_button = Button(label="Boats Page",button_type=BUTTON_STYLE["type"][0],width=BUTTON_STYLE["width"],height=BUTTON_STYLE["height"],icon=BUTTON_STYLE["icons"][0])

    back_boats_button.js_on_event('button_click',CustomJS(code="window.location.href='/boats"))

def view_boat(doc):
    if SELECTED_BOAT == None:
        CustomJS(code="window.location.href='/boats")
    else:
        check_boat(doc,SELECTED_BOAT)