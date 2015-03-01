# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 18:27:27 2015

@author: Alan
"""

import shapefile as sf
import pandas as pd
import networkx as nx

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
            x_in = (b.x1 < x < b.x2) or (b.x1 > x > b.x2)
            y_in = (b.y1 < y < b.y2) or (b.y1 > y > b.y2)
            return x_in and y_in
        
        return p_in(self.x1, self.y1) or p_in(self.x2, self.y2) or p_in(self.x1, self.y2) or p_in(self.x2, self.y1)

class CountyNetwork(object):
    
    def __init__(self):
        
        districts = sf.Reader('cb_2013_us_county_500k')
        columns = [field[0] for field in districts.fields[1:]]
        self.df = pd.DataFrame(districts.records(), columns = columns)
        self.df['SHAPES'] = districts.shapes()
        
        self.g = nx.Graph()
        self.g.position = {}
        self.g.area = {}

        [self.g.add_node(district) for district in self.df.GEOID]
        bboxes = [Bbox(shape.bbox) for shape in self.df['SHAPES']]
        self.g.position = {district : bbox.middle() for (district, bbox) in zip(self.df.GEOID, bboxes)}
        self.g.area = {district : value for (district, value) in zip(self.df.GEOID, self.df.ALAND + self.df.AWATER)}
        
        
        
        
            
    
        
    
        
        
        
        