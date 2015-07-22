import sys, pygame
from pygame.locals import *
import pygame.font
import pygame.image
import pygame.transform
from shape import *
import math
import texture_control

from draw_call import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

w, h = 320,240
screen = None
font = None


image_dict = {}
image_dict_large = -1

def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

def init(width=320, height=240):
    global screen, w, h, font
    w = width
    h = height

    screen = pygame.display.set_mode((w,h), OPENGL|DOUBLEBUF)
    pygame.font.init()
    font = pygame.font.SysFont(None, 15)

    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_BLEND)

def draw_loop(draw_calls):

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, w, 0.0, h, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glPushMatrix()

    for call in draw_calls.ordered_calls():
        glLoadIdentity()
        call.run()

    glColor4ub(255,255,255,255)


    glBegin(GL_LINE_LOOP); 
    glVertex2f(20, 100)
    glVertex2f(100, 100)
    glVertex2f(100, 20)
    glVertex2f(20, 20)
    glEnd(); 


    glPopMatrix()

    pygame.display.flip()

def draw_texture_gl(texture, pos, area=None, angle=0):

    #glTranslate(w-pos.x, h-pos.y, 0.0)
    
    glColor4f(1.0, 1.0, 1.0, 1.0)

    glBindTexture(GL_TEXTURE_2D, texture.tex_ID)

    glBegin(GL_QUADS)

    glTexCoord(0.0, 1.0)
    glVertex2f(pos.x, h-pos.y)

    glTexCoord(1.0, 1.0)
    glVertex2f(pos.x+texture.width, h-pos.y)

    glTexCoord(1.0, 0.0)
    glVertex2f(pos.x+texture.width, h-pos.y-texture.height)

    glTexCoord(0.0, 0.0)
    glVertex2f(pos.x, h-pos.y-texture.height)

    glEnd()

def get_dimensions():
    return Pnt(w,h)


def draw_image(texture, pos, area=None, angle=0,):
    if angle:
        d = (texture.get_width()*2, texture.get_height()*2)
        texture = pygame.transform.smoothscale(texture, d)
        texture = pygame.transform.rotate(texture, angle)
        d = (texture.get_width()/2, texture.get_height()/2)
        texture = pygame.transform.smoothscale(texture, d)


    width, height = texture.get_width(),texture.get_height()
    if area:
        width, height = area.width, area.height
    pos = pos-Pnt(width, height)/2

    if area:
        area = (area.pnt.x, area.pnt.y, area.width, area.height)

    screen.blit(texture, pos.tuple(), area)

def fill(x, y, w, h, r, g, b):
    screen.fill((r,g,b),(x,y,w,h))

def draw_shape(shape, rgb, pos = None):
    if shape.type == 'poly':
        draw_shape_polygon(shape, pos, rgb)
    elif shape.type == 'circle':
        draw_shape_circle(shape, pos, rgb)
    elif shape.type == 'point':
        draw_shape_point(shape, pos, rgb)

def draw_shape_polygon(polygon, pos, rgb):
    points = polygon.get_points()
    if pos:
        points = map(lambda a: a+pos, points)
    points = [p.tuple() for p in points]
    pygame.draw.polygon(screen, rgb, points, 1)

def draw_shape_circle(circle, pos, rgb):
    pnt = circle.centre
    if pos:
        pnt = pnt + pos
    pnt = Pnt(pnt.x, -pnt.y)
    #pygame.draw.circle(screen, rgb, map(int,pnt.tuple()), int(circle.radius), 1)
    draw_circle_gl(pnt,circle.radius, rgb)

def draw_shape_point(point, pos, rgb):
    pnt = point.centre
    if pos:
        pnt = pos + pnt
    screen.fill(rgb, (pnt.x, pnt.y, 1, 1))

def draw_rect(rect, rgb, pos = None, width = 1):
    p, w, h = rect.tuple()
    if pos:
        p = p+pos
    pygame.draw.rect(screen, rgb, (p.x, p.y, w, h), width) 

def draw_shape_bound(shape, r, g, b):
    p, w, h = shape.bounding_box().tuple()
    pygame.draw.rect(screen, (r,g,b), (p.x,p.y,w,h), 1)
    
def draw_point(pos, r, g, b):
    pygame.draw.line(screen, (r,g,b), pos, pos, 1)
        
def draw_line(pos1, pos2, r, g, b, width=1):
    pygame.draw.line(screen, (r,g,b), pos1, pos2, width)

def draw_circle(pos, rad, r, g, b):
    pygame.draw.circle(screen, (r,g,b), pos, rad)

def draw_circle_gl(pos, rad, rgb, segments = 10): 
    theta = 2 * 3.1415926 / float(segments); 
    c = math.cos(theta)
    s = math.sin(theta)
    t = 0

    x = rad
    y = 0 

    glColor3ub(255,255,255)

    glTranslate(pos.x, -pos.y, 0.0)

    glBegin(GL_LINE_LOOP); 

    glVertex2f(0, -10)
    glVertex2f(-10, -10)
    glVertex2f(-10, 0)
    glVertex2f(0, 0)
    
    """
    for ii in range(segments):
        glVertex2f(x + pos.x, y + pos.y)

        #apply the rotation matrix
        t = x;
        x = c * x - s * y;
        y = s * t + c * y;
    """
    glEnd(); 

    glTranslate(-pos.x, pos.y, 0.0)

def draw_arc(pos, rad, ang1, ang2, r, g, b, width=1):
    rect = (pos[0]-rad, pos[1]-rad, rad*2, rad*2)
    pygame.draw.arc(screen, (r,g,b), rect, ang1, ang2, width)

def draw_poly(poly, r, g, b, width=0):
    pygame.draw.polygon(screen, (r,g,b), poly, width)
    #poly.append(poly[0])
    #for i in range(len(poly)-1):
    #    draw_line(poly[i], poly[i+1], r,g,b)

def draw_text(text, pos, r,g,b):
    text = font.render(text, True, (r,g,b))
    screen.blit(text, pos)

def flip(col = (0,0,0)):
    pygame.display.flip()
    screen.fill(col)
