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
            [0.5,0,0], # red
            [0.5,0,0],
            [0,0.5,0], # green
            [0,0.5,0],
            [0,0,0.5], # blue
            [0,0,0.5],
            [0.5,0.5,0], # yellow
            [0.5,0.5,0],
            [0,0.5,0.5], # cyan
            [0,0.5,0.5],
            [0.5,0,0.5], # magenta
            [0.5,0,0.5]
            ]

class shapeobj:
    x = y = z = 0
    dx = dy = dz = 0
    angle = spin = 0
    w = l = h = 0
    
def drawCube():
    glBegin(GL_TRIANGLES)
    for i in range(len(faces)):
         r,g,b = facecolors[i]
         glColor3f(r,g,b)
         face = faces[i]
         for vertex in face:
           glVertex3fv(verticies[vertex]) 
    glEnd()

def drawGround():
    ground_vertices = ( (-100,-0.1,50), (100,-0.1,50), (-100,-0.1,-300), (100,-0.1,-300))
    glBegin(GL_QUADS)
    glColor3fv((0.1,0.2,0))
    for vertex in ground_vertices:
        glVertex3fv(vertex)
    glEnd()
    
def init():
    global cubes
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glMatrixMode(GL_PROJECTION) # operate on projection (world)
    #glLoadIdentity()           
    
    gluPerspective(50.0, display[0]/display[1], 0.1, 300.0)
    glTranslatef(0, -2, 0) # viewer flying 2 units up
    glEnable(GL_CULL_FACE)  # doesn't need normals if winding order is correct 
    glEnable(GL_DEPTH_TEST)

    cubes = []
    for i in range(50) :
            c = shapeobj()
            c.x = random.uniform(-100,50)
            c.y = 1
            c.z = random.uniform(-50,50)
            
            c.h = random.uniform(1,5)
            cubes.append(c)
            
def render():
        global x,y,z
        global cubes
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW) # operate on model
 
        glLoadIdentity()
        drawGround()
        
        # cubes
        for c in cubes :  
            glLoadIdentity()
            glScale(1,c.h,1)
            glTranslatef(c.x, c.y, c.z)
            glRotatef(c.angle, 1.0, 1.0, 0.0)
            drawCube()
    
        glMatrixMode(GL_PROJECTION)
        #glRotatef(x,0,1,0)
        glTranslatef(x, y, z)
        
        #find out where the current viewer position 
        matrixMV = glGetFloatv(GL_PROJECTION_MATRIX)
        
        # constrain to groundsize (50,-50)
        mx,my,mm,mz = matrixMV[3]
        if (mz > 60 - my) : z = 0.01 
        if (mz < -50) : z = -0.01
        if (mx > 150) : x = -0.01
        if (mx < -100) : x = 0.01
        
x = y = z = 0
jumping = 0

def game() :
    global x,y,z
    global jumping
        
    keys = pygame.key.get_pressed()
    x += (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * 0.01
    
    if keys[pygame.K_SPACE] and not jumping : jumping = 200
    if jumping > 0 :
            jumping -= 1
            if jumping >= 100 : y = -0.1
            else : y = 0.1
    if not jumping : y = 0
        
    z -= (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 0.01
        
    x *= 0.95
    z *= 0.95
    
init()
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    game()
    render()
    pygame.display.flip()
