from ecmwf.opendata import Client
import datetime




def start_stop_dates_time():

    """
    returns yyyymmdd format,
    returns the cycle, current date, as well as a date 3 days later.
    """
    yyyymmdd = str(datetime.datetime.now())
    yyyymmdd = f"{yyyymmdd[:4]}{yyyymmdd[5:7]}{yyyymmdd[8:10]}{yyyymmdd[10:11]}"
    #print(yyyymmdd)
    #print(datetime.datetime.now())
    cycle = str(datetime.datetime.now())
    cycle = int(cycle[11] + cycle[12])
    if cycle < 6:
        cycle = "00"
    elif cycle >= 6 and cycle < 12:
        cycle == "06"
    elif cycle >= 12 and cycle < 18:
        cycle == "12"
    else:
        cycle == "18"
    enddate = datetime.datetime.now()
    enddate = enddate + datetime.timedelta(3)
    enddate = f"{yyyymmdd[:4]}{yyyymmdd[5:7]}{yyyymmdd[8:10]}{yyyymmdd[10:11]}"

    return cycle, yyyymmdd,enddate


if __name__ == "__main__":
    time,start,stop = start_stop_dates_time()
    client = Client()

    client.retrieve(
        source="azure",
        model="ifs",
        step=240,
        type="fc",
        param="msl",
        infer_stream_keyword=True,
        target="..\gribs\data.grib2",
    )
