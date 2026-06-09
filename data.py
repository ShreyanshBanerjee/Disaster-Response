import osmnx as ox
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

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
