"""
Tool shortcuts for applying weights to vertices similar to 3dsMax.
Select bone, vertex and 
"""

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


class VSetVertexWeight(bpy.types.Operator):
    bl_idname = "ops.set_vertex_weight"
    bl_label = "Set Vertex Weight"
    
    weight = bpy.props.FloatProperty(name="Weight", default=1.0, min=0.0, max=1.0)
    
    def execute(self, context):
        set_weight(weight=self.weight)
        return {'FINISHED'}


class VSetVertexWeightPanel(bpy.types.Panel):
    bl_label = "Vertex Weight"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "weightpaint"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.operator("ops.set_vertex_weight", text="0.0").weight = 0.0
        row.operator("ops.set_vertex_weight", text="0.5").weight = 0.5
        row.operator("ops.set_vertex_weight", text="1.0").weight = 1.0
        
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.operator("ops.set_vertex_weight", text="0.25").weight = 0.25
        row.operator("ops.set_vertex_weight", text="0.75").weight = 0.75
        
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.operator("ops.set_vertex_weight", text="0.33").weight = 0.33333
        row.operator("ops.set_vertex_weight", text="0.66").weight = 0.66666
        
        row = layout.row()
        row.operator("ops.toggle_deforming_bones")
        
        row = layout.row()
        row.operator("bpy.context.object.data.use_paint_mask")
        
        row = layout.row()
        row.prop(bpy.context.object.data, "use_paint_mask_vertex"
        row.prop(bpy.context.object.data, "use_paint_mask")

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
