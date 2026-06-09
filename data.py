import os
import zipfile
import json
import pandas as pd
import pickle

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

print(getShelters(41.8268, -72.5533, 50))

