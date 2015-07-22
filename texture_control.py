import pygame.image

texture_dict = {}

def load_texture(filename, id=None):
    global texture_dict
    im = pygame.image.load(filename).convert_alpha()

    if not id:
        id = 0
        while id in textures:
            id += 1
        self.tex_ID = id
    texture_dict[id] = im
    return im

def get_texture(id):
    return texture_dict.get(id, None)