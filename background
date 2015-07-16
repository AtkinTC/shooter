from draw_call import Draw_call
import draw
from shape import *

class Background_scrolling:
    def __init__(self, width, height, image_id, parallax_depth=1, depth=1):
        self.width = width
        self.height = height
        self.image_id = image_id
        self.parallax_depth = parallax_depth
        self.depth = depth
        self.centre = Pnt()

    def update(self):
        off_centre = draw.camera_align(self.centre)/self.parallax_depth
        s_dim = draw.get_dimensions()
        if off_centre.x + self.width < s_dim.x:
            self.centre.x += self.width*self.parallax_depth
            
        elif off_centre.x - self.width > 0:
            self.centre.x -= self.width*self.parallax_depth
            
        if off_centre.y + self.height < s_dim.y:
            self.centre.y += self.height*self.parallax_depth
            
        elif off_centre.y - self.height > 0:
            self.centre.y -= self.height*self.parallax_depth

    def draw(self, draw_list):
        off_centre = draw.camera_align(self.centre)/self.parallax_depth

        call = Draw_call('image', self.depth)
        call.set_arg('id', self.image_id)
        call.set_arg('pos', off_centre+Pnt(-self.width,-self.height)/2)
        call.set_arg('cam', False)
        draw_list.append(call)

        call = Draw_call('image', self.depth)
        call.set_arg('id', self.image_id)
        call.set_arg('pos', off_centre+Pnt(self.width,-self.height)/2)
        call.set_arg('cam', False)
        draw_list.append(call)

        call = Draw_call('image', self.depth)
        call.set_arg('id', self.image_id)
        call.set_arg('pos', off_centre+Pnt(-self.width,self.height)/2)
        call.set_arg('cam', False)
        draw_list.append(call)

        call = Draw_call('image', self.depth)
        call.set_arg('id', self.image_id)
        call.set_arg('pos', off_centre+Pnt(self.width,self.height)/2)
        call.set_arg('cam', False)
        draw_list.append(call)


class Background_object:
    def __init__(self, x, y, width, height, image_id, parallax_depth=1, depth=1):
        self.centre = Pnt(x,y)
        self.width = width
        self.height = height
        self.image_id = image_id
        self.parallax_depth = parallax_depth
        self.depth = depth
        

    def draw(self, draw_list):
        s_dim = draw.get_dimensions()

        call = Draw_call('image', self.depth)
        call.set_arg('id', self.image_id)
        call.set_arg('pos', (draw.camera_align(self.centre)-s_dim/2)/self.parallax_depth+s_dim/2)
        call.set_arg('cam', False)
        draw_list.append(call)

        
