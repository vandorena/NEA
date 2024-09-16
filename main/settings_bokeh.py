import bokeh
from bokeh.io import curdoc
from bokeh.models import Button, Slider
from bokeh.layouts import row,column
from globals import SETTINGS,mapheight,mapwidth

def update_width_height(attr,old,new):
    global mapheight,mapwidth
    mapheight = map_height_slider.value
    mapwidth = map_width_slider.value
    return

def settings(doc):

    map_width_slider = Slider(start=100,end=1000,step=10,value=mapwidth,lable="Map Width in Pixels")
    map_height_slider = Slider(start=100,end=900,step=10,value=mapheight,lable="Map Height in Pixels")

    map_width_slider.on_change("value", update_width_height)

    column1 = column(map_height_slider,map_width_slider)
    doc.add_root()
    