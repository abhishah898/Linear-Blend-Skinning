# Author: DA LAO Group 3
# pygame tutorial and help taken from https://livebook.manning.com/book/math-for-programmers/a-loading-and-rendering-3d-models-with-opengl-and-pygame/v-9/


import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import matplotlib.cm
from math import *
from numpy import dot
import numpy as np
from vectors import *

import csv
import numpy as np



weightMap = [0, 1, 2, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 4, 5, 6]

def normal(face):
    return(np.cross(np.subtract(face[1], face[0]), np.subtract(face[2], face[0])))
 
blues = matplotlib.cm.get_cmap('Blues')
 
def shade(face,color_map=blues,light=(1,2,3)):
    return color_map(1 - dot(normal(face)/np.linalg.norm(normal(face)), light)/np.linalg.norm(light))

def updatefaces(vertices, polygons, weights, posemat, frameid):
    nvArr = []

    for i in range(len(vertices)):
        v = np.array(vertices[i])
        v = np.append(v, 1)
        M = np.zeros([4, 4])
        wt = 0
        for j in range(len(weights[i])):
            wt += weights[i][j]
        for j in range(len(weights[i])):
            if(weights[i][j]!= 0):
                M = M + (np.array(posemat[frameid][weightMap[j]]) * weights[i][j]/wt)
        nv = np.transpose(M @ np.transpose(v))
        nvArr.append([nv[0]/nv[3], nv[1]/nv[3], nv[2]/nv[3]])

    faces = []

    for polygon in polygons:
        face = []
        for vert in polygon:
            face.append(nvArr[vert])
        faces.append(face)

    return faces



light = (1,2,3)

NUM_BONES = 17
#End Helper Functions


#load vertices
with open('vertices.csv', newline='') as f:
    reader = csv.reader(f)
    vertices = list(reader)

for i in range(len(vertices)):
    for j in range(len(vertices[0])):
        vertices[i][j] = float(vertices[i][j])


#load polygons
with open('polygons.csv', newline='') as f:
    reader = csv.reader(f)
    polygons = list(reader)

for i in range(len(polygons)):
    for j in range(len(polygons[0])):
        polygons[i][j] = int(polygons[i][j])


#load weights
with open('weights.csv', newline='') as f:
    reader = csv.reader(f)
    tempWeights = list(reader)

for i in range(len(tempWeights)):
    for j in range(len(tempWeights[0])):
        tempWeights[i][j] = float(tempWeights[i][j])

weights = [[0 for i in range(NUM_BONES)] for j in range(len(vertices))]

for item in tempWeights:
    weights[int(item[0])][int(item[1])] = item[2]


#Load pose mat
posemat = np.load('posemat.npy')

#Create faces from polygons
faces = []

for polygon in polygons:
    face = []
    for vert in polygon:
        face.append(vertices[vert])
    faces.append(face)


pygame.init()
display = (800,800)
window = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)


#Camera (Perspective) parameters
gluPerspective(60, 1, 0.1, 1500.0) #First: FOV. Last: Draw Distance
glTranslatef(0, 0.0, -600) #Camera Position
glEnable(GL_CULL_FACE)
glEnable(GL_DEPTH_TEST)
glCullFace(GL_BACK)


#To rotate the camera around object. Optional
degrees_per_second = 0
degrees_per_milisecond = degrees_per_second / 1000.

glRotatef(40, 0,1,0)



clock = pygame.time.Clock()
for i in range(len(posemat)):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
 
    clock.tick()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for face in faces:
        color = shade(face,blues,light)
        for vertex in face:
            glColor3fv((color[0], color[1], color[2]))
            glVertex3fv(vertex)
    glEnd()
    pygame.display.flip()
    milliseconds = clock.tick()
    #glRotatef(milliseconds * degrees_per_milisecond, 0,1,0) To rotate around object

    print("Frame: " + str(i))

    faces = updatefaces(vertices, polygons, weights, posemat, i)