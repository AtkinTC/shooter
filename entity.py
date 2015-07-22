from shape import *
from math import *
from draw_call import Draw_call
import input
import entity_control

small = 0.0000001

class Entity:
    def __init__(self, texture, shape, pos):
        self.texture = texture
        self.shape = shape
        self.pos = pos
        self.camera = None
        self.type = None

    def set_id(self, id):
        self.id = id

    def set_camera(self, camera):
        self.camera = camera

    def update(self, delta):
        return None

    def draw(self):
        return None

    def collide(self, target_id, contact_pnt):
        pass

    def get_shape_proper(self):
        if self.shape.type == 'poly':
            return Polygon(self.shape.points, self.shape.centre+self.pos)
        elif self.shape.type == 'circle':
            return Circle(self.shape.radius, self.shape.centre+self.pos)
        elif self.shape.type == 'point':
            return Point(self.shape.centre+self.pos)

    def debug_draw(self):
        calls = []

        call = Draw_call('shape', 10)
        call.set_arg('shape', self.shape)
        call.set_arg('pos', self.camera.adjust_pnt(self.pos))
        call.set_arg('rgb', (100, 100, 255))
        calls.append(call)

        call = Draw_call('rect', 10)
        call.set_arg('rect', self.shape.bounding_box())
        call.set_arg('pos', self.camera.adjust_pnt(self.pos))
        call.set_arg('rgb', (250, 100, 100))
        calls.append(call)

        return calls

class Enemy(Entity):
    def __init__(self, texture, shape, pos, logic):
        Entity.__init__(self, texture, shape, pos)

        self.type = 'enemy'

        if logic:
            logic.parent = self
        else:
            self.logic = None

    def update(self, delta):
        if self.logic:
            self.logic.update()

    def draw(self, debug=False):
        calls = []

        call = Draw_call('texture', 4)
        call.set_arg('texture', self.texture)
        call.set_arg('pos', self.camera.adjust_pnt(self.pos))
        calls.append(call)

        if debug:
            calls += self.debug_draw()


        return calls


class Player(Entity):
    def __init__(self, texture, shape, max_accel, max_speed, max_turn, bullet_texture):
        Entity.__init__(self, texture, shape, Pnt())
        self.type = 'player'
        self.dir = math.pi
        self.max_accel = max_accel
        self.max_speed = max_speed
        self.max_turn = max_turn
        self.accel = Pnt()
        self.velocity = Pnt()
        self.rotation = 0
        self.cooldown = 300
        self.timer = 300
        self.bullet_texture = bullet_texture

    def input_aim(self):
        target = input.mpos+self.camera.get_pos()-Pnt(self.camera.get_width(),self.camera.get_height())/2
        diff = target-self.pos
        target_rad = math.atan2(diff.y, diff.x) - math.pi/2
        diff_r = atan2(sin(target_rad-self.dir),cos(target_rad-self.dir))
        self.rotation = diff_r*0.01
        self.rotation = max(min(self.rotation, self.max_turn), -self.max_turn)

    def input_accel(self):
        acc = input.player_move
        if acc.mag():
            r = atan2(acc.x,acc.y)
            x = self.max_accel*sin(r)
            if abs(x) < small:
                x = 0
            y = self.max_accel*cos(r)
            if abs(y) < small:
                y = 0
            self.accel = Pnt(x,y)

    def input_shoot(self):
        if self.timer >= self.cooldown and input.player_shoot:
            bullet = Projectile(self.bullet_texture, Point(), self.pos, self.dir, 0.4, 3000)
            bullet.set_camera(self.camera)
            entity_control.register(bullet)
            self.timer = 0


    def update(self, delta):
        self.input_aim()
        self.input_accel()
        self.input_shoot()

        if self.timer < self.cooldown:
            self.timer += delta

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
        
    def draw(self, debug=False):
        a = ((-self.dir+math.pi)*180.0)/math.pi
        
        calls = []

        call = Draw_call('texture', 5)
        call.set_arg('texture', self.texture)
        call.set_arg('pos', self.camera.adjust_pnt(self.pos))
        call.set_arg('angle', a)
        calls.append(call)

        if debug:
            calls += self.debug_draw()

        return calls

class Projectile(Entity):
    def __init__(self, texture, shape, pos, dir, speed, lifetime=None, rotate=False):
        Entity.__init__(self, texture, shape, pos)
        self.type = 'bullet'
        self.dir = dir
        self.velocity = Pnt(-sin(dir), cos(dir))*speed
        self.lifetime = lifetime
        self.age = 0
        self.rotate = rotate

    def update(self, delta):
        self.age += delta
        if self.lifetime and self.age >= self.lifetime:
            entity_control.kill_entity(self.id)
            return None

        self.pos = self.pos + self.velocity*delta

    def draw(self, debug=False):
        calls = []

        call = Draw_call('texture', 6)
        call.set_arg('texture', self.texture)
        call.set_arg('pos', self.camera.adjust_pnt(self.pos))
        if self.rotate:
            a = ((-self.dir+math.pi)*180.0)/math.pi
            call.set_arg('angle', a)
        calls.append(call)

        if debug:
            calls += self.debug_draw()

        return calls

    def collide(self, target_id, contact_pnt):
        if entity_control.get_entity(target_id).type == 'enemy':
            entity_control.kill_entity(self.id)