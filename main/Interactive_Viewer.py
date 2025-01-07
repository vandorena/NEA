from bokeh.plotting import figure, show, curdoc
from bokeh.models import ColumnDataSource, Slider, Button
from bokeh.models.callbacks import CustomJS
from bokeh.layouts import column,row

def viewer(doc):
    plot = figure(x_range=(-2000000, 2000000), y_range=(1000000, 7000000),
            x_axis_type="mercator", y_axis_type="mercator", height=500,width=1000)

    plot.add_tile("CartoDB Positron", retina=True)

    doc.add_root(plot)


if __name__ == "__main__":
    viewer(curdoc())