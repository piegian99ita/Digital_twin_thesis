import bpy
import requests
import math
import json

#class used to translate values into coordinates from latitude and longitude (taken from Blosm utils)
class TransverseMercator:
    radius = 6378137.

    def __init__(self, **kwargs):
        # setting default values
        self.lat = 0. # in degrees
        self.lon = 0. # in degrees
        self.k = 1. # scale factor
        
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        self.latInRadians = math.radians(self.lat)

    def fromGeographic(self, lat, lon):
        lat = math.radians(lat)
        lon = math.radians(lon-self.lon)
        B = math.sin(lon) * math.cos(lat)
        x = 0.5 * self.k * self.radius * math.log((1.+B)/(1.-B))
        y = self.k * self.radius * ( math.atan(math.tan(lat)/math.cos(lon)) - self.latInRadians )
        return (x, y, 0.)

    def toGeographic(self, x, y):
        x = x/(self.k * self.radius)
        y = y/(self.k * self.radius)
        D = y + self.latInRadians
        lon = math.atan(math.sinh(x)/math.cos(D))
        lat = math.asin(math.sin(D)/math.cosh(x))

        lon = self.lon + math.degrees(lon)
        lat = math.degrees(lat)
        return (lat, lon)

def latlon_to_mercator(lat, lon, lat0, lon0):
    R = 6378137  # Raggio della Terra in metri
    x = R * math.radians(lon - lon0)
    y = R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return x, y


api_key = "pk.0bbad14bcc06727bb61e865dc64f230b"

url = "https://opencellid.org/cell/getInArea"
format_type = "json"  

# Calcolo della bounding box (BBOX) e dell'origine

lat_max=46.07135
lat_min=46.05938
lon_max=11.16365
lon_min=11.14743
lat0=(lat_max+lat_min)/2
lon0=(lon_max+lon_min)/2

# Creazione della stringa del payload
payload = {
    "key": api_key,
    "BBOX": f"{lat_min},{lon_min},{lat_max},{lon_max}",
    "format": format_type
}

# Effettuare la richiesta GET per ottenere le base station
response = requests.get(url, params=payload)

if response.status_code != 200:
    print(f"Errore nella richiesta API: {response.status_code}")
    print(response.text)
    raise SystemExit


data = response.json()

if "cells" not in data or len(data["cells"]) == 0:
    print("Nessuna base station trovata nell'area specificata.")
    raise SystemExit


with open("base_stations.json", "w") as f:
    json.dump(data, f, indent=4)


xyz_coordinates = []

projection = TransverseMercator(lat=lat0, lon=lon0)

for cell in data["cells"]:
    x, y, _ = projection.fromGeographic(cell["lat"], cell["lon"])
    xyz_coordinates.append((x, y, 0))

with open("bs_location.json", "w") as f:
    json.dump(xyz_coordinates, f, indent=4)