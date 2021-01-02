import bpy
import csv

obj = bpy.context.active_object  #Select Object or use  obj = bpy.data.objects['Armature']

#Active Object is the one on which you have clicked. Make sure to click on mesh before exporting faces, vertices, etc
#bpy.ops.mesh.quads_convert_to_tris(quad_method='FIXED', ngon_method='BEAUTY')   Optional. To triangulate Faces. Go to edit mode and seleect all on the mesh first.



faces = []
for face in obj.data.polygons:  
    verts_in_face = face.vertices[:]
    if(len(verts_in_face)!=3):
        print("Please Triangulate the Mesh.")
        quit()
    faces.append(verts_in_face)

print(len(faces))

with open('faces.txt', 'w') as f:       
    write = csv.writer(f)      
    write.writerows(faces) 

obdata = obj.data

verts = [(obj.matrix_world @ v.co) for v in obj.data.vertices]

""" Commented)
vertices = [[0 for i in range(3)] for j in range(len(obdata.vertices))]
for v in obj.data.vertices:
    vertices[v.index][0] = v.x
    vertices[v.index][1] = v.y
    vertices[v.index][2] = v.z
"""

with open('vertices.txt', 'w') as f:       
    write = csv.writer(f)      
    write.writerows(verts)


#Export animation using (.bvh) File > Export > Motion Capture

arm = bpy.data.objects['Armature']
obj = bpy.context.active_object
obj_verts = obj.data.vertices
obj_group_names = [g.name for g in obj.vertex_groups]
vertexWeights = [[0 for i in range(len(arm.pose.bones))] for j in range(len(obj.data.vertices))]

for bone in arm.pose.bones:
    if bone.name not in obj_group_names:
        continue
        print("Skipped a Bone")
    gidx = obj.vertex_groups[bone.name].index
    bone_verts = [v for v in obj_verts if gidx in [g.group for g in v.groups]]
    for v in bone_verts:
        for g in v.groups:
            if g.group == gidx: 
                w = g.weight
                vertexWeights[v.index][gidx] = w


wo = []

for i in range(len(vertexWeights)):
    for j in range(len(vertexWeights[0])):
        if(vertexWeights[i][j]!=0):
            wo.append([i, j, vertexWeights[i][j]])


with open('weights.txt', 'w') as f:       
    write = csv.writer(f)      
    write.writerows(wo)




