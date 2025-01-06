import openmeteo_requests
import requests_cache
import retry_requests
import datetime

def opening_sesh():
    cached_session = requests_cache.CachedSession('.cache', expire_after = 4000)
    retry_session = retry_requests(cached_session, retries = 5, backoff_factor = 0.2)
    meteo = openmeteo_requests.Client(session = retry_session)
    return meteo

def make_10mvu_request(lat,lon,time:datetime):
    meteo = opening_sesh()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":lat,
        "longitude": lon,
        "minutely_15":["wind_speed_10m","wind_direction_10m"],
        "timezone": "gmt",
        "forecast_days": 1
    }
    response = meteo.weather_api(url, params=params)
    print(response)
    first_response = response[0]
    print(first_response.Minutely15())

if __name__ == "_main_":
    make_10mvu_request(0,0,datetime.datetime.now())