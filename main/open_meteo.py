import requests
import requests_cache
import retry_requests
import datetime

def fallback_nws_request(lat,lon,time:datetime):
    first_request_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    first_response = requests.get(first_request_url)
    while first_response.status_code != 200:
        first_response = requests.get(first_request_url)
    first_response_data = first_response.json()
    second_response_url = first_response_data["properties"]["forecast"]
    second_response = requests.get(second_response_url)
    while second_response.status_code != 200:
        second_response = requests.get(second_response_url)

    index = None
    difference = datetime.timedelta.max

    for i in range(0,len(response_data["minutely_15"]["time"])):
            current_datetime = datetime.datetime.fromisoformat(response_data["minutely_15"]["time"][i])
            delta = abs(current_datetime - time)
            if delta < difference:
                difference = delta
                index = i
    

def make_10mvu_request(lat,lon,time:datetime):
    #print("Request made!")
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":lat,
        "longitude": lon,
        "minutely_15":"windspeed_10m,winddirection_10m",
        "timezone": "UTC",
        "forecast_days": 1
    }
    try:
        response = requests.get(url,params=params)
        response_data = response.json()
        #print(response_data)
    except requests.exceptions.HTTPError:
        response = requests.get(url,params=params)
        response_data = response.json()
        #print(response_data)

    if 'error' in response_data:
        print(response_data['error'])

    index = None
    difference = datetime.timedelta.max

    try:
        for i in range(0,len(response_data["minutely_15"]["time"])):
            current_datetime = datetime.datetime.fromisoformat(response_data["minutely_15"]["time"][i])
            delta = abs(current_datetime - time)
            if delta < difference:
                difference = delta
                index = i
    except BaseException:
        print(response_data)

    return response_data["minutely_15"]["windspeed_10m"][index], response_data["minutely_15"]["winddirection_10m"][index]

if __name__ == "__main__":
    print(make_10mvu_request(50,50,datetime.datetime.now()))