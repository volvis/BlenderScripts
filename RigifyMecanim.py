import bpy
import math

rig_id = "Rigify-Mecanim"
rigify_instance = None

def get_mecanim_armature ():
    global rig_id
    armatures = [armature for armature in bpy.data.armatures if armature.get(rig_id) == True]
    if len(armatures) == 0: # No such armature data, create new
        bpy.ops.object.add(type='ARMATURE', location=(0,0,0))
        bpy.context.active_object.data[rig_id] = True
    else:
        if armatures[0].users == 0: # Armature data not linked to scene
            obj = bpy.data.objects.new(rig_id, armatures[0])
            bpy.context.scene.objects.link(obj)
            bpy.context.scene.objects.active = obj
        else: # In scene, find it
            for obj in bpy.context.scene.objects:
                if obj.type == 'ARMATURE' and obj.data.get(rig_id) == True:
                    bpy.context.scene.objects.active = obj
                    return

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
        b.parent = bpy.context.active_object.data.edit_bones[bone_parent]
    con = bpy.context.object.pose.bones[bone_name].constraints.new('COPY_TRANSFORMS')
    con.target = get_rigify_armature()
    con.subtarget = bone_head["name"]

if bpy.context.mode != 'OBJECT':
    bpy.ops.object.editmode_toggle()

bpy.context.scene.objects.active = get_rigify_armature()
bpy.ops.object.editmode_toggle()

original = {}
for bone in bpy.context.active_object.data.edit_bones:
    original[bone.name] = {
        "name": bone.name,
        "head": bone.head,
        "tail": bone.tail,
        "roll": bone.roll
    }

bpy.ops.object.editmode_toggle()

get_mecanim_armature()

bpy.ops.object.editmode_toggle()
bpy.ops.armature.select_all(action='SELECT')
bpy.ops.armature.delete()

create_bone(mec("hips"), original["DEF-hips"], original["DEF-hips"])
create_bone(mec("spine"), original["DEF-spine"], original["DEF-spine"], mec("hips"))
create_bone(mec("chest"), original["DEF-chest"], original["DEF-chest"], mec("spine"))
create_bone(mec("neck"), original["DEF-neck"], original["DEF-neck"], mec("chest"))
create_bone(mec("head"), original["DEF-head"], original["DEF-head"], mec("neck"))

def create_finger(side, name, original_name):
    hand = mec("hand."+side)
    f1 = mec(name+".01."+side)
    f2 = mec(name+".02."+side)
    f3 = mec(name+".03."+side)
    create_bone(f1, original["DEF-"+original_name+".01."+side+".01"], original["DEF-"+original_name+".01."+side+".02"], hand)
    create_bone(f2, original["DEF-"+original_name+".02."+side], original["DEF-"+original_name+".02."+side], f1)
    create_bone(f3, original["DEF-"+original_name+".03."+side], original["DEF-"+original_name+".03."+side], f2)

def create_arm(side="L"):
    shoulder = mec("shoulder."+side)
    upperarm = mec("upper_arm."+side)
    forearm = mec("forearm."+side)
    hand = mec("hand."+side)
    
    create_bone(shoulder, original["DEF-shoulder."+side], original["DEF-shoulder."+side], mec("chest"))
    create_bone(upperarm, original["DEF-upper_arm.01."+side], original["DEF-upper_arm.02."+side], shoulder)
    create_bone(forearm, original["DEF-forearm.01."+side], original["DEF-forearm.02."+side], upperarm)
    create_bone(hand, original["DEF-hand."+side], original["DEF-hand."+side], forearm)
    
    create_finger(side, "thumb", "thumb")
    create_finger(side, "index", "f_index")
    create_finger(side, "middle", "f_middle")
    create_finger(side, "ring", "f_ring")
    create_finger(side, "pinky", "f_pinky")

def create_leg(side="L"):
    thigh = mec("thigh."+side)
    shin = mec("shin."+side)
    foot = mec("foot."+side)
    toe = mec("toe."+side)
    create_bone(thigh, original["DEF-thigh.01."+side], original["DEF-thigh.02."+side], mec("hips"))
    create_bone(shin, original["DEF-shin.01."+side], original["DEF-shin.02."+side], thigh)
    create_bone(foot, original["DEF-foot."+side], original["DEF-foot."+side], shin)
    create_bone(toe, original["DEF-toe."+side], original["DEF-toe."+side], foot)


create_leg("L")
create_leg("R")

create_arm("L")
create_arm("R")
