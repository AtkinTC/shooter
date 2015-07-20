from shape import *

class Camera:
    def __init__(self, width, height):
        self.pos = Pnt()
        self.zoom = 1
        self.base_width = width
        self.base_height = height

    def set_pos(self, new_pos):
        self.pos = new_pos

    def set_zoom(self, new_zoom):
        self.zoom = new_zoom

    def get_pos(self):
        return self.pos.copy()

    def get_width(self):
        return self.base_width

    def get_height(self):
        return self.base_height

    def adjust_pnt(self, pnt):
        return Pnt(self.base_width, self.base_height)/2 + pnt - self.pos