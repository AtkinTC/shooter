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
        if type == 'texture':
            draw_texture(**self.args)
        elif type == 'shape':
            draw_shape(**self.args)
        elif type == 'rect':
            draw_rect(**self.args)
        elif type == 'text':
            draw_text(**self.args)

class Draw_Call_List:
    def __init__(self):
        self.dict = {}
        self.small = 0
        self.large = 0

    def append(self, calls):
        for call in calls:
            if self.dict.has_key(call.depth):
                self.dict[call.depth].append(call)
            else:
                self.dict[call.depth] = [call]
            self.small = min(self.small, call.depth)
            self.large = max(self.large, call.depth+1)

    def draw(self):
        for k in range(self.small, self.large):
            for call in self.dict.get(k, []):
                call.run_draw_call()
