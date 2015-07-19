from draw import *

class Draw_call:
    def __init__(self, type, depth):
        self.type = type
        self.depth = depth
        self.args = {}

    def set_arg(self, arg, value):
        self.args[arg] = value

    def run_draw_call(self):
        type = self.type
        if type == 'image':
            draw_image(**self.args)
        elif type == 'shape':
            draw_shape(**self.args)
        elif type == 'rect':
            draw_rect(**self.args)
