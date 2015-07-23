import sys, pygame
from pygame.locals import *
import pygame.font
import pygame.image
import pygame.transform
from shape import *
import math
import texture_control

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
    screen = pygame.display.set_mode((w,h))
    screen.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont(None, 15)

def get_dimensions():
    return Pnt(w,h)


def draw_texture(texture, pos, area=None, angle=0,):
    if angle:
        d = (texture.get_width()*2, texture.get_height()*2)
        texture = pygame.transform.smoothscale(texture, d)
        texture = pygame.transform.rotate(texture, angle)
        d = (texture.get_width()/2, texture.get_height()/2)
        texture = pygame.transform.smoothscale(texture, d)


    width, height = texture.get_width(),texture.get_height()
    if area:
        width, height = area.width, area.height
        area = (area.pnt.x, area.pnt.y, area.width, area.height)
        
    pos = pos-Pnt(width, height)/2

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
    pygame.draw.circle(screen, rgb, map(int,pnt.tuple()), int(circle.radius), 1)

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
