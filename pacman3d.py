#pacman - 80s game,but in 3D

import pygame, random
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

#cube
vertices = [[ 1,  1,  1], [-1,  1,  1], [-1, -1,  1], [ 1, -1,  1], [ 1,  1, -1], [-1,  1, -1], [-1, -1, -1], [ 1, -1, -1]]
faces = [[0, 1, 2],[0, 2, 3],[4, 0, 3],[4, 3, 7],[5, 4, 7],[5, 7, 6],[1, 5, 6],[1, 6, 2],[4, 5, 1],[4, 1, 0],[2, 6, 7],[2, 7, 3]]

WALL = 0
DOT = 1
#define EMPTY    2
#define BLOCK    3
PILL = 4

maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 4, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [2, 2, 2, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 2, 2, 2],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 3, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [2, 2, 2, 2, 1, 1, 1, 0, 3, 3, 3, 0, 1, 1, 1, 2, 2, 2, 2],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [2, 2, 2, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1, 0, 1, 0, 2, 2, 2],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

ghosts:list = []
dots:list = []
pills:list = []
player = 0

class shapeobj:
    x = y = z = 0
    xd = yd = zd = 0
    color = 0
    
def drawCube():
    glBegin(GL_QUADS)
    f2old = 0
    for i in range(len(faces)):
        #r,g,b = facecolors[i]
        face = faces[i]
         
        f1,f2,f3 = face
        if (i % 2) :
            glTexCoord2f(0.0, 1.0)
            glVertex3fv(vertices[f2])
            glTexCoord2f(1.0, 1.0)
            glVertex3fv(vertices[f2old])
            glTexCoord2f(1.0, 0.0)
            glVertex3fv(vertices[f1])
            glTexCoord2f(0.0, 0.0)
            glVertex3fv(vertices[f3])
        f2old = f2
    glEnd()

def loadTexture():
    textureSurface = pygame.image.load('crate.bmp')
    textureData = pygame.image.tostring(textureSurface, "RGBA", True)
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
    global walls,player,ghosts,dots
    
    pygame.init()
    display = (900,900)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glMatrixMode(GL_PROJECTION) # operate on projection (world)
    glLoadIdentity()           
    
    #glRotatef(270,0,0,1)
    #glTranslatef(-0.8,-0.7, 0)
    gluPerspective(40.0, display[0]/display[1], 0.1, 200.0)
    glTranslatef(-20,-20,-70)
    
    glFrontFace(GL_CCW)
    #glEnable(GL_CULL_FACE)  # doesn't need normals if winding order is correct 
    glEnable(GL_DEPTH_TEST)
    #gluLookAt(20,-10,-30,0,0,-44.5,0,1,0);
    walls = []
    dots = []
    
    for y in range(len(maze)):       
        for x in range(len(maze[0])):
            object = maze[y][x] 
            if object == WALL:
                w = shapeobj()
                w.x = x * 2
                w.y = y * 2
                walls.append(w)
            if object == DOT:
                d = shapeobj()
                d.x = x * 2
                d.y = y * 2
                dots.append(d)
            if object == PILL:
                p = shapeobj()
                p.x = x * 2
                p.y = y * 2
                pills.append(p)
    
    ghosts = []
    ghostcolors = [[1,0,0],[0.7,0.5,0.5],[0,1,1],[1,0.5,0]] # red,pink,cyan,orange
    for color in ghostcolors :
        g = shapeobj()
        g.color = color
        g.x = random.randrange(8,11)
        g.y = 8
        g.xd = 1
        ghosts.append(g)
    
    player = shapeobj()
    player.x = 9
    player.y = 4
    player.xd = -1
    
    loadTexture()

def render():
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW) # operate on model
  
        #walls
        for w in walls :  
            glLoadIdentity()
            glTranslatef(w.x, w.y, w.z)
            drawCube()
        
        #player pacman
        glLoadIdentity()
        glTranslatef(player.x *2, player.y *2, 0)
        glColor3f(1,1,0)
        gluQuad = gluNewQuadric()
        gluSphere(gluQuad,1,30,5)
        
        #ghosts
        for g in ghosts:
            glLoadIdentity()
            glTranslatef(g.x *2, g.y *2, 0)
            glColor3f(*g.color)
            gluSphere(gluQuad,1,10,10)
 
        for d in dots:
            glLoadIdentity()
            glTranslatef(d.x, d.y, d.z)
            glColor3f(1,1,1) 
            gluSphere(gluQuad,0.2,10,10)
            
        for d in pills:
            glLoadIdentity()
            glTranslatef(d.x, d.y, d.z)
            c = random.randrange(2)
            glColor3f(c,c,c) 
            gluSphere(gluQuad,0.5,10,10)
             
        glColor3f(1,1,1)
        pygame.display.flip()

def findgaps(s):
    exits = []
    if maze[round(s.y + 1)][round(s.x)]: exits.append([0,1])
    if maze[round(s.y - 1)][round(s.x)]: exits.append([0,-1])
    if maze[round(s.y)][round(s.x + 1)]: exits.append([1,0])
    if maze[round(s.y)][round(s.x - 1)]: exits.append([-1,0])
    return exits

def hitwalls(s):
    hit = 0
    nextx = s.x + s.xd / 5
    nexty = s.y + s.yd / 5
    
    dest = maze[round(nexty)][round(nextx)]
    
    if (dest == WALL): hit = 1
    else : hit = 0
    
    if not hit:
        s.x = nextx
        s.y = nexty
    
    if s.xd == 0: s.x = round(s.x)
    if s.yd == 0: s.y = round(s.y)
    #wraparound
    if s.x < 0 : s.x = 17
    if s.x > 17.5 : s.x = 0
    
    return hit   
    
def game() :
    
    keys = pygame.key.get_pressed()

    move = [0,0]
    if keys[pygame.K_RIGHT]: move = [1,0]     
    if keys[pygame.K_LEFT] : move = [-1,0]
    if keys[pygame.K_UP]   : move = [0,1]
    if keys[pygame.K_DOWN] : move = [0,-1]
    exits = findgaps(player)
    if move in exits: player.xd,player.yd = move
 
    if hitwalls(player) :
        player.xd = player.yd = 0
    
    for g in ghosts:
        if abs(g.x-player.x) < 0.5 and abs(g.y-player.y) < 0.5 :
            init() # collide with ghost and die
        if hitwalls(g):
            exits = findgaps(g)
            dir = random.randrange(len(exits))
            g.xd,g.yd = exits[dir]
                    
    for d in dots:
        if abs(d.x/2 - player.x) < 0.5 and abs(d.y/2 - player.y) < 0.5:
            dots.remove(d)
                
    for p in pills:
        if abs(p.x/2 - player.x) < 0.5 and abs(p.y/2 - player.y) < 0.5:
            powerup = 100
            pills.remove(p)

init()
dragging = False
lasty = lastx = 0
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
                glTranslatef(20,20,-20)
                glRotatef(1,vert *2,horiz *2,0)
                glTranslatef(-20,-20,20)
    game()
    render()
