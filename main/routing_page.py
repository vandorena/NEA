import bokeh
from bokeh.io import curdoc
from bokeh.models import Button, Div
from globals import selected_boat,selected_grib

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

    start_routing_button = Button()



def pre(doc):
    pass 