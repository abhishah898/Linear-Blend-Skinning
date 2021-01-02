import bpy

obj = bpy.data.objects['animation']


#Get Bone Names
for action in bpy.data.actions:
    bpy.context.object.animation_data.action = action
    for frame in range(2):
        print("Frame " + str(frame))
        bpy.context.scene.frame_set(frame)
        for bone in bpy.context.object.data.bones:
            poseBone = obj.pose.bones[bone.name]
            mat = poseBone.matrix
            print(bone.name)

#Conversion attempt from blender co-ordinated to OpenGL coordinates
global_matrix = axis_conversion(to_forward="-Z", to_up="Y").to_4x4()


#Save animation frame bind poses for skeleton
#Recursive bind pose calculation
def recursiveMatCalc(arm, bone_name):
    parent = arm.pose.bones[bone_name].parent
    localmat = arm.data.bones[bone_name].matrix_local
    basismat = arm.pose.bones[bone_name].matrix_basis
    if parent != None:
        parent_local = arm.data.bones[parent.name].matrix_local
        return recursiveMatCalc(arm, parent.name) @ (parent_local.inverted() @ localmat) @ basismat
    else:
        return  localmat @ basismat


poseMat = []
for action in bpy.data.actions:
    bpy.context.object.animation_data.action = action
    for frame in range(250):
        bpy.context.scene.frame_set(frame)
        bpy.context.view_layer.update()
        pm = []
        for bone in bpy.context.object.data.bones:
            bone = obj.pose.bones[bone.name]
            bone_matrix = global_matrix @ recursiveMatCalc(obj, bone.name) @ obj.data.bones[bone.name].matrix_local.inverted() @ global_matrix.inverted()
            pm.append(bone_matrix)
        poseMat.append(pm)
with open('posemat.npy', 'wb') as f:
    np.save(f, poseMat)