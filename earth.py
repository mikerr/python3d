# super simple 3d earth, texmapped sphere, no fragment shader

import pygame, math, time
from pygame.locals import *

from OpenGL.GL import *
#from OpenGL.GLU import *

def loadTexture():
    textureSurface = pygame.image.load('earth.jpg')
    textureData = pygame.image.tostring(textureSurface, "RGBA", True)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texid

def init():
    
    pygame.init()
    display = (900,900)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glMatrixMode(GL_PROJECTION) # operate on projection (world)
    glLoadIdentity()           
    
    #gluPerspective(40.0, display[0]/display[1], 0.1, 200.0)
    glOrtho(-25,25,-25,25,0,50.0)
    glTranslatef(0,0,-50)
    
    glFrontFace(GL_CCW)
    glEnable(GL_DEPTH_TEST)
 
    loadTexture()

def drawSphere(r,lats,longs): 

    for i in range(lats+1):
        lat0 = math.pi * (-0.5 + (i - 1) / lats)
        z0  = math.sin(lat0)
        zr0 = math.cos(lat0)

        lat1 = math.pi * (-0.5 + i / lats)
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)
        
        glBegin(GL_QUAD_STRIP);
        for j in range (longs+1): 
            lng = 2 * math.pi * (j - 1) / longs
            x = math.cos(lng)
            y = math.sin(lng)

            u = i / longs
            v = j / lats
            u1 = (i + 1) / longs
            
            #glNormal3f(x * zr0, y * zr0, z0)
            glTexCoord2f(v, u)
            glVertex3f(r * x * zr0, r * y * zr0, r * z0)
            
            #glNormal3f(x * zr1, y * zr1, z1)
            glTexCoord2f(v, u1)
            glVertex3f(r * x * zr1, r * y * zr1, r * z1)

        glEnd()
    
def render():
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW) # operate on model
        
        glLoadIdentity()
        glTranslatef(0,0, 0)
        glRotatef(270,1,0,0)
        #glRotatef(-30,0,1,0)
        
        #glu depreciated...
        #gluQuad = gluNewQuadric()
        #gluQuadricTexture(gluQuad,GL_TRUE)
        #gluSphere(gluQuad,15,25,25)
        drawSphere(15,25,25)
        pygame.display.flip()


dragging = False
lastx = lasty = 0

def game() :
    global dragging, lastx, lasty
    
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN: dragging = True
            if event.type == pygame.MOUSEBUTTONUP: dragging = False
            if event.type == pygame.MOUSEMOTION and dragging == True:
                mouse_x, mouse_y = event.pos
                
                horiz = lastx - mouse_x
                vert = lasty - mouse_y
                
                lastx,lasty = event.pos
                
                glMatrixMode(GL_PROJECTION)
                glRotatef(1,-vert,-horiz,0)
            if event.type == pygame.MOUSEWHEEL:
                glMatrixMode(GL_PROJECTION)
                if event.y == 1 : scale = 0.9
                else: scale = 1.1
                glScale(scale,scale,scale)
                print(event.y)

    glMatrixMode(GL_PROJECTION)
    glRotate(-1,0,1,0)
    
    
init()
while True:
    time.sleep(0.05)
    game()
    render()
