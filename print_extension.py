import bpy

bl_info = {
    "name": "Print to text datablock",
    "description": "Replaces the standard print() statement to redirect messages to a text datablock.",
    "author": "Pekka Heikkinen",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "In your script add 'from print_extension import print'",
    "category": "Development"}

___print = print
def print(str, clear=False, log_name='_LOG_', log_format="{0}\n"):
    if log_name not in bpy.data.texts:
        bpy.data.texts.new(log_name)
    log_target = bpy.data.texts[log_name]
    if clear:
        log_target.clear()
    out = log_format.format(str)
    log_target.write(out)
    ___print(out)

def register():
    pass
    
def unregister():
    pass
