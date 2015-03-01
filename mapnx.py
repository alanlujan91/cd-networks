# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 20:01:24 2015

@author: Alan
"""

import shapefile as sf
import pandas as pd
import networkx as nx
#import matplotlib.pylab as plt
from bbox import Bbox

class MapNetwork(object):
    
    def __init__(self, shapefile, node_f, sub = False, g = None, df = None, node_id = None):
        if not sub:
            shapefile = sf.Reader(shapefile)
            columns = [field[0] for field in shapefile.fields[1:]]
            shapes = shapefile.shapes()
            records = shapefile.records()
            self.node_id = columns.index(node_f)
            self.df = pd.DataFrame(records, columns = columns)
            self.df['SHAPE'] = shapes
            self.df['AREA'] = self.df['ALAND'] + self.df['AWATER']
            
            self.g = nx.Graph()
            self.g.position = {}
            for i in range(len(records)):
                node = records[i][self.node_id]
                self.g.add_node(node)
                
            for i in range(len(self.g)):
                shape_i = shapes[i]
                district_i = records[i][self.node_id]
                bbox_i = Bbox(shape_i.bbox)
                self.g.position[district_i] = bbox_i.middle()
                print i
                for j in range(i+1,len(self.g)):
                    shape_j = shapes[j]
                    district_j = records[j][self.node_id]
                    bbox_j = Bbox(shape_j.bbox)
                    if(bbox_j.isin(bbox_i)):
                        for p in shape_i.points:
                            if p in shape_j.points:
                                self.g.add_edge(district_i, district_j)
                                break
        else:
            self.g = g
            self.df = df
            self.node_id = node_id
                        
    def draw(self):
        areas = [self.df[self.df['GEOID'] == v].iloc[0]['AREA'] for v in self.g]
        m = max(areas)
        areas = [a/m*1800+600 for a in areas]
        degrees = [float(self.g.degree(v)) for v in self.g]
        nx.draw_networkx(self.g, self.g.position, with_labels = False, node_size = areas, node_color = degrees)
        
    def filtered_graph(self, attr, val):
        df = self.df[self.df[attr] == val]
        g = nx.Graph()
        node_f = self.df.columns.values[self.node_id]
        [g.add_node(v) for v in self.g.nodes() if v in df[node_f].values]
        [g.add_edge(u,v) for (u,v) in self.g.edges() if u in g and v in g]
        g.position = {node : self.g.position[node] for node in g}
        
        return MapNetwork('', '', sub = True, g = g, df = df, node_id = self.node_id)
                        
        