import bpy
import math
from bpy.props import EnumProperty, PointerProperty
from mathutils import Matrix
from bpy.app.handlers import persistent

bl_info = {
    "name": "Sticky Key",
    "description": "Keyframe temporary parent/child transformations",
    "author": "Pekka Heikkinen",
    "version": (1, 1),
    "location": "VIEW_3D > Tools > Animation",
    "category": "Animation"
}

###################
# Stickykey props #
###################

class StickyKeyProperties(bpy.types.PropertyGroup):
    tween = EnumProperty(items=[
        ("linearTween", "Linear", "", 1),
        ("easeInOutQuad", "Quad", "", 2),
        ("easeInOutCubic", "Cubic", "", 3),
        ("easeInOutQuart", "Quart", "", 4),
        ("easeInOutQuint", "Quint", "", 5),
        ("easeInOutSine", "Sine", "", 6),
        ("easeInOutExpo", "Expo", "", 7),
        ("easeInOutCirc", "Circ", "", 8),
        ], name="Tween")
    tween_dir = EnumProperty(items=[
        ("InOut", "In/Out", "", 1),
        ("In", "In", "", 2),
        ("Out", "Out", "", 3),
        ], name="Dir")
    
bpy.utils.register_class(StickyKeyProperties)
bpy.types.Scene.stickykey = PointerProperty(type=StickyKeyProperties)

############################################
# Ease functions                           #
# ported from http://www.gizma.com/easing/ #
# by http://th0ma5w.github.io              #
############################################

linearTween = lambda t, b, c, d : c*t/d + b

def easeInQuad(t, b, c, d):
    t /= d
    return c*t*t + b

def easeOutQuad(t, b, c, d):
    t /= d
    return -c * t*(t-2) + b

def easeInOutQuad(t, b, c, d):
    t /= d/2
    if t < 1:
        return c/2*t*t + b
    t-=1
    return -c/2 * (t*(t-2) - 1) + b

def easeInOutCubic(t, b, c, d):
    t /= d/2
    if t < 1:
        return c/2*t*t*t + b
    t -= 2
    return c/2*(t*t*t + 2) + b

def easeInQuart(t, b, c, d):
    t /= d
    return c*t*t*t*t + b

def easeOutQuart(t, b, c, d):
    t /= d
    t -= 1
    return -c * (t*t*t*t - 1) + b

def easeInOutQuart(t, b, c, d):
    t /= d/2
    if t < 1:
        return c/2*t*t*t*t + b
    t -= 2
    return -c/2 * (t*t*t*t - 2) + b

def easeInQuint(t, b, c, d):
    t /= d
    return c*t*t*t*t*t + b

def easeOutQuint(t, b, c, d):
    t /= d
    t -= 1
    return c*(t*t*t*t*t + 1) + b

def easeInOutQuint(t, b, c, d):
    t /= d/2
    if t < 1:
        return c/2*t*t*t*t*t + b
    t -= 2
    return c/2*(t*t*t*t*t + 2) + b

def easeInSine(t, b, c, d):
    return -c * math.cos(t/d * (math.pi/2)) + c + b

def easeOutSine(t, b, c, d):
    return c * math.sin(t/d * (math.pi/2)) + b

def easeInOutSine(t, b, c, d):
    return -c/2 * (math.cos(math.pi*t/d) - 1) + b

def easeInExpo(t, b, c, d):
    return c * math.pow( 2, 10 * (t/d - 1) ) + b

def easeOutExpo(t, b, c, d):
    return c * ( -math.pow( 2, -10 * t/d ) + 1 ) + b

def easeInOutExpo(t, b, c, d):
    t /= d/2
    if t < 1: 
        return c/2 * math.pow( 2, 10 * (t - 1) ) + b
    t -= 1
    return c/2 * ( -math.pow( 2, -10 * t) + 2 ) + b

def easeInCirc(t, b, c, d):
    t /= d
    return -c * (math.sqrt(1 - t*t) - 1) + b

def easeOutCirc(t, b, c, d):
    t /= d;
    t -= 1
    return c * math.sqrt(1 - t*t) + b

def easeInOutCirc(t, b, c, d):
    t /= d/2
    if t < 1:
        return -c/2 * (math.sqrt(1 - t*t) - 1) + b
    t -= 2
    return c/2 * (math.sqrt(1 - t*t) + 1) + b

#######################
# Stickykey functions #
#######################
    
def get_matrix(context):
    if context.mode == "OBJECT":
        return context.active_object.matrix_world
    elif context.mode == "POSE":
        return context.active_object.matrix_world * context.active_pose_bone.matrix

def getFollowers(context):
    followers = []
    active_object = None
    if context.mode == "OBJECT":
        followers = [obj for obj in context.selected_objects if obj != context.active_object]
        active_object = context.active_object
    elif context.mode == "POSE":
        followers = [obj for obj in context.selected_pose_bones if obj != context.active_pose_bone]
        active_object = context.active_pose_bone
    return followers, active_object

def getRelativeTransforms(context, time):
    cur = context.scene.frame_current
    context.scene.frame_set(time)
    context.scene.update()
    followers, active_object = getFollowers(context)
    dict = {}
    for obj in followers:
        if context.mode == "OBJECT":
            dict[obj] = active_object.matrix_world.inverted() * obj.matrix_world
        elif context.mode == "POSE":
            dict[obj] = active_object.matrix.inverted() * obj.matrix
    return dict

def setKeyframeForFollowers(context):
    followers, active_object = getFollowers(context)
    override = {}
    if context.mode == "OBJECT":
        override = {'selected_objects': followers, 'active_object':followers[0]}
    elif context.mode == "POSE":
        override = {'selected_pose_bones': followers, 'active_pose_bone':followers[0]}
    bpy.ops.anim.keyframe_insert(override)

#######################
# Stickykey operators #
#######################

class SetAsMaster(bpy.types.Operator):
    bl_idname = "stickykey.setasmaster"
    bl_label = "Set Selected As Master"
    
    master = None
    bone = None
    
    def get_matrix_world():
        if SetAsMaster.master is not None:
            if SetAsMaster.bone is not None:
                return SetAsMaster.master.matrix_world * SetAsMaster.bone.matrix
            else:
                return SetAsMaster.master.matrix_world
        else:
            return Matrix.Translation((0.0, 0.0, 0.0))
    
    def get_local_matrix(context):
        m = get_matrix(context)
        l = SetAsMaster.get_matrix_world()
        return l.inverted() * m
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None)
    
    def execute(self, context):
        self.__class__.master = context.active_object
        if context.mode == "POSE":
            self.__class__.bone = context.active_pose_bone
        else:
            self.__class__.bone = None
        return {'FINISHED'}


class LockTransform(bpy.types.Operator):
    bl_idname = "stickykey.setstart"
    bl_label = "Lock Sticky Transform"
    
    matrix = None
    original = None
    
    @classmethod
    def release(cls, context):
        cls.matrix = None
        if cls.original is not None:
            context.scene.frame_start = cls.original
            cls.original = None
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None and SetAsMaster.master != None)
    
    def execute(self, context):
        self.__class__.matrix = SetAsMaster.get_local_matrix(context)
        if self.__class__.original is None:
            self.__class__.original = context.scene.frame_start
        context.scene.frame_start = context.scene.frame_current
        return {'FINISHED'}

        
class LockTransformEnd(bpy.types.Operator):
    bl_idname = "stickykey.setend"
    bl_label = "Lock Sticky Transform End"
    
    matrix = None
    original = None
    
    @classmethod
    def release(cls, context):
        cls.matrix = None
        if cls.original is not None:
            context.scene.frame_end = cls.original
            cls.original = None
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None and SetAsMaster.master != None and LockTransform.matrix != None and context.scene.frame_current > context.scene.frame_start)
    
    def execute(self, context):
        self.__class__.matrix = SetAsMaster.get_local_matrix(context)
        if self.__class__.original is None:
            self.__class__.original = context.scene.frame_end
        context.scene.frame_end = context.scene.frame_current
        return {'FINISHED'}

        
class UnlockTransform(bpy.types.Operator):
    bl_idname = "stickykey.release"
    bl_label = "Unlock Sticky Transform"
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None and SetAsMaster.master != None)
    
    def execute(self, context):
        LockTransform.release(context)
        LockTransformEnd.release(context)
        return {'FINISHED'}

        
class MoveToTransform(bpy.types.Operator):
    bl_idname = "stickykey.movetotransform"
    bl_label = "Move To Sticky Transform"
    
    tweentype = bpy.props.BoolProperty(name="wut")
    
    @classmethod
    def poll(cls, context):
        return LockTransform.matrix is not None
    
    def execute(self, context):
        mw = SetAsMaster.get_matrix_world()
        numat = mw * LockTransform.matrix
        scene = context.scene
        progress = (scene.frame_current - scene.frame_start) / (scene.frame_end-scene.frame_start)
        tw = scene.stickykey.tween.replace("InOut", scene.stickykey.tween_dir)
        progress = globals()[tw](progress, 0.0, 1.0, 1.0)
        
        if LockTransformEnd.matrix is not None:
            endmat = mw * LockTransformEnd.matrix
            numat = numat.lerp(endmat, progress)
            
        if context.mode == 'OBJECT':
            context.active_object.matrix_world = numat
        if context.mode == 'POSE':
            context.active_pose_bone.matrix = context.active_object.matrix_world.inverted() * numat
        return {'FINISHED'}


class TweenAnimationRange(bpy.types.Operator):
    bl_idname = "stickykey.tweenrange"
    bl_label = "Tween Range"
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None and SetAsMaster.master != None and LockTransform.matrix is not None and context.scene.frame_end > context.scene.frame_start)
    
    def execute(self, context):
        bpy.ops.anim.keying_set_active_set(type='LocRotScale')
        for fr in range(context.scene.frame_start, context.scene.frame_end+1):
            context.scene.frame_set(fr)
            bpy.ops.anim.keyframe_insert()
        bpy.ops.stickykey.release()
        return {'FINISHED'}

        
class StickyKeyPanel(bpy.types.Panel):
    bl_label = "StickyKey"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Animation"
    
    @classmethod
    def poll(cls, context):
        if context.mode == "OBJECT":
            return len(context.selected_objects) > 0
        elif context.mode == "POSE":
            return len(context.selected_pose_bones) > 0
        return false

    def draw(self, context):
        global params
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.operator(SetAsMaster.bl_idname)
        row = layout.row(align=True)
        row.operator(LockTransform.bl_idname, text="Set Start")
        row.operator(LockTransformEnd.bl_idname, text="Set End")
        row.operator(UnlockTransform.bl_idname, text="Release")
        row = layout.row()
        row.prop(scene.stickykey, "tween", text="")
        if scene.stickykey.tween != "linearTween":
            row.prop(scene.stickykey, "tween_dir", text="")
        row.operator(TweenAnimationRange.bl_idname)

######################
# Stickykey handlers #
######################

@persistent
def update_transforms(scene):
    if LockTransform.matrix is not None:
        bpy.ops.stickykey.movetotransform()


##########################
# Stickykey registration #
##########################
        
def register():
    bpy.utils.register_module(__name__)
    bpy.app.handlers.frame_change_post.append(update_transforms)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.app.handlers.frame_change_post.remove(update_transforms)

#######################
# Stickykey debugging #
#######################
    
if __name__ == "__main__":
    register()
