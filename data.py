import os
import zipfile
import json
import pandas as pd
import pickle
import osmnx as ox
import numpy as np
from geopy.geocoders import Nominatim

#shelter data
with open("shelter_location_data.pkl", "rb") as f:
    shelter_data = pickle.load(f)  

def get_shelters_data(lat, lon, r):
    if shelter_data is None:
        load_shelters_data()

    minLat = lat - r*0.01
    maxLat = lat + r*0.01
    minLon = lon - r*0.01
    maxLon = lon + r*0.01

    candidates = shelter_data[
        (shelter_data["lat"] >= minLat) &
        (shelter_data["lat"] <= maxLat) &
        (shelter_data["lon"] >= minLon) &
        (shelter_data["lon"] <= maxLon)
    ]

    distance = distance_between_latlong((candidates["lat"], candidates["lon"]), (lat, lon))

    return candidates[distance <= r]

#geolocation math
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
