import requests
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points


def elevation(lat, lon):
    elevURL = "https://epqs.nationalmap.gov/v1/json"
    params = {'x': lon, 'y': lat, 'units': 'Meters'}

    response = requests.get(elevURL, params=params).json()
    elevation = response['value']

    return elevation



# usgsURL = "https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60/query"
# hydroParams = {
#     'geometry': f"{lon},{lat}",
#     'geometryType': 'esriGeometryPoint',
#     'inSR': '4326',
#     'spatialRel': 'esriSpatialRelIntersects',
#     'distance': '5000',           
#     'units': 'esriSRUnit_Meter',  
#     'outFields': 'GNIS_Name',      
#     'returnGeometry': 'true',
#     'f': 'json'
# }

# hydro = requests.get(usgsURL, params=hydroParams).json()

# target = Point(lon, lat)
# minDistance = float('inf')

# if 'features' in hydro:
#     for feature in hydro['features']:
#         if 'geometry' in feature and 'paths' in feature['geometry']:
#             for path in feature['geometry']['paths']:
#                 riverLine = LineString(path)
#                 distance = target.distance(riverLine) * 111
#                 if distance < minDistance:
#                     minDistance = distance
# else:
#     print("Warning: No rivers or flowlines detected within a 5km radius.")

def soil(lat, lon):
    soilURL = "https://sdmdataaccess.nrcs.usda.gov/Tabular/post.rest"
    query = f"SELECT TOP 1 c.hydgrp, c.drainagecl FROM mapunit mu INNER JOIN component c ON mu.mukey = c.mukey WHERE mu.mukey IN (SELECT * FROM SDA_Get_Mukey_from_intersection_with_WktWgs84('POINT({lon} {lat})'))"
    soil = requests.post(soilURL, json={"query": query, "format": "json"}).json()

    return soil['Table'][0][0], soil['Table'][0][1]


# print(f"Elevation: {elevation} meters")
# # print(f"Minimum distance to river: {minDistance} km")
# print(f"Soil Hydrologic Group: {soil_data['Table'][0][0]} | Drainage Class: {soil_data['Table'][0][1]}")