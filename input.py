#from pygame.locals import *
import pygame
from shape import Pnt

mpos = Pnt()
player_move = Pnt()

player_shoot = False

keys_down = set()

def key_down(key):
    global keys_down
    keys_down.add(key)

def key_up(key):
    global keys_down
    keys_down.discard(key)

def update():
    pass