import bpy
from mathutils import Vector
import os


def findPlaneDimension():
    
    x_min = float('inf')
    x_max = float('-inf')
    y_min = float('inf')
    y_max = float('-inf')

    for obj in bpy.context.scene.objects:        
        if obj.type == 'MESH':
            for vert in obj.bound_box:
                world_vert = obj.matrix_world @ Vector(vert)
                x_min = min(x_min, world_vert.x)
                x_max = max(x_max, world_vert.x)
                y_min = min(y_min, world_vert.y)
                y_max = max(y_max, world_vert.y)

    
    return max(abs(x_min),abs(y_min),x_max,y_max)



def createPlane(dimension):
    bpy.ops.mesh.primitive_plane_add(size=dimension, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(5, 5, 1))
    #add a material to the plane 
    plane = bpy.context.object
    itu_concrete = bpy.data.materials.get("itu_concrete")
    if plane.data.materials:
        # assign to 1st material slot
        plane.data.materials[0] = itu_concrete
    else:
        # no slots
        plane.data.materials.append(itu_concrete)

#FUNCTION USED TO SELECT OBJECTS IN THE SCENE BY THE NAME PATTERN
def selectObjects(theObjectName):
    for o in theObjectName: 
        bpy.ops.object.select_pattern(pattern=o)

def assignMaterials(material_1,material_2,material_3):

    # 
    itu_concrete = bpy.data.materials.get(material_1)
    itu_brick= bpy.data.materials.get(material_2)
    itu_plasterboard= bpy.data.materials.get(material_3)
    
    ###    CHANGE MATERIALS TO THE SCENE'S OBJECTS

    theObjects = ["*buildings*"] 
    selectObjects(theObjects)

    selectedObjects =  bpy.context.selected_objects
   
    for obj in selectedObjects:
        if obj.data.materials:
            # If the object already has materials iterate over the material slots
            for i in range(len(obj.data.materials)):
                material = obj.data.materials[i]

                # Check the material name and assign a new material accordingly
                if material.name == "wall":
                    obj.data.materials[i] = itu_plasterboard
                elif material.name == "roof":
                    obj.data.materials[i] = itu_brick
                else:
                    obj.data.materials[i] = itu_concrete
        else:
            # If no materials are present add the default material
            obj.data.materials.append(itu_concrete)

    

    



def importOsmData(min_lat, max_lat, min_lon, max_lon):

    # check if the add-on is installed
    if "blender-osm" not in bpy.context.preferences.addons and "blosm" not in bpy.context.preferences.addons:
        print("Blosm is not activated.")
        return

    #coordinates assignmente
    bpy.context.scene.blosm.minLat = min_lat
    bpy.context.scene.blosm.maxLat = max_lat
    bpy.context.scene.blosm.minLon = min_lon
    bpy.context.scene.blosm.maxLon = max_lon
    
    
    # import settings and what objects to import
    bpy.context.scene.blosm.mode = "3Dsimple"
    bpy.context.scene.blosm.buildings = True
    bpy.context.scene.blosm.water = False
    bpy.context.scene.blosm.forests = False
    bpy.context.scene.blosm.vegetation = False
    bpy.context.scene.blosm.highways = False
   
    
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
        
    # import operator
    bpy.ops.blosm.import_data()
    
    

def createMaterials(material_1,material_2,material_3):
    
    # materials creation 
    itu_concrete = bpy.data.materials.new(name=material_1)
    itu_brick= bpy.data.materials.new(name=material_2)
    itu_plasterboard= bpy.data.materials.new(name=material_3)

    itu_concrete.use_nodes=True
    itu_plasterboard.use_nodes=False
    itu_brick.use_nodes=False
    
    # change material color
    itu_brick.diffuse_color = (0.0833207, 0.0202846, 0.00993753, 1) 
    itu_plasterboard.diffuse_color = (0.283222, 0.748403, 0.143687, 1)


    # Get the material's node tree
    node_tree1 = itu_concrete.node_tree
    

    # Look for an existing Diffuse BSDF node
    diffuse_node1 = None
    for node in node_tree1.nodes:
        if node.type == "BSDF_DIFFUSE":
            diffuse_node1 = node
            break
   
    # If no Diffuse BSDF node exists, create one
    if not diffuse_node1:
        diffuse_node1 = node_tree1.nodes.new(type="ShaderNodeBsdfDiffuse")
        diffuse_node1.location = (0, 0)

    # Set the color of the Diffuse BSDF
    diffuse_node1.inputs["Color"].default_value = (0.237326, 0.295693, 0.287148, 1)    

    # Look for the Material Output node
    output_node1 = None
    for node in node_tree1.nodes:
        if node.type == "OUTPUT_MATERIAL":
            output_node1 = node
            break

    # If no Material Output node exists create one
    if not output_node1:
        output_node1 = node_tree1.nodes.new(type="ShaderNodeOutputMaterial")
        output_node1.location = (200, 0)
    

    # Link the Diffuse BSDF to the Material Output's Surface input
    node_tree1.links.new(diffuse_node1.outputs["BSDF"], output_node1.inputs["Surface"])



def mitsubaExport():
    path = "/home/piegian99/Digital_twin_thesis/mitsuba_export/"

    file_name = "test_scene.xml"
    file_path = os.path.join(path, file_name)   
    scene = bpy.context.scene    
    scene.render.engine = 'MITSUBA'
    bpy.ops.export_scene.mitsuba(filepath=file_path,export_ids=True,axis_forward='Y')

    print(f"Export completed: {file_path}")




#  COORDINATES OF THE CITY OF POVO (TRENTO) 
max_lat=46.07135
min_lat=46.05938
max_lon=11.16365
min_lon=11.14743


#FUNCTION FOR IMPORTING THE MAP BY USING BLOSM ADD-ON:
# we can set the cordinates by changing the input of this function 
importOsmData(min_lat,max_lat,min_lon,max_lon)


#LIST OF MATERIALS SUPPORTED BY SIONNA:
#  - concrete is the default material assigned to the terrain plane and to the "unknown" materials
#  - brick is assigned to the roof of the buildings
#  - plasterboard is assigned the walls of the buildings
material_1= "itu_concrete"
material_2="itu_brick"
material_3="itu_plasterboard"

#FUNCTION TO CREATE IN BLENDER THE MATERIALS IN THE ITU CONVENTION SUPPORTED BY SIONNA FOR THE EXPORT 
createMaterials(material_1,material_2,material_3)

#FUNCTION CALLED TO SET THE DIMENSION OF THE TERRAIN PLANE BASED ON THE FARTHEST COORDINATE
# +5 is used to give a small margin and the *2 to adjust the dimension 
dimension=(findPlaneDimension()+5)*2

#FUNCTION TO CREATE THE TERRAIN PLANE IN BLENDER OF THE RIGHT DIMENSION AND TO ASSIGN THE CONCRETE MATERIAL TO IT
createPlane(dimension)

#FUNCTION TO ASSIGN THE ITU CONVENTION MATERIALS TO ALL THE OBJECT IN THE SCENE (except the plane)
assignMaterials(material_1,material_2,material_3)

#INCREASE THE LIGHTINING TO RENDER IT CORRECTLY
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.9, 0.9, 0.9, 1)
bpy.context.scene.world.color = (1, 1, 1)

#FUNCTION TO EXPORT THE SCENE BY USING MITSUBA ADD-ON IN .xml FORMAT TO USE IN SIONNA
mitsubaExport()


