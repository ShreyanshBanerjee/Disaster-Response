import os
import zipfile
import json
import pandas as pd
import pickle
import osmnx as ox
import numpy as np
from geopy.geocoders import Nominatim

def unzip():
    zipName = "files\my_archive.zip"

    with zipfile.ZipFile(zipName, 'r') as zip_ref:
        zip_ref.extractall(path="files")
        
    print("extracted")

if __name__ == "__main__":
    unzip()

def loaddf(filepath="files/shelter_location_data.pkl"):
    with open(filepath, "rb") as f:
        return pickle.load(f)
    
def getdf(filepath="files/shelter_location_data.pkl"):
    with open(filepath, "rb") as f:
        df = pickle.load(f)
    
    return df

shelters = []

with open("files/national-shelter-system-facilities-geojson.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

for i in data["features"]:
    properties = i["properties"]

    shelters.append({"name": properties["shelter_name"], "city": properties["city"], "state": properties["state"], "capacity": properties["evacuation_capacity"], "lat": properties["latitude"], "lon": properties["longitude"]
    })

dfShelters = pd.DataFrame(shelters)

dfShelters.to_csv("files/shelters.csv", index=False)



with open("shelter_location_data.pkl", "rb") as f:
    dfShelters = pickle.load(f)
print(dfShelters)

# remeber to make a function that returns all the points in a radius of (lat, lon). use pandas to go thru it efficently

def getShelters(lat, lon, r):
    minLat = lat - r
    maxLat = lat + r
    minLon = lon - r
    maxLon = lon + r

    candidates = dfShelters[
        (dfShelters["lat"] >= minLat) &
        (dfShelters["lat"] <= maxLat) &
        (dfShelters["lon"] >= minLon) &
        (dfShelters["lon"] <= maxLon)
    ]

    distance = ((candidates["lat"] - lat) ** 2) + ((candidates["lon"] - lon) ** 2)

    return candidates[distance <= r ** 2]

nominatim_instance = Nominatim(user_agent="AIm_Prepared_App")

def get_points(lat, long):
    #using the OpenStreetMap API to access a representation of the nearby road network, in terms of graphs and edges
    G = ox.graph_from_point(
        (43.1548, -77.5486),
        dist=100,
        network_type="drive"
    )

    nodes, edges = ox.graph_to_gdfs(G)
    
    return nodes, edges

def convert_latlong_to_address(lat, long):
    return nominatim_instance.reverse((str(lat), str(long)))
    

def convert_address_to_latlong(street, city, state):
    #will add safety guards protecting against crashing from incorrect inputs
    location = nominatim_instance.geocode(f"{street}, {city}, {state}")
    return float(location.latitude), float(location.longitude)

def distance_between_latlong(a, b):
    #haversine formula
    delta_lat = abs(a[0]-b[0]) * np.pi/180
    delta_long = abs(a[1]-b[1]) * np.pi/180

    a = np.sin(delta_lat/2)**2 + np.cos(a[0]*np.pi/180) * np.cos(b[0]*np.pi/180) * np.sin(delta_long/2)**2
    c = 2*np.atan2(np.sqrt(a), np.sqrt(1-a))
    return 6371 * c

def construct_a_star():
    pass
