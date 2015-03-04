# -*- coding: utf-8 -*-
"""
Created on Sun Mar 01 14:17:31 2015

@author: Alan
"""

class Point(object):
    
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        
    def dist(self, point):
        return ((selfx - point.x)**2 + (self.y - point.y)**2)**0.5
        

class Shape(object):
    
    def __init__(self, shape):
        self.shape = shape
        
    def round_pts(self, digits):
        return [[round(x, digits), round(y, digits)] for (x,y) in self.shape.points]
        
    def bbox(self):
        return Bbox(self.shape.bbox)
        
    def isin(self, shape):
        