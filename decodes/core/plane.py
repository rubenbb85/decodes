from decodes.core import *
from . import base, vec, point #here we may only import modules that have been loaded before this one.    see core/__init__.py for proper order
if VERBOSE_FS: print "plane.py loaded"
import math


class Plane(Vec):
    """
    a simple plane class


    """
    
    def __init__(self, point=Point(), normal=Vec(0,0,1)):
        """ Plane constructor.

            :param point: Base point for a plane. 
            :type point: Point
            :param normal: Normal direction of the new Plane. Defaults to Vec(0,0,1)
            :type normal: Vec
            :result: Plane object.
            :rtype: Plane
        """
        super(Plane,self).__init__(point)
        self._vec = normal.normalized()

    
    @property
    def vec(self): 
        """ Returns the plane's vector.

            :result: Plane's vector (Point).
            :rtype: Vec
        """
        return self._vec
    @vec.setter
    def vec(self, v): 
        """ Sets the plane's vector.

            :param v: Sets the vector of the plane (Point).
            :type v: Vec, point
            :result: Plane object.
            :rtype: Plane
        """
        self._vec = v.normalized()

    @property
    def normal(self): 
        """ Returns the plane's normal.

            :result: Plane's normal.
            :rtype: Vec
        """
        return self._vec
    @normal.setter
    def normal(self, v): 
        """ Sets the plane's normal.

            :param v: Sets the normal of the plane .
            :type v: Vec
            :result: Plane object.
            :rtype: Plane
        """
        self._vec = v.normalized()

    @property
    def cpt(self): 
        """ Returns the plane's center point.

            :result: Plane's center point.
            :rtype: Point
        """
        return Point(self.x,self.y,self.z)
    @cpt.setter
    def cpt(self, pt): 
        """ Sets the plane's center point.

            :param pt: Sets the center point of the plane .
            :type pt: Point
            :result: Plane object.
            :rtype: Plane
        """
        self.x = pt.x
        self.y = pt.y
        self.z = pt.z