import bpy

def set_weight(weight = 1.0):
    pose_bone = bpy.context.active_pose_bone
    wp_object = bpy.context.weight_paint_object

    if pose_bone is not None and wp_object is not None:
        if pose_bone.name not in wp_object.vertex_groups:
            wp_object.vertex_groups.new(pose_bone.name)
        vg = wp_object.vertex_groups[pose_bone.name]
        selected_verts = []
        for vert in wp_object.data.vertices:
            if vert.select is True:
                selected_verts.append(vert.index)
        if weight <= 0:
            vg.remove(selected_verts)
        else:
            vg.add(selected_verts, weight, 'REPLACE')

    bpy.ops.paint.weight_paint_toggle()
    bpy.ops.paint.weight_paint_toggle()

set_weight(0)
