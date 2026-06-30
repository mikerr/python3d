# mandelbrot set, in 3D

import pygame, math,random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = []
height = 20

w = h = 100
max_iter = 255

def mandel(cx,cy,scale) :
    global vertices
    vertices = []
   
    for i in range(0,h):
      y = (i - h/2) * scale + cy;
      for j in range (0,w):
        x = (j - w/2) * scale + cx;
        
        xs = (x - 0.25)
        zx = math.sqrt(xs * xs + y * y)
        if (x < zx - 2 * zx * zx + 0.25) : continue
        if ((x + 1)*(x + 1) + y * y < 1/16) : continue

        zx = zy = 0
        for n in range (max_iter):
            iters = n       
            zx2 = zx * zx
            zy2 = zy * zy
            zy = 2 * zx * zy + y
            zx = zx2 - zy2 + x
            if (zx2 + zy2 > 4) : break
        if (iters < max_iter-1):
            vertices.append((iters/height,i/5.0,j/5.0))
                
def julia(cx,cy,scale):
    global vertices
    vertices = []
    for x in range(0,w):
        for y in range(0,h):
            zx =  (x - w/2) / w * 3 * scale
            zy =  (y - h/2) / h * 2 * scale

            for n in range (max_iter):
                iters = n
                zx2 = zx * zx
                zy2 = zy * zy
                zy = 2 * zx * zy + cy
                zx = zx2 - zy2 + cx
                if (zx2 + zy2 > 4) : break
            if (iters < max_iter-1):
                vertices.append((iters/height,x/5.0,y/5.0))
            
def draw():
    
    glPointSize(1.0)
    glBegin(GL_POINTS)
    glColor3f(0,1,0)
    for vertex in vertices:
        
        if drawcolor:
            color = int(vertex[0] * height)
            r = color & 48
            g = color & 12
            b = color & 3
            glColor3f(r,g,b)
            
        glVertex3fv(vertex)
    glEnd()

cx = -0.6
cy = 0
scale = 0.02
fractal = "mandel"
drawcolor = True

def init():
    global vertices
    
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(50, (display[0]/display[1]), 0.1, 500.0)
    glTranslatef(-2.0,-10.0, -30)
    
    vertices = []
           
def render():
    global cx,cy,scale, height, fractal, drawcolor
    
    mandel(cx,cy,scale)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: scale *= 0.98
        if keys[pygame.K_z]: scale *= 1.02
        
        if keys[pygame.K_w]: height *= 0.9
        if keys[pygame.K_s]: height *= 1.1
        
        if keys[pygame.K_LEFT]:  cx += 0.01
        if keys[pygame.K_RIGHT]: cx -= 0.01
        
        if keys[pygame.K_UP]:    cy += 0.01
        if keys[pygame.K_DOWN]:  cy -= 0.01
        
        if keys[pygame.K_m]:  fractal = "mandel"
        if keys[pygame.K_j]:  fractal = "julia"
        
        if keys[pygame.K_c]:  drawcolor = not drawcolor
        
        # interesting destinations
        if keys[pygame.K_1]: cx,cy = (-0.5,0);   scale = 0.02 # home
        if keys[pygame.K_2]: cx,cy = (-1,-0.31); scale = 0.0004 
        if keys[pygame.K_3]: cx,cy = (-1.4,0);   scale = 0.002
        if keys[pygame.K_4]: cx,cy = (-1.6156,1.02876); scale = 0.004 
        if keys[pygame.K_5]: cx,cy = (-1.53,0);    scale = 0.02
        if keys[pygame.K_6]: cx,cy = (-0.5,0); scale = 0.02
        if keys[pygame.K_7]: cx,cy = (-0.5,0); scale = 0.02
        if keys[pygame.K_8]: cx,cy = (-0.5,0); scale = 0.02
        if keys[pygame.K_9]: cx,cy = (-0.74,0.169); scale = 0.0001517
        if keys[pygame.K_0]: cx,cy = (-0.11,0.9); scale = 0.00033
        
        if any(pygame.key.get_pressed()):
            if fractal == "mandel":
                mandel(cx,cy,scale)
            else:
                julia(cx,cy,scale)
            print (cx,cy,scale)
        
        glRotatef(1, 0, 1, 0.5)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw()
        pygame.display.flip()
        pygame.time.wait(4)
init()
render()
