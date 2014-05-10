"""
Adds every DEFORMING bone as a vertex group
"""

import bpy

for mesh in bpy.context.selected_objects:
    bpy.data.objects[mesh.name].vertex_groups.clear()
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            for b in obj.pose.bones:
                if b.name.startswith("DEF"):
                    vg = bpy.data.objects[mesh.name].vertex_groups.new(b.name)
                    for f in bpy.data.objects[mesh.name].data.polygons:
                        vg.add(f.vertices, 0.0, 'ADD')
