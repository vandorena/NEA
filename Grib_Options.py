from ecmwf.opendata import Client

BASECLIENT_PHYSICS = Client(
    source="ecmwf",
    model="ifs",
    resol="0p25",
    preserve_request_order=False,
    infer_stream_keyword=True,
)

BASECLIENT_DATA = Client(
    source="ecmwf",
    model="aifs",
    resol="0p25",
    preserve_request_order=False,
    infer_stream_keyword=True,
)