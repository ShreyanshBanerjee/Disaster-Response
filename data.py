import osmnx as ox
from geopy.geocoders import Nominatim

nominatim_instance = Nominatim(user_agent="AIm_Prepared_App")

def get_points(lat, long):
    #using the OpenStreetMap API to access a representation of the nearby road network, in terms of graphs and edges
    G = ox.graph_from_point(
        (43.1548, -77.5486),
        dist=1000,
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
