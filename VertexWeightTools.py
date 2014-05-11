"""
Tool shortcuts for applying weights to vertices similar to 3dsMax.
Select bone, vertices and click the desired value
"""

import bpy


class VToggleRigifyDeformingBones(bpy.types.Operator):
    bl_idname = "aijai.toggle_deforming_bones"
    bl_label = "Toggle Deforming Bones (Rigify)"
    
    def execute(self, context):
        control_layers = [0,2,4,6,12,15,24]
        for armature in bpy.data.armatures:
            if 'rig_id' in armature:
                controls = armature.layers[29]
                for layer in control_layers:
                    armature.layers[layer] = controls
                armature.layers[29] = not controls 
        return {'FINISHED'}


def aijai_set_weight(weight = 1.0):
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
    bl_idname = "aijai.set_vertex_weight"
    bl_label = "Set Vertex Weight"
    bl_options = {'REGISTER', 'UNDO'}
    
    weight = bpy.props.FloatProperty(name="Vertex Weight", default=1.0, min=0.0, max=1.0)
    
    def execute(self, context):
        aijai_set_weight(weight=self.weight)
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
        row.operator("aijai.set_vertex_weight", text="0.0").weight = 0.0
        row.operator("aijai.set_vertex_weight", text="0.5").weight = 0.5
        row.operator("aijai.set_vertex_weight", text="1.0").weight = 1.0
        
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.operator("aijai.set_vertex_weight", text="0.25").weight = 0.25
        row.operator("aijai.set_vertex_weight", text="0.75").weight = 0.75
        
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.operator("aijai.set_vertex_weight", text="0.33").weight = 0.33333
        row.operator("aijai.set_vertex_weight", text="0.66").weight = 0.66666
        
        row = layout.row()
        row.operator("aijai.toggle_deforming_bones")
        
        row = layout.row()
        row.operator("aijai.context.object.data.use_paint_mask")
        
        row = layout.row()
        row.prop(bpy.context.object.data, "use_paint_mask_vertex")
        row.prop(bpy.context.object.data, "use_paint_mask")
        
        row = layout.row()
        row.operator("aijai.set_vertex_weight", "Type Vertex Weight")


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()

