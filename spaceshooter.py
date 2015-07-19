import sys, pygame, math
from pygame.locals import *
import time
import pygame.time
import pygame.font
import pygame.image
import collision
import draw
import draw_call
import entity
import background
from shape import *
from random import randint
from pygame.time import Clock

#test

pygame.init()

clock = 0

size = width, height = 640, 480

draw.init(width,height)

def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)



ship = draw.load_image('ship.tif', True)
dust1 = draw.load_image('layers\dust_640x480_1.tif', True)
dust2 = draw.load_image('layers\dust_640x480_2.tif', True)
dust3 = draw.load_image('layers\dust_800x800_1.tif', True)
planet1 = draw.load_image('layers\planet_154x154_1.tif', True)
planet2 = draw.load_image('layers\planet_40x40_1.tif', True)
starfield = draw.load_image('layers\starfield_640x480_1.tif', True)

shape = Polygon([Pnt(0,-15),Pnt(10,15), Pnt(-10,15)], Pnt())

player = entity.Player(ship, shape, 0.001, 0.3, 0.005)

back1 = background.Background_scrolling(640, 480, dust1, 0.5, 4)
back2 = background.Background_scrolling(640, 480, dust2, 1.0, 3)
back3 = background.Background_scrolling(800, 800, dust3, 2.0, 3)
back_planet1 = background.Background_object(300, 100, 154, 154, planet1, 4, 2)
back_planet2 = background.Background_object(550, -200, 40, 40, planet2, 6, 1)
back5 = background.Background_scrolling(640, 480, starfield, 20, 0)

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
        player.input_accel(player_move)

    player.input_aim(mpos+draw.get_camera()-Pnt(width/2,height/2))

    #update loop
    player.update(delta)
    back1.update()
    back2.update()
    back3.update()
    #back4.update()
    back5.update()

    draw.camera_set(player.pos-player.velocity*delta)
    
    #draw loop

    draw_list = draw_call.Draw_list()

    back5.draw(draw_list)
    back_planet2.draw(draw_list)
    back_planet1.draw(draw_list)
    back3.draw(draw_list)
    back2.draw(draw_list)
    back1.draw(draw_list)
    player.draw(draw_list)

    draw_list.draw()
              
    draw.draw_text(str(clock/1000.0), (0,0), 255, 255, 255)
    draw.draw_text(str(fps_clock.get_fps()), (40,0), 255, 255, 255)
    draw.draw_text(str(map(int, player.pos.tuple())), (0,30), 255, 255, 255)

    draw.draw_text(str(player_move), (0,15), 255, 255, 255)

    delta = fps_clock.get_time()
    fps_clock.tick()
    
    draw.flip()

    time.sleep(0.02)

pygame.quit()
