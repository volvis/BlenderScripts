"""
Toggles the skeleton layers in Rigify rigs between
a) Displaying the deformer bones for skinning
b) Displaying the controller objects for posing
"""

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

class VSkinningPanel(bpy.types.Panel):
    bl_label = "Skinning"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = 'objectmode'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("aijai.toggle_deforming_bones")


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
