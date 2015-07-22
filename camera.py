from shape import *

class Camera:
    def __init__(self, width, height):
        self.pos = Pnt()
        self.zoom = 1
        self.width = width
        self.height = height

    def set_pos(self, new_pos):
        self.pos = new_pos

    def set_zoom(self, new_zoom):
        self.zoom = new_zoom

    def get_pos(self):
        return self.pos.copy()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def adjust_pnt(self, pnt):
        return Pnt(self.width, self.height)/2 + pnt - self.pos