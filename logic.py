from math import *
from shape import *
import entity_control
import entity

"""a logic class, controlling a socketed entity"""
class Logic:
    def __init__(self):
        self.vehicle = None

    """called every time the parent entity is updated"""
    def update(self, delta):
        pass

class Enemy_Basic_Logic(Logic):
    def __init__(self, target_id):
        Logic.__init__(self)
        self.target_id = target_id
        self.chase_state = None

    def update(self, update):
        target = entity_control.get_entity(self.target_id)

        if target:
            diff = target.pos - self.vehicle.pos
            if self.chase_state == None:
                self.vehicle.socket_logic(Enemy_Basic_Chaser_Logic(self.target_id), 'move')
                self.chase_state = True

            if diff.mag() < 150 and self.chase_state:
                self.vehicle.socket_logic(Enemy_Basic_Orbit_Logic(self.target_id, 75), 'move')
                self.chase_state = False
            elif diff.mag() > 200 and not self.chase_state:
                self.vehicle.socket_logic(Enemy_Basic_Chaser_Logic(self.target_id), 'move')
                self.chase_state = True

class Enemy_Basic_Chaser_Logic(Logic):
    def __init__(self, target_id):
        Logic.__init__(self)
        self.target_id = target_id

    def update(self, delta):
        #self.vehicle = entity.Enemy(self.vehicle)

        target = entity_control.get_entity(self.target_id)

        if target:
            self.vehicle.target_pos = target.pos


class Enemy_Basic_Orbit_Logic(Logic):
    def __init__(self, target_id, range):
        Logic.__init__(self)
        self.target_id = target_id
        self.dir = None
        self.range = range

    def update(self, delta):
        #self.vehicle = entity.Enemy(self.vehicle)

        target = entity_control.get_entity(self.target_id)

        if self.vehicle.velocity.mag() > 0.001:
            for i in range(delta):
                self.vehicle.velocity = self.vehicle.velocity*0.999999
        else:
            self.vehicle.velocity = Pnt()

        if target:

            #self.range = self.vehicle.target_pos - self.vehicle.pos

            if self.dir == None:
                diff = target.pos - self.vehicle.pos
                self.dir = atan2(diff.y, diff.x)
                

            self.dir -= 0.0015*delta

            self.dir = (self.dir if self.dir < 2*pi else self.dir-2*pi)
            self.dir = (self.dir if self.dir > 2*pi else self.dir+2*pi)

            self.vehicle.target_pos = Pnt(cos(self.dir), sin(self.dir)) * self.range + target.pos

"""independantly rotating orbital around parent, movement only"""
class Orbital_Logic(Logic):
    def __init__(self, relative_position, rotation_speed, move_speed=0):
        Logic.__init__(self)
        self.base_pos = relative_position
        self.speed = rotation_speed
        self.rot = 0
        self.move_speed = move_speed

    def update(self, delta):
        self.rot = self.rot + self.speed*delta

        while self.rot > pi:
            self.rot -= 2*pi
        while self.rot < -pi:
            self.rot += 2*pi


        x = (self.base_pos.x)*cos(self.rot) - (self.base_pos.y)*sin(self.rot)
        y = (self.base_pos.x)*sin(self.rot) + (self.base_pos.y)*cos(self.rot)

        target = self.vehicle.parent.pos + Pnt(x,y)

        if self.move_speed <= 0:
            self.vehicle.pos = target
        else:
            diff = target - self.vehicle.pos
            r = atan2(diff.y, diff.x)
            move = Pnt(self.move_speed*delta*cos(r), self.move_speed*delta*sin(r))
            if move.mag() > diff.mag():
                move = diff
            self.vehicle.pos += move

"""orbital, static in relation to parent, including rotation, movement only"""
class Orbital_Relative_Logic(Logic):
    def __init__(self, relative_position, move_speed=0):
        Logic.__init__(self)
        self.base_pos = relative_position

        self.move_speed = move_speed

    def update(self, delta):

        x = (self.base_pos.x)*cos(self.vehicle.parent.dir) - (self.base_pos.y)*sin(self.vehicle.parent.dir)
        y = (self.base_pos.x)*sin(self.vehicle.parent.dir) + (self.base_pos.y)*cos(self.vehicle.parent.dir)

        target = self.vehicle.parent.pos + Pnt(x,y)

        if self.move_speed <= 0:
            self.vehicle.pos = target
        else:
            diff = target - self.vehicle.pos
            r = atan2(diff.y, diff.x)
            move = Pnt(self.move_speed*delta*cos(r), self.move_speed*delta*sin(r))
            if move.mag() > diff.mag():
                move = diff
            self.vehicle.pos += move

"""orbital, static in relation to parent, no rotation, movement only"""
class Orbital_Static_Logic(Logic):
    def __init__(self, relative_position, move_speed=0):
        Logic.__init__(self)
        self.base_pos = relative_position
        self.move_speed = move_speed

    def update(self, delta):
        target = self.vehicle.parent.pos + self.base_pos

        if self.move_speed <= 0:
            self.vehicle.pos = target
        else:
            diff = target - self.vehicle.pos
            r = atan2(diff.y, diff.x)
            move = Pnt(self.move_speed*delta*cos(r), self.move_speed*delta*sin(r))
            if move.mag() > diff.mag():
                move = diff
            self.vehicle.pos += move