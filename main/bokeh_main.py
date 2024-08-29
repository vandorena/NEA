from bokeh.server.server import Server
from mainpage import create_main_page
from boats_bokeh import boats
from new_boat_bokeh import new_boats
from grib_manager_bokeh import gribs
from boat_view_bokeh import view_boat

routes = {
    "/": create_main_page,
    "/boats": boats,
    "/new_boat": new_boats,
    "/grib_manager": gribs,
    "/view_boat": view_boat,
}

def make_document(doc, app):
    app(doc)
    doc.title = "Weather Routing"

def main():
    server = Server(
        {route: (lambda doc, app=app: make_document(doc, app)) for route, app in routes.items()},
        num_procs=1
        )
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()

if __name__ == "__main__":
    main()