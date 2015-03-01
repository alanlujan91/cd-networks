# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 23:35:52 2015

@author: Alan
"""

import shapefile as sf
import pandas as pd
import networkx as nx

districts = sf.Reader('cb_2013_us_cd113_500k')

shapes = districts.shapes()
records = districts.records()

df = pd.DataFrame(records, columns = [districts.fields[i][0] for i in range(1, len(districts.fields))])

g = nx.Graph()
g.position = {}

idnum = 3

for i in range(len(records)):
    district = records[i][idnum]
    g.add_node(district)
    bbox = shapes[i].bbox
    g.position[district] = [(bbox[0]+bbox[2])/2, (bbox[1] + bbox[3])/2]
    
for i in range(len(records)):
    district_i = records[i][idnum]
    points_i = shapes[i].points
    print i 
    for j in range(len(records)):
        district_j = records[j][idnum]
        points_j = shapes[j].points
        for p_i in points_i:
            if p_i in points_j:
                g.add_edge(district_i, district_j)
                pass
            
nx.draw_networkx(g)