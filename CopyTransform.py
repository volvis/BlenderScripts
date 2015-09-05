import bpy
from mathutils import Matrix

stored_transform = None

class StoreTransform(bpy.types.Operator):
    bl_idname = "transform.storetransform"
    bl_label = "Store Transform From Active"
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)
    
    def get_matrix_world(self, context):
        ao = context.active_object
        if context.mode == 'POSE':
            return ao.matrix_world * context.active_pose_bone.matrix
        else:
            return ao.matrix_world
    
    def execute(self, context):
        global stored_transform
        stored_transform = self.get_matrix_world(context)
        return {'FINISHED'}
    

class RetrieveTransform(bpy.types.Operator):
    bl_idname = "transform.retrievetransform"
    bl_label = "Retrieve Transform For Active"
    
    @classmethod
    def poll(cls, context):
        global stored_transform
        return context.active_object != None and stored_transform != None
    
    def execute(self, context):
        global stored_transform
        ao = context.active_object
        if context.mode == 'POSE':
            context.active_pose_bone.matrix = context.active_object.matrix_world.inverted() * stored_transform
        else:
            ao.matrix_world = stored_transform
        return {'FINISHED'}

class RetrieveTransformToCursor(bpy.types.Operator):
    bl_idname = "transform.retrievetransformtocursor"
    bl_label = "Retrieve Transform For Cursor"
    
    @classmethod
    def poll(cls, context):
        global stored_transform
        return stored_transform != None
    
    def execute(self, context):
        global stored_transform
        bpy.context.scene.cursor_location = stored_transform.to_translation()
        return {'FINISHED'}

class TransformStorePanel(bpy.types.Panel):
    bl_label = "Transform Storage"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Animation'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.alignment='EXPAND'
        row.operator(StoreTransform.bl_idname, text="Store", icon='COPYDOWN')
        row.operator(RetrieveTransformToCursor.bl_idname, text="", icon='CURSOR')
        row.operator(RetrieveTransform.bl_idname, text="Retrieve", icon='PASTEDOWN')

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()
