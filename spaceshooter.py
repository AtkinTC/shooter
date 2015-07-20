import sys, pygame, math
from pygame.locals import *
import time
import pygame.time
import pygame.font
import pygame.image
import collision
import draw
from draw_call_list import Draw_Call_List
import entity
import background
from shape import *
from random import randint
from pygame.time import Clock

from camera import Camera


clock = 0

game_dimensions = width, height = 0, 0

entities = None

camera = None

def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

def init():
    global clock, game_dimensions, width, height, entities, camera

    pygame.init()

    clock = 0

    game_dimensions = width, height = 640, 480

    draw.init(width, height)

    camera = Camera(width, height)

    ship = draw.load_image('graphics\ship.tif', True)
    dust1 = draw.load_image('graphics\layers\dust_640x480_1.tif', True)
    dust2 = draw.load_image('graphics\layers\dust_640x480_2.tif', True)
    dust3 = draw.load_image('graphics\layers\dust_800x800_1.tif', True)
    planet1 = draw.load_image('graphics\layers\planet_154x154_1.tif', True)
    planet2 = draw.load_image('graphics\layers\planet_40x40_1.tif', True)
    starfield = draw.load_image('graphics\layers\starfield_640x480_1.tif', True)

    entities = {}
    shape = Polygon([Pnt(0,-15),Pnt(10,15), Pnt(-10,15)], Pnt())
    entities['player'] = entity.Player(ship, shape, 0.001, 0.3, 0.005)

    
    entities['back1'] = background.Background_scrolling(640, 480, dust1, 0.5, 4)
    entities['back2'] = background.Background_scrolling(640, 480, dust2, 1.0, 3)
    entities['back3'] = background.Background_scrolling(800, 800, dust3, 2.0, 3)
    entities['back_planet1'] = background.Background_object(300, 100, 154, 154, planet1, 4, 2)
    entities['back_planet2'] = background.Background_object(550, -200, 40, 40, planet2, 6, 1)
    entities['back4'] = background.Background_scrolling(640, 480, starfield, 20, 0)

    for e in entities.values():
        e.set_camera(camera)
    
    


init()

count = 0
#main loop
done = False
fps_clock = Clock()
delta = 0
player_move = Pnt()
while not done:
    clock = pygame.time.get_ticks()
    mx, my = pygame.mouse.get_pos()
    mpos = Pnt(mx, my)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            #W
            if event.key == 119:
                player_move.y += -1
            #S
            if event.key == 115:
                player_move.y += 1
            #A
            if event.key == 97:
                player_move.x += -1
            #D
            if event.key == 100:
                player_move.x += 1
        if event.type == pygame.KEYUP:
            #W
            if event.key == 119:
                player_move.y += 1
            #S
            if event.key == 115:
                player_move.y += -1
            #A
            if event.key == 97:
                player_move.x += 1
            #D
            if event.key == 100:
                player_move.x += -1

    if player_move.mag():
        entities['player'].input_accel(player_move)

    entities['player'].input_aim(mpos+camera.get_pos()-Pnt(camera.get_width(),camera.get_height())/2)

    #update loop
    for e in entities.values():
        e.update(delta)

    camera.set_pos(entities['player'].pos-entities['player'].velocity*delta)
    
    #draw loop

    draw_list = Draw_Call_List()

    for e in entities.values():
        draw_list.append(e.draw())

    draw_list.draw()
              
    draw.draw_text(str(clock/1000.0), (0,0), 255, 255, 255)
    draw.draw_text(str(fps_clock.get_fps()), (40,0), 255, 255, 255)
    draw.draw_text(str(map(int, entities['player'].pos.tuple())), (0,30), 255, 255, 255)

    draw.draw_text(str(player_move), (0,15), 255, 255, 255)

    delta = fps_clock.get_time()
    fps_clock.tick()
    
    draw.flip()

    time.sleep(0.02)

pygame.quit()
