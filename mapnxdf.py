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
    
    def __init__(self, **kwargs):
        self.key = kwargs.get('key')
        self.source = kwargs.get('source')
        self.g = nx.Graph()
        
        with fiona.open(self.source) as nodes:
            for node in nodes:
                self.g.add_node(node['properties'][key])
                
            shapes = {node['properties'][key] : geom.shape(node['geometry']) for node in nodes}
            
            for u, v in combinations(self.g.nodes(), 2):
                if shapes[u].touches(shapes[v]):
                    self.g.add_edge(u, v)
                    
        self.df = pd.DataFrame.from_dict([node['properties'] for node in nodes])
        
    def filtered_graph(self, attr, val): 
        df = self.df[self.df[attr] == val]
        g = nx.Graph()
        [g.add_node(node) for node in self.g.nodes() if node in df[attr].values]
        [g.add_edge(u, v) for (u,v) in self.g.edges() if u in g and v in g]
        