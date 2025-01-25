import bpy

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete the selected objects
bpy.ops.object.delete()

print("All objects in the scene have been deleted.")
