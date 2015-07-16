from draw import *

def run_draw_call(call):
    type = call.type
    if type == 'image':
        draw_image(**call.args)
    elif type == 'shape':
        draw_shape(**call.args)
    elif type == 'rect':
        draw_rect(**call.args)

class Draw_list:
    def __init__(self):
        self.dict = {}

    def append(self, call):
        if self.dict.has_key(call.depth):
            self.dict[call.depth].append(call)
        else:
            self.dict[call.depth] = [call]

    def draw(self):
        for k in self.dict.keys():
            for call in self.dict[k]:
                run_draw_call(call)
        

class Draw_call:
    def __init__(self, type, depth):
        self.type = type
        self.depth = depth
        self.args = {}

    def set_arg(self, arg, value):
        self.args[arg] = value
