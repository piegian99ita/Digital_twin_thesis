import bpy
import requests
import math

# API Configurazione
api_key = "pk.0bbad14bcc06727bb61e865dc64f230b"

url = "https://opencellid.org/cell/getInArea"
format_type = "json"  # Formato dei dati restituiti

# Calcolo della bounding box (BBOX)

lat_max=46.07135
lat_min=46.05938
lon_max=11.16365
lon_min=11.14743

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

# Estrazione dei dati dal risultato JSON
data = response.json()

if "cells" not in data or len(data["cells"]) == 0:
    print("Nessuna base station trovata nell'area specificata.")
    raise SystemExit

'''
# Funzione per convertire coordinate geografiche in coordinate Blender
def geo_to_blender(lat, lon, origin_lat, origin_lon, scale_factor=1):
    """
    Converte le coordinate geografiche (latitudine e longitudine)
    in coordinate Blender con un'origine specificata.
    """
    x = (lon - origin_lon) * 111320 * math.cos(math.radians(origin_lat)) / scale_factor
    y = (lat - origin_lat) * 111320 / scale_factor
    return x, y, 0  # Z è 0 per posizionare le torri sul piano XY

# Creazione delle base station in Blender
origin_lat, origin_lon = lat, lon  # Punto di riferimento centrale
scale_factor = 1  # Fattore di scala per ridimensionare le coordinate in Blender

for cell in data["cells"]:
    cell_lat = cell["lat"]
    cell_lon = cell["lon"]
    pos_x, pos_y, pos_z = geo_to_blender(cell_lat, cell_lon, origin_lat, origin_lon, scale_factor)
    
    # Aggiungere un oggetto base station (es. un cilindro)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=5, location=(pos_x, pos_y, pos_z))
    
    # Facoltativo: Etichettare l'oggetto
    obj = bpy.context.object
    obj.name = f"BaseStation_{cell['cellid']}"

print("Base station aggiunte con successo a Blender!")
'''
