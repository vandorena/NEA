import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Spectral10
from bokeh.models import Patch

# Data in polar coordinates
azimuths = np.linspace(0, 2 * np.pi, 20)
ranges = np.array([2, 4, 6, 8])

# Convert to x and y meshes
azimuths_m, ranges_m = np.meshgrid(azimuths, ranges)
xx = ranges_m * np.cos(azimuths_m)
yy = ranges_m * np.sin(azimuths_m)

# Array of color values
C = np.random.randint(0, 10, xx.shape)
colors = Spectral10  # Use a built-in color palette with 10 colors


def pcolor(plot, C, xx, yy):
    """ Create a pseudocolor-like plot. Note the last points in C ignored. """
    xx_count, yy_count = xx.shape

    for j in range(yy_count - 1):
        for i in range(xx_count - 1):
            # Coordinates for the quadrilateral
            ys = [yy[i, j], yy[i, j + 1], yy[i + 1, j + 1], yy[i + 1, j]]
            xs = [xx[i, j], xx[i, j + 1], xx[i + 1, j + 1], xx[i + 1, j]]
    
            plot.patch(xs, ys, fill_color=None, line_color=None)


# Create plot
output_file("sample.html", title="Sample Example")
plot = figure(title="Pseudocolor Plot", x_axis_label="X", y_axis_label="Y", match_aspect=True)

# Create pseudocolor plot
pcolor(plot, C, xx, yy)

# Show plot
show(plot)
