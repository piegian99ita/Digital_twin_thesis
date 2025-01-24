import bpy

# Get the current scene
current_scene = bpy.context.scene

# Check if the current scene exists
if current_scene is not None:
    # Get the name of the scene
    scene_name = current_scene.name
    
    # Ensure there are multiple scenes (Blender needs at least one scene)
    if len(bpy.data.scenes) > 1:
        # Delete the current scene
        bpy.data.scenes.remove(current_scene)
        print(f"Scene '{scene_name}' deleted.")
    else:
        print("Cannot delete the only scene. Add another scene first.")
else:
    print("No active scene to delete.")
