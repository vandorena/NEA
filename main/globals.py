import datetime
from ecmwf.opendata import Client

NETWORK_STATUS = False
CURRENT_BOATS = {"boat_list":[]}
CURRENT_TIME = datetime.datetime.now()
CURRENT_SUBFOLDERS ={
    "subfolder_list":[]
}
BASECLIENT_DATA = Client(
    source="ecmwf",
    model="aifs",
    resol="0p25",
    preserve_request_order=False,
    infer_stream_keyword=True,
)
BASECLIENT_PHYSICS = Client(
    source="ecmwf",
    model="ifs",
    resol="0p25",
    preserve_request_order=False,
    infer_stream_keyword=True,
)