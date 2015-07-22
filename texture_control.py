import pygame.image

texture_dict = {}

def load_texture(name, id, alpha=False):
    global texture_dict
    im = pygame.image.load(name)
    if alpha:
        im = pygame.image.load(name).convert_alpha()
    else:
        im = pygame.image.load(name).convert()

    texture_dict[id] = im
    return im

def get_texture(id):
    return texture_dict.get(id, None)