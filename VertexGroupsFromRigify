import bpy

for mesh in bpy.context.selected_objects:
    for obj in bpy.context.scene.objects:
        deformers = []
        index = 0
        if obj.type == 'ARMATURE':
            for b in obj.pose.bones:
                if b.name.startswith("DEF"):
                    bpy.data.objects[mesh.name].vertex_groups.new(b.name)
