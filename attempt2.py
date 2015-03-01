# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 23:35:52 2015

@author: Alan
"""

import shapefile as sf
import pandas as pd
import networkx as nx

districts = sf.Reader('cb_2013_us_county_500k')

shapes = districts.shapes()
records = districts.records()

df = pd.DataFrame(records, columns = [districts.fields[i][0] for i in range(1, len(districts.fields))])

g = nx.Graph()
g.position = {}

idnum = 3

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
        x1_in = (b.x1 < self.x1 < b.x2) or (b.x1 > self.x1 > b.x2)
        y1_in = (b.y1 < self.y1 < b.y2) or (b.y1 > self.y1 > b.y2)
        if (x1_in and y1_in): 
            return True
        else:
            x2_in = (b.x1 < self.x2 < b.x2) or (b.x1 > self.x2 > b.x2)
            y2_in = (b.y1 < self.y2 < b.y2) or (b.y1 > self.y2 > b.y2)
            if (x2_in and y2_in):
                return True
            else: 
                return False

for i in range(len(records)):
    district = records[i][idnum]
    g.add_node(district)
    bbox = Bbox(shapes[i].bbox)
    g.position[district] = bbox.middle()
    
for i in range(len(records)):
    district_i = records[i][idnum]
    bbox_i = Bbox(shapes[i].bbox)
    for j in range(len(records)):
        district_j = records[j][idnum]
        bbox_j = Bbox(shapes[j].bbox)
        if i != j:
            if bbox_j.isin(bbox_i):
                g.add_edge(district_i, district_j)
            
nx.draw_networkx(g, pos=g.position, with_labels=False, label='US Counties Adjacency Network')