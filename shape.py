import math

class Pnt:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, pnt):
        if isinstance(pnt, Pnt):
            return Pnt(self.x+pnt.x, self.y+pnt.y)
        else:
            raise TypeError('can only add Pnt to Pnt')

    def __radd__(self, pnt):
            return self

    def __sub__(self, pnt):
        if isinstance(pnt, Pnt):
            return Pnt(self.x-pnt.x, self.y-pnt.y)
        else:
            raise TypeError('can only add Pnt to Pnt')

    def __mul__(self, n):
        if isinstance(n, (int, float)):
            return Pnt(self.x*n, self.y*n)
        else:
            raise TypeError('can only multiply Pnt by number')

    def __div__(self, n):
        if isinstance(n, (int, float)):
            return Pnt(self.x/n, self.y/n)
        else:
            raise TypeError('can only multiply Pnt by number')

    def __eq__(self, pnt):
        return isinstance(pnt, Pnt) and self.x == pnt.x and self.y == pnt.y
        
            
    def __str__(self):
        return 'Pnt({0.x!s},{0.y!s})'.format(self)

    def tuple(self):
        return (self.x, self.y)

    def mag(self):
        return math.pow(math.pow(self.x,2)+math.pow(self.y,2),0.5)

class Rect:
    def __init__(self, width, height, pnt=None, x=None, y=None):
        self.width = width
        self.height = height
        if pnt:
            self.pnt = pnt
        else:
            self.pnt = Pnt(x,y)

    def __eq__(self, rect):
        return isinstance(rect,Rect) and self.pnt==rect.pnt and self.width==rect.width and self.height==rect.height

    def __str__(self):
        return 'Rect(({0.pnt.x!s},{0.pnt.y!s}),{0.width!s},{0.height!s})'.format(self)

    def tuple(self, flat=0):
        if flat:
            x, y = self.pnt.tuple()
            return (x, y, self.width, self.height)
        else:
            return (self.pnt, self.width, self.height)

class Shape:
    def __init__(self):
        self.centre = Pnt()
        self.width = 0
        self.height = 0
        self.topleft = Pnt()
        self.type = None

    def translate(self, pnt):
        self.centre = self.centre + pnt

    def bounding_box(self):
        return Rect(self.width, self.height, pnt=self.topleft)

class Polygon(Shape):
    def __init__(self, points, centre=None):
        Shape.__init__(self)
        
        if len(points) < 3:
            #throw error
            print "Polygon error: needs 3 or more points"
            return None

        self.type = 'poly'

        if centre:
            self.centre = centre

        self.points = points
        self.calculate_bound()

    def get_points(self):
        points = map(lambda a: a+self.centre, self.points)
        return points

    def rotate(self, rad, pnt=None):
        cos = math.cos(rad)
        sin = math.sin(rad)

        if pnt:
            rx = cos*(self.centre.x-pnt.x) - sin*(self.centre.y-pnt.y)+pnt.x
            ry = sin*(self.centre.x-pnt.x) + cos*(self.centre.y-pnt.y)+pnt.y
            self.centre = Pnt(rx,ry)
            
        points = []
        for p in self.points:
            rx = cos*p.x - sin*p.y
            ry = sin*p.x + cos*p.y
            points.append(Pnt(rx,ry))

        self.points = points

        self.calculate_bound()

    def calculate_bound(self):
        minx = self.points[0].x
        maxx = self.points[0].x
        miny = self.points[0].y
        maxy = self.points[0].y
        for p in self.points:
            minx = min(minx, p.x)
            miny = min(miny, p.y)
            maxx = max(maxx, p.x)
            maxy = max(maxy, p.y)
        self.width = maxx-minx+2
        self.height = maxy-miny+2
        self.topleft = Pnt(self.centre.x+minx, self.centre.y+miny)

class Circle(Shape):
    def __init__(self, radius, centre=None):
        Shape.__init__(self)
        
        self.type = 'circle'

        if centre:
            self.centre = centre

        self.radius = radius
        self.width = 2*radius
        self.height = 2*radius
        self.topleft = self.centre - Pnt(radius, radius)

class Point(Shape):
    def __init__(self, centre=None):
        Shape.__init__(self)
        
        self.type = 'point'

        if centre:
            self.centre = centre
