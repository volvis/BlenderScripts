import bpy
import math

rig_id = "RigifyMecanim"
rigify_instance = None

def get_mecanim_armature ():
    global rig_id
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE' and obj.data.get(rig_id) == True:
            bpy.context.scene.objects.active = obj
            obj.select = True
            bpy.ops.object.delete()
    bpy.ops.object.add(type='ARMATURE', location=(0,0,0))
    bpy.context.active_object.data[rig_id] = True


def get_rigify_armature():
    global rigify_instance
    if rigify_instance != None:
        return rigify_instance
    else:
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE' and obj.data.get('rig_id') != None:
                rigify_instance = obj
                return rigify_instance

def mec(name):
    if name.startswith("MEC-"):
        return name
    else:
        return "MEC-" + name

def new_bone(obj, bone_name):
    if obj == bpy.context.active_object and bpy.context.mode == 'EDIT_ARMATURE':
        edit_bone = obj.data.edit_bones.new(bone_name)
        name = edit_bone.name
        edit_bone.head = (0, 0, 0)
        edit_bone.tail = (0, 1, 0)
        edit_bone.roll = 0
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        return name
    else:
        raise Error("Can't add new bone '%s' outside of edit mode" % bone_name)

def create_bone(bone_name, bone_head, bone_tail, bone_parent=None):
    new_bone(bpy.context.active_object, bone_name)
    b = bpy.context.active_object.data.edit_bones[bone_name]
    b.head = bone_head["head"]
    b.tail = bone_tail["tail"]
    b.roll = bone_head["roll"]
    if bone_parent != None:
        #bpy.context.object.data.use_connect = False
        b.parent = bpy.context.active_object.data.edit_bones[bone_parent]
    con = bpy.context.object.pose.bones[bone_name].constraints.new('COPY_TRANSFORMS')
    con.target = get_rigify_armature()
    con.subtarget = bone_head["name"]


def create_finger(side, name, original_name, original):
    hand = mec("hand."+side)
    f1 = mec(name+".01."+side)
    f2 = mec(name+".02."+side)
    f3 = mec(name+".03."+side)
    create_bone(f1, original["DEF-"+original_name+".01."+side+".01"], original["DEF-"+original_name+".01."+side+".02"], hand)
    create_bone(f2, original["DEF-"+original_name+".02."+side], original["DEF-"+original_name+".02."+side], f1)
    create_bone(f3, original["DEF-"+original_name+".03."+side], original["DEF-"+original_name+".03."+side], f2)

def create_arm(side, original):
    shoulder = mec("shoulder."+side)
    upperarm = mec("upper_arm."+side)
    forearm = mec("forearm."+side)
    hand = mec("hand."+side)
    
    create_bone(shoulder, original["DEF-shoulder."+side], original["DEF-shoulder."+side], mec("chest"))
    create_bone(upperarm, original["DEF-upper_arm.01."+side], original["DEF-upper_arm.02."+side], shoulder)
    create_bone(forearm, original["DEF-forearm.01."+side], original["DEF-forearm.02."+side], upperarm)
    create_bone(hand, original["DEF-hand."+side], original["DEF-hand."+side], forearm)
    
    create_finger(side, "thumb", "thumb", original)
    create_finger(side, "f_index", "f_index", original)
    create_finger(side, "f_middle", "f_middle", original)
    create_finger(side, "f_ring", "f_ring", original)
    create_finger(side, "f_pinky", "f_pinky", original)

def create_leg(side, original):
    thigh = mec("thigh."+side)
    shin = mec("shin."+side)
    foot = mec("foot."+side)
    toe = mec("toe."+side)
    create_bone(thigh, original["DEF-thigh.01."+side], original["DEF-thigh.02."+side], mec("hips"))
    create_bone(shin, original["DEF-shin.01."+side], original["DEF-shin.02."+side], thigh)
    create_bone(foot, original["DEF-foot."+side], original["DEF-foot."+side], shin)
    create_bone(toe, original["DEF-toe."+side], original["DEF-toe."+side], foot)

def create_mecanim():
    bpy.ops.object.select_all(action='DESELECT')
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = get_rigify_armature()
    bpy.ops.object.editmode_toggle()
    
    original = None
    original = {}
    for bone in bpy.context.active_object.data.edit_bones:
        original[bone.name] = { "name": bone.name, "head": bone.head, "tail": bone.tail, "roll": bone.roll}
        del bone

    bpy.ops.object.editmode_toggle()

    get_mecanim_armature()

    bpy.ops.object.editmode_toggle()
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.delete()

    create_bone(mec("hips"), original["DEF-hips"], original["DEF-hips"])
    create_bone(mec("spine"), original["DEF-spine"], original["DEF-spine"], mec("hips"))
    create_bone(mec("chest"), original["DEF-chest"], original["DEF-chest"], mec("spine"))
    

    create_leg("L", original)
    create_leg("R", original)

    create_arm("L", original)
    create_arm("R", original)
    
    create_bone(mec("neck"), original["DEF-neck"], original["DEF-neck"], mec("chest"))
    create_bone(mec("head"), original["DEF-head"], original["DEF-head"], mec("neck"))
    
    bpy.ops.object.editmode_toggle()
    del original


create_mecanim()