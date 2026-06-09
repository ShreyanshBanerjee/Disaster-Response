import os
import zipfile

def unzip():
    zipName = "files\my_archive.zip"
    file = "national-shelter-system-facilities-geojson.geojson"
            
    with zipfile.ZipFile(zipName, 'r') as zip_ref:
        zip_ref.extractall(path="files")
        
    print("extracted")

if __name__ == "__main__":
    unzip()


