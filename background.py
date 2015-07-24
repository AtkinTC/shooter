from draw_call import Draw_call
import draw
import camera
from shape import *

class Background_scrolling:
    def __init__(self, texture, parallax_depth=1, depth=1):
        self.type = 'background'
        self.width = texture.get_width()
        self.height = texture.get_height()
        self.texture = texture
        self.parallax_depth = parallax_depth
        self.depth = depth
        self.centre = Pnt()
        self.id = None

    def set_camera(self, camera):
        self.camera = camera

    def set_id(self, id):
        self.id = id

    def update(self, delta):
        off_centre = self.camera.adjust_pnt(self.centre,self.parallax_depth)
        s_dim = draw.get_dimensions()
        if off_centre.x + self.width < s_dim.x:
            self.centre.x += self.width*self.parallax_depth
            
        elif off_centre.x - self.width > 0:
            self.centre.x -= self.width*self.parallax_depth
            
        if off_centre.y + self.height < s_dim.y:
            self.centre.y += self.height*self.parallax_depth
            
        elif off_centre.y - self.height > 0:
            self.centre.y -= self.height*self.parallax_depth

    def draw(self, debug):
        off_centre = self.camera.adjust_pnt(self.centre, self.parallax_depth)

        s_dim = draw.get_dimensions()

        calls = []
         
        if debug:
            calls = calls + self.debug_draw()

        #top left tile
        width, height = off_centre.x, off_centre.y
        origin = Pnt(self.width-off_centre.x, self.height-off_centre.y)

        call = Draw_call('texture', self.depth)
        call.set_arg('texture', self.texture)
        call.set_arg('pos', off_centre+Pnt(-width,-height)/2)
        call.set_arg('area', Rect(width, height, origin))
        calls.append(call)

        #top right tile
        width, height = s_dim.x-off_centre.x, off_centre.y
        origin = Pnt(0,self.height-off_centre.y)

        call = Draw_call('texture', self.depth)
        call.set_arg('texture', self.texture)
        call.set_arg('pos', off_centre+Pnt(width, -height)/2)
        call.set_arg('area', Rect(width, height, origin))
        calls.append(call)

        #bottom left tile
        width, height = off_centre.x, s_dim.y-off_centre.y
        origin = Pnt(self.width-off_centre.x,0)

        call = Draw_call('texture', self.depth)
        call.set_arg('texture', self.texture)
        call.set_arg('pos', off_centre+Pnt(-width, height)/2)
        call.set_arg('area', Rect(width, height, origin))
        calls.append(call)

        #bottom right tile
        width, height = s_dim.x-off_centre.x, s_dim.y-off_centre.y
        origin = Pnt(0,0)

        call = Draw_call('texture', self.depth)
        call.set_arg('texture', self.texture)
        call.set_arg('pos', off_centre+Pnt(width, height)/2)
        call.set_arg('area', Rect(width, height, origin))
        calls.append(call)

        return calls


    def debug_draw(self):
        off_centre = self.camera.adjust_pnt(self.centre, self.parallax_depth)

        calls = []

        call = Draw_call('line', 10)
        call.set_arg('pos1', off_centre-Pnt(5,0))
        call.set_arg('pos2', off_centre+Pnt(5,0))
        call.set_arg('rgb', (150,50,250))
        calls.append(call)

        call = Draw_call('line', 10)
        call.set_arg('pos1', off_centre-Pnt(0,5))
        call.set_arg('pos2', off_centre+Pnt(0,5))
        call.set_arg('rgb', (150,50,250))
        calls.append(call)

        return calls


class Background_object:
    def __init__(self, centre, texture, parallax_depth=1, depth=1):
        self.type = 'background'
        self.centre = centre
        self.width = texture.get_width()
        self.height = texture.get_height()
        self.texture = texture
        self.parallax_depth = parallax_depth
        self.depth = depth
        self.id = None
        
    def set_camera(self, camera):
        self.camera = camera

    def set_id(self, id):
        self.id = id

    def update(self, delta):
        return None

    def draw(self, debug):

        calls = []

        if debug:
            calls = calls + self.debug_draw()

        call = Draw_call('texture', self.depth)
        call.set_arg('texture', self.texture)
        call.set_arg('pos', (self.camera.adjust_pnt(self.centre, self.parallax_depth)))
        #call.set_arg('area', Rect(self.width/2, self.height/2, Pnt()))
        calls.append(call)

        return calls

    def debug_draw(self):
        off_centre = self.camera.adjust_pnt(self.centre, self.parallax_depth)

        calls = []

        call = Draw_call('rect', 10)
        call.set_arg('rect', Rect(self.width, self.height, off_centre-Pnt(self.width,self.height)/2))
        call.set_arg('rgb', (255,255,255))
        calls.append(call)

        return calls


        
