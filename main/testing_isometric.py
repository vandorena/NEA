import routing_model,Grib_Options,boats,path,datetime,os

#ecwmf = Grib_Options.ECMWF_API()
#ecwmf.make_request()
boat = boats.Boat("sunfast3600")
boat.add_polar("sunfast3600.pol")
grib = Grib_Options.GRIB(os.path.join(f"{datetime.datetime.today().year}-{datetime.datetime.today().month}-{datetime.datetime.today().day}","12-0-0.grib2"))
path_s = path.Path(start_time=datetime.datetime.now(), start_lattitude=0,start_longitude=0,end_latitude=15,end_longitude=15, boat=boat)
routing_modes = routing_model.Routing_Model(path=path_s,grib=grib)
routing_modes.create_big_circle_route()
print(routing_modes.isometric(path_s.start_lattitude, path_s.start_longitude, path_s.start_time))