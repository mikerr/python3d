import pygame
from pygame.locals import *
#pip3 install pyopenGL
from OpenGL.GL import *
from OpenGL.GLU import *

verticies = [
            [ 1,  1,  1],
             [-1,  1,  1],
             [-1, -1,  1],
             [ 1, -1,  1],
             [ 1,  1, -1],
             [-1,  1, -1],
             [-1, -1, -1],
             [ 1, -1, -1]]
        # cube faces
        # (triangles)
faces = [
            [0, 1, 2],
            [0, 2, 3],
            [4, 0, 3],
            [4, 3, 7],
            [5, 4, 7],
            [5, 7, 6],
            [1, 5, 6],
            [1, 6, 2],
            [4, 5, 1],
            [4, 1, 0],
            [2, 6, 7],
            [2, 7, 3]]
facecolors = [
            [15,0,0], # red
            [15,0,0],
            [0,15,0], # green
            [0,15,0],
            [0,0,15], # blue
            [0,0,15],
            [15,15,0], # yellow
            [15,15,0],
            [0,15,15], # cyan
            [0,15,15],
            [15,0,15], # magenta
            [15,0,15]
            ]
         
def Cube():
    glBegin(GL_TRIANGLES)
    i = 0
    for face in faces:
         r,g,b = facecolors[i]
         glColor3f(r,g,b)
         i += 1
         
         for vertex in face:
           glVertex3fv(verticies[vertex]) 
    glEnd()

def init():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(50, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)
    glEnable(GL_CULL_FACE);  # doesn't need normals if winding order is correct 

def render():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE); # wireframe
        Cube()
        pygame.display.flip()
        pygame.time.wait(4)
      
init()
render()
