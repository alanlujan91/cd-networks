# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 12:04:30 2015

@author: Alan
"""

import fiona
import networkx as nx
import shapely.geometry as geom
import pandas as pd
from itertools import combinations

class MapNetworkxDF(object):
    
    def __init__(self, filtered = False, **kwargs):
        self.key = kwargs.get('key')
        self.source = kwargs.get('source')
        self.g = kwargs.get('g')
        self.df = kwargs.get('df')
        
        if not filtered:
            self.g = nx.Graph()
            
            with fiona.open(self.source) as nodes:
                for node in nodes:
                    self.g.add_node(node['properties'][self.key])
                    
                shapes = {node['properties'][self.key] : geom.shape(node['geometry']) for node in nodes}
                
                for u, v in combinations(self.g.nodes(), 2):
                    if shapes[u].touches(shapes[v]):
                        self.g.add_edge(u, v)
                        
                self.g.pos = {key : shapes[key].centroid.coords[0] for key in shapes.keys()}
                self.df = pd.DataFrame.from_dict([node['properties'] for node in nodes])
        
    def filtered_graph(self, attr, val): 
        df = self.df[self.df[attr] == val]
        g = nx.Graph()
        [g.add_node(node) for node in self.g.nodes() if node in df[self.key].values]
        [g.add_edge(u, v) for (u,v) in self.g.edges() if u in g and v in g]
        g.pos = {node : self.g.pos[node] for node in g}
        return MapNetworkxDF(filtered = True, g = g, df = df, key = self.key)
        
    def draw(self):
        nx.draw_networkx(self.g, pos = self.g.pos, with_labels=False)
        