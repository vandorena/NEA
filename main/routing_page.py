import bokeh
from bokeh.io import curdoc
from bokeh.models import Button, Div
from globals import selected_boat,selected_grib,BUTTON_STYLE
from bokeh.layouts import column,row

def main(doc):
    infinite_while = False
    routing_started = False
    while not infinite_while:
        if routing_started == True:
            post(doc)
        else:
            pre(doc)



def post(doc):
    global selected_boat
    boat_Div = Div(text=f"<p><b>{selected_boat}</p></b>")
    grib_Div = Div(test=f"<p><b>{selected_grib}</p></b>")

    
    
    right_column = 



def pre(doc):
    start_routing_button = Button(
        label="Start Routing",
        button_type=BUTTON_STYLE["type"][2],
        width=BUTTON_STYLE["width"],
        height=BUTTON_STYLE["height"],
        icon=BUTTON_STYLE["icons"][0]
        )
    right_column = column(start_routing_button)