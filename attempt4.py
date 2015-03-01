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
g.area = {}

idnum = 4

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

for i in range(len(records)):
    district = records[i][idnum]
    g.add_node(district)
    bbox = Bbox(shapes[i].bbox)
    g.position[district] = bbox.middle()
    g.area[district] = sum(records[i][7:8])
    
for i in range(len(records)):
    district_i = records[i][idnum]
    bbox_i = Bbox(shapes[i].bbox)
    print i
    for j in range(i+1,len(records)):
        district_j = records[j][idnum]
        bbox_j = Bbox(shapes[j].bbox)
        if i != j:
            if bbox_j.isin(bbox_i):
                for p in shapes[i].points:
                    if p in shapes[j].points:
                        g.add_edge(district_i, district_j)
                        break
            
G = nx.connected_component_subgraphs(g).next()
areas = [g.area[v] for v in G]
m = max(areas)
node_color = [float(g.degree(v)) for v in g]
node_size = [g.area[v]/m*1000+300 for v in g]
nx.draw_networkx(g, pos=g.position, with_labels=False, node_color = node_color, node_size = node_size)