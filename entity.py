from shape import *
from math import *
from draw_call import Draw_call

small = 0.0000001

class Player:
    def __init__(self, image_id, shape, max_accel, max_speed, max_turn):
        self.image_id = image_id
        self.shape_base = shape
        self.shape = shape
        self.pos = Pnt()
        self.dir = math.pi
        self.max_accel = max_accel
        self.max_speed = max_speed
        self.max_turn = max_turn
        self.accel = Pnt()
        self.velocity = Pnt()
        self.rotation = 0     

    def input_aim(self, target):
        diff = target-self.pos
        target_rad = math.atan2(diff.y, diff.x) - math.pi/2
        diff_r = atan2(sin(target_rad-self.dir),cos(target_rad-self.dir))
        self.rotation = diff_r*0.01
        self.rotation = max(min(self.rotation, self.max_turn), -self.max_turn)

    def input_accel(self, acc):
        r = atan2(acc.x,acc.y)
        x = self.max_accel*sin(r)
        if abs(x) < small:
            x = 0
        y = self.max_accel*cos(r)
        if abs(y) < small:
            y = 0
        self.accel = Pnt(x,y)

    def update(self, delta):
        self.dir = self.dir + self.rotation*delta

        while self.dir > math.pi:
            self.dir = self.dir - 2*math.pi
        while self.dir < -math.pi:
            self.dir = self.dir + 2*math.pi

        for i in range(min(delta,40)):
            self.velocity = self.velocity*0.999
        
        if self.accel.mag() > small:
            self.velocity = self.velocity + self.accel*delta


        if self.velocity.mag() > self.max_speed:
            r = atan2(self.velocity.x, self.velocity.y)
            self.velocity = Pnt(self.max_speed*sin(r),self.max_speed*cos(r))

        if abs(self.velocity.x) < small:
            self.velocity.x = 0
        if abs(self.velocity.y) < small:
            self.velocity.y = 0


        self.pos = self.pos + self.velocity*delta

        self.shape.rotate(self.rotation*delta)
        
        self.rotation = 0
        self.accel = Pnt()
        
    def draw(self, cam):
        a = ((-self.dir+math.pi)*180.0)/math.pi
        
        calls = []

        call = Draw_call('image', 5)
        call.set_arg('id', self.image_id)
        call.set_arg('pos', cam.adjust_pnt(self.pos))
        call.set_arg('angle', a)
        calls.append(call)

        call = Draw_call('shape', 10)
        call.set_arg('shape', self.shape)
        call.set_arg('pos', cam.adjust_pnt(self.pos))
        call.set_arg('rgb', (100, 100, 255))
        calls.append(call)

        call = Draw_call('rect', 10)
        call.set_arg('rect', self.shape.bounding_box())
        call.set_arg('pos', cam.adjust_pnt(self.pos))
        call.set_arg('rgb', (250, 100, 100))
        calls.append(call)

        return calls
