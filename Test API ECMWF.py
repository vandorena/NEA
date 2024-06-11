from ecmwf.opendata import Client

client = Client()

client.retrieve(
    source="azure",
    model="aifs",
    step=240,
    type="fc",
    param="msl",
    target="data.grib2",
)