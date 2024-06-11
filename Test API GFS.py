import requests
import datetime


def getgrib():
    yyyymmdd = str(datetime.datetime.now())
    yyyymmdd = f"{yyyymmdd[:4]}{yyyymmdd[5:7]}{yyyymmdd[8:10]}{yyyymmdd[10:11]}"
    print(yyyymmdd)
    print(datetime.datetime.now())
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
    return requests.post(f"https://www.ncei.noaa.gov/cdo-web/api/v2/datasets")

print(str(getgrib()))