from globals import CURRENT_BOATS, selected_boat, BUTTON_STYLE
import bokeh
from bokeh.io import curdoc
from bokeh.layouts import row,column
from bokeh.models import Button,Div,CustomJS,ColumnDataSource, DataTable, DateFormatter, TableColumn

def check_boat(doc):
    try:
        print(f"{selected_boat}")
        boat_object = selected_boat
        
        source = ColumnDataSource(boat_object.data)
        columns = []
        columns.append(TableColumn(field=boat_object.data["heading_list"], title = "Headings (degrees to true wind)"))
        for i in range(0,len(boat_object.data["wind_list"])):
            columns.append(TableColumn(field=boat_object.data[boat_object.data["wind_list"][i]],title=f"{boat_object.data['wind_list'][i]}knts"))
        table = DataTable(source=source,columns=columns)

        back_boats_button = Button(label="Boats Page",button_type=BUTTON_STYLE["type"][0],width=BUTTON_STYLE["width"],height=BUTTON_STYLE["height"],icon=BUTTON_STYLE["icons"][0])
        back_boats_button.js_on_event('button_click',CustomJS(code="window.location.href='/boats"))

        layout = row(table,back_boats_button)
        doc.add_root(layout)
    except AttributeError:
        pass

def view_boat(doc):
    if selected_boat is None:
        CustomJS(code="window.location.href='/boats")
    else:
        check_boat(doc,selected_boat)

check_boat(curdoc())