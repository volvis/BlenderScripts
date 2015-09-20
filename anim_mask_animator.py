import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "Mask Animator",
    "description": "Makes the Mask modifier animatable",
    "author": "Pekka Heikkinen",
    "version": (1, 1),
    "location": "VIEW_3D > Tools > Animation",
    "category": "Animation"
}


##########################
# Mask Animator handlers #
##########################

@persistent
def update_masks(scene):
    sceneDirty = False
    if 'Animated Masks' in bpy.data.groups:
        for object in bpy.data.groups['Animated Masks'].objects:
            if 'MaskIndex' in object and 'Mask' in object.modifiers:
                if object.MaskIndex < len(object.vertex_groups):
                    object.modifiers["Mask"].vertex_group =  object.vertex_groups[object.MaskIndex].name
                    sceneDirty = True
    if sceneDirty:
        scene.update()


def on_update_masks(self, context):
    update_masks(context.scene)


bpy.types.Object.MaskIndex = bpy.props.IntProperty(name = "Mask Index", min=0, update=on_update_masks)


###########################
# Mask Animator Operators #
###########################

class SetMaskAnimation(bpy.types.Operator):
    bl_idname = "maskanimation.setasanimated"
    bl_label = "Set Mask Animation For Selected"
    
    @classmethod
    def poll(cls, context):
        if context.active_object != None:
            if 'Animated Masks' not in bpy.data.groups:
                return True
            else:
                return bpy.data.groups['Animated Masks'] not in context.active_object.users_group
        return False
    
    def execute(self, context):
        if 'Animated Masks' not in bpy.data.groups:
            bpy.ops.group.create(name='Animated Masks')
        bpy.ops.object.group_link(group='Animated Masks')
        if 'MaskIndex' not in context.active_object:
            context.active_object["MaskIndex"] = 0
        if 'Mask' not in context.active_object.modifiers:
            context.active_object.modifiers.new("Mask", type='MASK')
        return {'FINISHED'}


####################
# Mask Animator UI #
####################

class MaskAnimatorPanel(bpy.types.Panel):
    bl_label = "Mask Animator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Animation"
    
    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.operator(SetMaskAnimation.bl_idname)


##############################
# Mask Animator registration #
##############################

def register():
    bpy.utils.register_module(__name__)
    bpy.app.handlers.frame_change_post.append(update_masks)
    bpy.app.handlers.render_pre.append(update_masks)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.app.handlers.frame_change_post.remove(update_masks)
    bpy.app.handlers.render_pre.remove(update_masks)


########################
# Mask Animator Debug #
#######################

if __name__ == "__main__":
    bpy.app.handlers.frame_change_post.clear()
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.render_pre.clear()
    register()
