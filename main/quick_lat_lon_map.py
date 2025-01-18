
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource

# Example latitude and longitude arrays
lats = [41.842775836063375, 42.663713201208274, 43.47174552441022, 44.22723473382097, 44.90888800606786, 45.57642503645703, 46.189476228811266, 46.856756487673685, 47.52389805195687, 48.136608412867474, 48.74920616827785, 49.36168855977664, 50.00006586595576, 50.552926806522315, 51.14950993503627, 51.69360254454381, 52.153329661160114, 52.46522987570518]
lons = [-22.72027660178584, -21.39142769739776, -20.065948143354333, -18.811325248506012, -17.666755393052274, -16.53261301108222, -15.48002494684494, -14.319122582438709, -13.143533258775568, -12.051637237203211, -10.946490531618508, -9.827640700269264, -8.645381944901764, -7.610672813659781, -6.478797061198587, -5.434815261734658, -4.544697603414347, -3.937919853905454]


# Convert lat/lon to Web Mercator projection for Bokeh
def mercator_projection(lat, lon):
    import math
    r_major = 6378137.000
    x = r_major * math.radians(lon)
    scale = x / lon if lon != 0 else 1
    y = r_major * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * scale
    return x, y

# Project lats and lons
merc_x, merc_y = zip(*[mercator_projection(lat, lon) for lat, lon in zip(lats, lons)])

# Create data source
source = ColumnDataSource(data=dict(x=merc_x, y=merc_y))

# Initialize plot

p = figure(title="Lat/Lon Path on Map", x_axis_type="mercator", y_axis_type="mercator",width = 1500, height = 900)
p.add_tile("CartoDB Positron", retina=True)
             

# Plot points and line
#p.line('x', 'y', source=source, line_width=2, color='blue', legend_label="Path")
p.scatter('x', 'y', source=source, size=8, color='red', legend_label="Points")

# Show plot
show(p)
