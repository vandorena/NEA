import bokeh, requests
import globals
from globals import BUTTON_STYLE
from bokeh.models import Button
from bokeh.layouts import row,column
from bokeh.models.callbacks import CustomJS

def check_network_status():
    try:
        requests.get(r"https://www.google.com",timeout=10)
        globals.NETWORK_STATUS = True
    except requests.ConnectionError:
        globals.NETWORK_STATUS = False

def create_main_page(doc):
    button_boats = Button(label="Boats Page",button_type=BUTTON_STYLE["type"][0],width=BUTTON_STYLE["width"],height=BUTTON_STYLE["height"],icon=BUTTON_STYLE["icons"][0])
    button_boats.js_on_event('button_click',CustomJS(code="window.location.href='/boats'"))

    layout = row(button_boats)
    doc.add_root(layout)
