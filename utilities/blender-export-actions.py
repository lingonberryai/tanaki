import bpy
import os
import getpass

# get the current file name without extension
filename = bpy.path.basename(bpy.context.blend_data.filepath)
base_filename = os.path.splitext(filename)[0]

# Get the current object
current_obj = bpy.context.object

# Get the username and construct the path to the desktop
username = getpass.getuser()
desktop_dir = os.path.join("/Users", username, "Desktop")

# Specify the name of the new folder
folder_name = "action-render"

# Join the desktop directory with the new folder name
output_dir = os.path.join(desktop_dir, folder_name)

# Create the folder if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Iterate over all the actions
for action in bpy.data.actions:
    # Construct the new filename with action
    new_filename = f"{base_filename}-{action.name}.blend"

    # set the action as the only active track
    current_obj.animation_data.action = action

    # create a new NLA track and a strip for the action
    track = current_obj.animation_data.nla_tracks.new()
    strip = track.strips.new(action.name, int(action.frame_range[0]), action)

    # write it out to a .blend file
    bpy.ops.wm.save_as_mainfile(
        filepath=os.path.join(output_dir, new_filename))

    # remove the created NLA track to prevent pollution of the NLA tracks
    current_obj.animation_data.nla_tracks.remove(track)

print("All actions exported")
