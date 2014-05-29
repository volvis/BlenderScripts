import bpy

rig_id = "Rigify-Mecanim"

def get_mecanim_armature ():
    global rig_id
    armatures = [armature for armature in bpy.data.armatures if armature.get(rig_id) == True]
    if len(armatures) == 0: # No such armature data, create new
        bpy.ops.object.add(type='ARMATURE', location=(1.0,1.0,0.0))
        bpy.context.active_object.data[rig_id] = True
    else:
        if armatures[0].users == 0: # Armature data not linked to scene
            obj = bpy.data.objects.new(rig_id, armatures[0])
            bpy.context.scene.objects.link(obj)
            bpy.context.scene.objects.active = obj
        else:
            for obj in bpy.context.scene.objects:
                if obj.type == 'ARMATURE' and obj.data.get(rig_id) == True:
                    bpy.context.scene.objects.active = obj
                

get_mecanim_armature()
print(bpy.context.scene.objects.active)