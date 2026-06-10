import requests
from datetime import datetime 
from datetime import timezone


def elevation(lat, lon):
    elevURL = "https://epqs.nationalmap.gov/v1/json"
    params = {'x': lon, 'y': lat, 'units': 'Meters'}

    response = requests.get(elevURL, params=params).json()
    elevation = response['value']

    return elevation


def soil(lat, lon):
    soilURL = "https://sdmdataaccess.nrcs.usda.gov/Tabular/post.rest"
    query = f"SELECT TOP 1 c.hydgrp, c.drainagecl FROM mapunit mu INNER JOIN component c ON mu.mukey = c.mukey WHERE mu.mukey IN (SELECT * FROM SDA_Get_Mukey_from_intersection_with_WktWgs84('POINT({lon} {lat})'))"
    soil = requests.post(soilURL, json={"query": query, "format": "json"}).json()

    return soil['Table'][0][0], soil['Table'][0][1]

def weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "precipitation,relative_humidity_2m,temperature_2m,wind_speed_10m",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "auto"
    }

    data = requests.get(url, params=params, timeout=10).json()

    precip = data["hourly"]["precipitation"]
    humidity = data["hourly"]["relative_humidity_2m"]
    temp = data["hourly"]["temperature_2m"]
    wind = data["hourly"]["wind_speed_10m"]

    i = 24

    rain3 = 0
    for j in range(-2, 1):
        rain3 += precip[i + j]
    
    rain24 = 0
    for j in range(-23, 1):
        rain24 += precip[i + j]

    month = datetime.now().month
    if month >= 6 and month <= 9:
        isRainySzn = 1
    else:
        isRainySzn = 0

    return {
        "rainfall_1h": precip[i],
        "rainfall_3h": rain3,
        "rainfall_24h": rain24,
        "humidity": humidity[i],
        "temperature": temp[i],
        "wind_speed": wind[i],
        "month": month,
        "is_rainy_szn": isRainySzn
    }