# -*- coding: utf-8 -*-
"""
Created on Sun Mar 01 14:17:31 2015

@author: Alan
"""

class Shape(object):
    
    def __init__(self, shape):
        self.shape = shape
        
    def round_pts(self, digits):
        return [[round(x, digits), round(y, digits)] for (x,y) in self.shape.points]