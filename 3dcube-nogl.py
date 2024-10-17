# 3dcube - wireframe, solid and shaded
import os, math, time
import sys, pygame

WIDTH = 1000
HEIGHT = 500
screen_color = (0, 0, 0)
line_color = (255, 255, 255)
    
screen = pygame.display.set_mode((WIDTH,HEIGHT))

def rot3d (point,rotate) :
    x,y,z = point
    rx,ry,rz = rotate
            
    # about z axis 
    nX = (math.cos(rz) * x) - (math.sin(rz) * y)
    nY = (math.sin(rz) * x) + (math.cos(rz) * y)
    x = nX 
    y = nY

    # about x axis 
    nZ = (math.cos(rx) * z) - (math.sin(rx) * y)
    nY = (math.sin(rx) * z) + (math.cos(rx) * y)
    z = nZ

    # about y axis 
    nX = (math.cos(ry) * x) - (math.sin(ry) * z)
    nZ = (math.sin(ry) * x) + (math.cos(ry) * z)

    return ((nX,nY,nZ))
        
def normal (triangle) :
    t1,t2,t3 = triangle
    
    x1,y1,z1 = t1
    x2,y2,z2 = t2
    x3,y3,z3 = t3
    
    #A = t2 - t1
    A = (x2-x1, y2-y1, z2-z1)
    
    #B = t3 - t1
    B = (x3-x1, y3-y1, z3-z1)
    
    # A cross product B
    Ax,Ay,Az = A
    Bx,By,Bz = B
    
    Nx = Ay * Bz - Az * By
    Ny = Az * Bx - Ax * Bz
    Nz = Ax * By - Ay * Bx
    
    return ((Nx,Ny,Nz))

def dotproduct(A,B):
     ax,ay,az = A
     bx,by,bz = B
 
     return ( ax * bx + ay * by + az * bz)

def to2d(xyz):
    x,y,z = xyz
    z = z - 200
    x = x * 1000 / z
    y = y * 1000 / z
    return ((500 + int(x),250 + int(y)))

def polyline (p1,p2,p3,p4):
    rgb = (255,255,255)
    pygame.draw.line(screen,rgb,p1,p2)
    pygame.draw.line(screen,rgb,p2,p3)
    pygame.draw.line(screen,rgb,p3,p4)
    pygame.draw.line(screen,rgb,p4,p1)

mode = angle = 0
facecolors= []
points = []
faces = []
def init() :
        global points, faces, facecolors 
        #cube points
        points = [
            [ 10,  10,  10],
             [-10,  10,  10],
             [-10, -10,  10],
             [ 10, -10,  10],
             [ 10,  10, -10],
             [-10,  10, -10],
             [-10, -10, -10],
             [ 10, -10, -10]]
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
            [255,0,0], # red
            [255,0,0],
            [0,255,0], # green
            [0,255,0],
            [0,0,255], # blue
            [0,0,255],
            [255,255,0], # yellow
            [255,255,0],
            [0,255,255], # cyan
            [0,255,255],
            [255,0,255], # magenta
            [255,0,255]
            ]
         
def update(tick) :
        global angle,mode
        mode = 2
        angle += 0.1
        
def draw(tick) :
        global angle,mode
        global facecolors
        
        screen_color = (0,0,0)
        screen.fill(screen_color)
        
        i = 0
        oldt2 = 0
        # get each face (3d triangle)
        for face in faces:
            triangle = []
            for pointindex in face:
                point3 = points[pointindex]
                rotated3 = rot3d(point3,[angle,0,angle])
                triangle.append (rotated3)      
            
            # find normal of triangle 
            n = normal(triangle)
            camera = (0,0,10)
            d = dotproduct(n,camera)
            
            #hidden surface removal
            #only draw if facing camera
            if (d > 0) : continue
            
            # 3d points to 2d screen
            t1,t2,t3 = triangle
            t1 = to2d(t1)
            t2 = to2d(t2)
            t3 = to2d(t3)
            
            if mode == 0:
                #wireframe
                # quad (merge 2 consecutive triangles)
                if (i % 2) :
                    white = (255,255,255)
                    pygame.draw.polygon (screen,white,[t2,t2old,t1,t3],1)
                t2old = t2
            if mode == 1:
                # shade by normal to screen camera
                d = abs(d) / 50
                shade = (d,d,d)
                pygame.draw.polygon (screen,shade,[t1,t2,t3])
            if mode == 2:
                # solid colors for faces
                r,g,b = facecolors[i]
                color = (r,g,b)
                pygame.draw.polygon (screen,color,[t1,t2,t3])    
            i += 1
                
init()
while True:
    update(0)
    draw(0)
    pygame.display.flip()
    time.sleep(0.04)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
