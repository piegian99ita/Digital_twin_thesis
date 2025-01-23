import bpy

def create_plane(scale):
    bpy.ops.mesh.primitive_plane_add(size=scale*15, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    
    #add a material to the plane 
    plane = bpy.context.object
    material = bpy.data.materials.get("itu_concrete")
    plane.data.materials.append(material)  



def import_all_osm_data(latitude, longitude, scale):
    """
    Importa tutti i tipi di dati OpenStreetMap disponibili utilizzando l'add-on Blosm.

    Args:
        latitude (float): Latitudine del centro.
        longitude (float): Longitudine del centro.
        scale (int): Scala della mappa (area coperta).
    """
     # Assicurati che l'add-on Blosm sia attivo
    if "blender-osm" not in bpy.context.preferences.addons and "blosm" not in bpy.context.preferences.addons:
        print("Blosm non è attivo. Attivalo nelle preferenze.")
        return

    # Itera su tutti i tipi di dati e importa ciascuno
    
        
    bpy.context.scene.blosm.latitude = latitude
    bpy.context.scene.blosm.longitude = longitude
    bpy.context.scene.blosm.scale = scale
    
    # Settaggi di importazione
    bpy.context.scene.blosm.mode = "3Dsimple"
    bpy.context.scene.blosm.buildings = True
    bpy.context.scene.blosm.water = True
    bpy.context.scene.blosm.forests = True
    bpy.context.scene.blosm.vegetation = True
    bpy.context.scene.blosm.highways = True
   
    
    bpy.context.scene.blosm.defaultRoofShape = 'flat'
    bpy.context.scene.blosm.levelHeight = 3
    bpy.context.scene.blosm.singleObject = True
    bpy.context.scene.blosm.relativeToInitialImport = True
    
    
    bpy.context.scene.blosm.defaultLevels[0].levels = 4
    bpy.context.scene.blosm.defaultLevels[1].levels = 5
    bpy.context.scene.blosm.defaultLevels[2].levels = 6


    bpy.context.scene.blosm.defaultLevels[0].weight = 10
    bpy.context.scene.blosm.defaultLevels[1].weight = 40
    bpy.context.scene.blosm.defaultLevels[2].weight = 10
    
    bpy.context.scene.blosm.terrainObject = ""









        
        
        # Esegui l'operatore per scaricare ed importare i dati
    bpy.ops.blosm.import_data()
    
    print("importato con successo!")

# Esempio di utilizzo
latitude = 46.065
longitude = 11.15
scale = 100   # Area di copertura in metri
create_plane(scale)
import_all_osm_data(latitude, longitude, scale)
