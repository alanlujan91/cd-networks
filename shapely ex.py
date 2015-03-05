# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 20:17:08 2015

@author: Alan
"""

import fiona
import shapely.geometry as geom
import networkx as nx
from itertools import combinations

counties = fiona.open('../source/cb_2013_us_county_500k.shp')

g = nx.Graph()

for county in counties:
    g.add_node(county['properties']['GEOID'])
    
shapes = {county['properties']['GEOID'] : geom.shape(county['geometry']) for county in counties}

for u, v in combinations(g.nodes(), 2):
    print u, v
    if shapes[u].touches(shapes[v]):
        g.add_edge(u, v)
        
g.pos = {key : shapes[key].centroid.coords[0] for key in shapes.keys()}

nx.draw_networkx(g, pos = g.pos, with_labels = False)