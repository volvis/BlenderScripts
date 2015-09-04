import bpy
from mathutils import Matrix

stored_transform = None

def get_matrix(context):
    if context.mode == "OBJECT":
        return context.active_object.matrix_world
    elif context.mode == "POSE":
        return context.active_object.matrix_world * context.active_pose_bone.matrix
    
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

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

#######################
# Stickykey debugging #
#######################
    
if __name__ == "__main__":
    register()
