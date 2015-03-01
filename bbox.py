# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 20:34:48 2015

@author: Alan
"""

class Bbox(object):
    
    def __init__(self, coords):
        self.x1 = coords[0]
        self.x2 = coords[2]
        self.y1 = coords[1]
        self.y2 = coords[3]
        
        self.p1 = (self.x1, self.y1)
        self.p2 = (self.x2, self.y2)
        
    def middle(self):
        return ((self.x1 + self.x2)/2, (self.y1 + self.y2)/2)
        
    def isin(self, b):
        
        def p_in(x,y):
            x_in = (b.x1 <= x <= b.x2) or (b.x1 >= x >= b.x2)
            y_in = (b.y1 <= y <= b.y2) or (b.y1 >= y >= b.y2)
            return x_in and y_in
        
        return p_in(self.x1, self.y1) or p_in(self.x2, self.y2) or p_in(self.x1, self.y2) or p_in(self.x2, self.y1)