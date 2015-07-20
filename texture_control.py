import pygame.image

texture_dict = {}

def load_texture(name, id, alpha=False):
    global texture_dict
    im = pygame.image.load(name)
    if alpha:
        im = im.convert_alpha()
    else:
        im = im.convert()

    texture_dict[id] = im

def get_texture(id):
    return texture_dict.get(id, None)