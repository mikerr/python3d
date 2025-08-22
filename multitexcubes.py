import pygame, random
from pygame.locals import *

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

class shapeobj:
    x = y = z = 0
    dx = dy = dz = 0
    angle = spin = 0
    
def drawCube():
    glBegin(GL_QUADS)
    f2old = 0
    for i in range(len(faces)):
         r,g,b = facecolors[i]
         face = faces[i]
         
         f1,f2,f3 = face
         if (i % 2) :
             glTexCoord2f(0.0, 1.0)
             glVertex3fv(verticies[f2])
             glTexCoord2f(1.0, 1.0)
             glVertex3fv(verticies[f2old])
             glTexCoord2f(1.0, 0.0)
             glVertex3fv(verticies[f1])
             glTexCoord2f(0.0, 0.0)
             glVertex3fv(verticies[f3])
         f2old = f2
    glEnd()

def loadTexture():
    textureSurface = pygame.image.load('crate.bmp')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texid

def init():
    global cubes
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glMatrixMode(GL_PROJECTION) # operate on projection (world)
    glLoadIdentity()           
    
    gluPerspective(50.0, display[0]/display[1], 0.1, 70.0)
   
    glEnable(GL_CULL_FACE)  # doesn't need normals if winding order is correct 
    glEnable(GL_DEPTH_TEST)

    cubes = []
    for i in range(15) :
            c = shapeobj()
            c.x = random.uniform(-5,5)
            c.y = random.uniform(-5,5)
            c.z = random.uniform(-50,-6)
            c.spin = random.uniform(-1.0,1.0)
            
            c.dx = random.uniform(-0.01,0.01)
            c.dy = random.uniform(-0.01,0.01)
            c.dz = random.uniform(-0.1,0.1)
            cubes.append(c)
    loadTexture()
    
def render():
        global cubes
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW) # operate on model
 
        
        for c in cubes :  
            glLoadIdentity()
            glTranslatef(c.x, c.y, c.z)
            glRotatef(c.angle, 1.0, 1.0, 0.0)
            drawCube()
        
        pygame.display.flip()
        
def game():
    global cubes
    for c in cubes:
            c.angle += c.spin
            c.x += c.dx
            if abs(c.x / c.z) > 1 : c.dx *= -1
            c.y += c.dy
            if abs(c.y / c.z) > 1 : c.dy *= -1
            c.z += c.dz
            if c.z < -70 or c.z > 0 : c.dz *= -1

init()
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    game()
    render()
