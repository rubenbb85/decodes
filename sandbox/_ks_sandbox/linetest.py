import fieldpack as fp
from fieldpack import *

outie = fp.makeOut(fp.outies.Rhino, "linetest")

print "constructors"
p = Point(1,1)
v = Vec(0,0,1)
seg1 = Segment(p,v)
outie.put(seg1)

p0 = Point(-1,1)
p1 = Vec(-2,1)
seg2 = Segment(p0,p1)
outie.put(seg2)

ray1 = Ray(Point(0,-1),Vec(0,0,1))
outie.put(ray1)

lin1 = Line(Point(0,1),Vec(0,0,1))
outie.put(lin1)




outie.draw()