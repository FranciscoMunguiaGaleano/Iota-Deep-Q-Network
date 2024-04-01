# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:11:55 2021

@author: Francisco Munguia
"""

import numpy as np

class Vector2D:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
        if hasattr(x, "__getitem__"):
            x, y = x
            self._v = [float(x), float(y)]
        else:
            self._v = [float(x), float(y)]
    def __str__(self):
        return "(%s, %s)"%(self.x,self.y)
    def from_points(self,p1,p2):
        return np.array(p1)-np.array(p2)
    def get_magnitude(self):
        return math.sqrt(self.x**2+self.y**2)
    def normalize(self):
        magnitude = self.get_magnitude()
        try:
            self.x /= magnitude
            self.y /= magnitude
        except ZeroDivisionError:
            self.x = 0
            self.y = 0
    def __add__(self, rhs):
        return Vector2D(self.x + rhs.x, self.y+ rhs.y)
    def __sub__(self, rhs):
        return Vector2D(self.x - rhs.x, self.y- rhs.y)
    def __neg__(self):
        return Vector2D(-self.x,-self.y)
    def __mul__(self,scalar):
        return Vector2D(self.x*scalar,self.y*scalar)
    def __truediv__(self,scalar):
        return Vector2D(self.x/scalar,self.y/scalar)
    
    def __getitem__(self, index):
        return self._v[index]

    def __setitem__(self, index, value):
        self._v[index] = 1.0 * value
