from math import *
from shape import *

"""a logic class, controlling a socketed entity"""
class Logic:
    def __init__(self):
        self.vehicle = None

    """called every time the parent entity is updated"""
    def update(self, delta):
        pass

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