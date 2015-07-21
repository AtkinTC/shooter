from shape import *
import math

types = {'point': 1, 'circle':2, 'poly':4}

def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

def shape_collide(s1, s2):
    if not bounding_box_collision(s1,s2):
        return None

    #convert type to corresponding flag
    t1 = types.get(s1.type)
    t2 = types.get(s2.type)

    #order the shapes by flag
    if t1 > t2:
        st = s1
        s1 = s2
        s2 = st

        tt = t1
        t1 = t2
        t2 = tt

    type = t1+t2

    #point on point
    if type == 2:
        return collide_pnt2pnt(s1,s2)
    #point on circle
    elif type == 3:
        return collide_pnt2circle(s1,s2)
    #circle on circle
    elif type == 4:
        return collide_circle2circle(s1,s2)
    #point on poly
    elif type == 5:
        return collide_pnt2pol(s1,s2)
    #circle on poly
    elif type == 6:
        return collide_circle2pol(s1,s2)
    #poly on poly
    elif type == 8:
        return collide_pol2pol(s1,s2)
    
"""
def collide(pos1, poly1, pos2, poly2):
    poly1_t = []
    for p in poly1:
        poly1_t.append(t_add(pos1, p))
    poly1 = poly1_t
    poly2_t = []
    for p in poly2:
        poly2_t.append(t_add(pos2, p))
    poly2 = poly2_t
    
    if len(poly1) < 1 or len(poly2) < 1:
        return False
    if len(poly1) > len(poly2):
        polyt = poly1
        poly1 = poly2
        poly2 = polyt
    if len(poly1) > 1:
        return collide_pol2pol(poly1,poly2)
    elif len(poly2) > 1:
        return collide_pnt2pol(poly1,poly2)
    else:
        return collide_pnt2pnt(poly1,poly2)
"""

def collide_pnt2pnt(s1,s2):
    if s1.centre == s2.centre:
        return s1.centre
    return False

def collide_pnt2circle(s1,s2):
    if (s1.centre-s2.centre).mag() <= s2.radius:
        return s1.centre
    return False

def collide_circle2circle(s1,s2):
    dif = s1.centre-s2.centre
    if dif.mag() <= s1.radius + s2.radius:
        return s2.centre+(dif/2)
    return False

def collide_pnt2pol(s1,s2):
    t_s = s2.get_points()
    t_s += [t_s[0]]
    
    c = s1.centre

    count = 0

    for i in range(len(s2.points)):
        a = t_s[i]
        b = t_s[i+1]
        p = ray_cast(a,b,c)
        if p:
            count += 1

    if (count%2)==1:
        return c
    else:
        return False

def collide_circle2pol(s1,s2):
    return False

def collide_pol2pol(s1,s2):
    t_s1 = s1.get_points()
    t_s1 += [t_s1[0]]
    t_s2 = s2.get_points()
    t_s2 += [t_s2[0]]
    #print t_s1, t_s2
    col = False
    for i in range(len(s1.points)):
        for j in range(len(s2.points)):
            a = t_s1[i]
            b = t_s1[i+1]
            c = t_s2[j]
            d = t_s2[j+1]

            p = intersect_bound(a,b,c,d)
            if p:
                return p
            
    p = collide_pnt2pol(Point(s1.centre),s2)
    if p:
        return p
    p = collide_pnt2pol(Point(s2.centre),s1)
    return p

def bounding_box_collision(sa, sb):
    r1 = sa.bounding_box()
    r2 = sb.bounding_box()

    x1 = max(r1.pnt.x,r2.pnt.x)
    y1 = max(r1.pnt.y,r2.pnt.y)
    x2 = min(r1.pnt.x+r1.width,r2.pnt.x+r2.width)
    y2 = min(r1.pnt.y+r1.height,r2.pnt.y+r2.height)

    return x2 >= x1 and y2 >= y1

def intersect_bound(a,b,c,d):
    min1x = min(a.x,b.x)
    min1y = min(a.y,b.y)
    max1x = max(a.x,b.x)
    max1y = max(a.y,b.y)

    min2x = min(c.x,d.x)
    min2y = min(c.y,d.y)
    max2x = max(c.x,d.x)
    max2y = max(c.y,d.y)

    #print min1x, max2x
    #if min1x > max2x or min2x > max1x or min1y > max2y or min2y > max2y:
    #    return None

    x1 = max(min1x, min2x)
    x2 = min(max1x, max2x)
    y1 = max(min1y, min2y)
    y2 = min(max1y, max2y)

    p = intersect(a,b,c,d)
    if not p:
        return None
    
    if x1 <= p.x <= x2 and y1 <= p.y <= y2:
        #print px, py
        return p
    return None

def ray_cast(p1, p2, origin, radian=0):
    rx = math.cos(radian)
    ry = math.sin(radian)
    i = intersect(p1,p2,origin,origin+Pnt(rx,ry))

    if not i:
        return None

    if rx > 0 and i.x < origin.x:
        return None
    if rx < 0 and i.x > origin.x:
        return None
    if ry > 0 and i.y < origin.y:
        return None
    if ry < 0 and i.y > origin.y:
        return None

    minx = min(p1.x,p2.x)
    maxx = max(p1.x,p2.x)
    miny = min(p1.y,p2.y)
    maxy = max(p1.y,p2.y)

    if i.x < minx or i.x > maxx or i.y < miny or i.y > maxy:
        return None

    return i
    

def intersect(a,b,c,d):
    de = (a.x-b.x)*(c.y-d.y) - (a.y-b.y)*(c.x-d.x)
    if de == 0:
        return None

    nx = (a.x*b.y-a.y*b.x)*(c.x-d.x) - (a.x-b.x)*(c.x*d.y-c.y*d.x)
    ny = (a.x*b.y-a.y*b.x)*(c.y-d.y) - (a.y-b.y)*(c.x*d.y-c.y*d.x)

    return Pnt(float(nx)/float(de), float(ny)/float(de))
