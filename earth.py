# super simple 3d earth, texmapped sphere, no fragment shader

import pygame, time, random
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

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
    
    gluPerspective(40.0, display[0]/display[1], 0.1, 200.0)
    glTranslatef(0,0,-50)
    
    glFrontFace(GL_CCW)
    glEnable(GL_DEPTH_TEST)
 
    loadTexture()

def render():
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW) # operate on model
  
        white = (1,1,1)
        yellow = (1,1,0)
        blue = (0,0,1)
        
        glLoadIdentity()
        glTranslatef(0,0, 0)
        #glColor3f(*white)
        glRotatef(270,1,0,0)
        #glRotatef(30,1,1,0)
        gluQuad = gluNewQuadric()
        gluQuadricTexture(gluQuad,GL_TRUE)
        gluSphere(gluQuad,15,25,25)
       
        pygame.display.flip()

def game() :
    keys = pygame.key.get_pressed()

    move = [0,0]

init()

dragging = False
lastx = lasty = 0
while True:
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
    glMatrixMode(GL_PROJECTION)
    glRotate(-1,0,1,0)
    time.sleep(0.05)
    game()
    render()
