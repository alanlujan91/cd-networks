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
from math import ceil, floor, fabs

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
            rounding_coefficient = 2.0
            for i in range(len(records)):
                bbox = shapes[i].bbox
                min_x = floor(rounding_coefficient * min(bbox[0], bbox[2])) / rounding_coefficient
                min_y = floor(rounding_coefficient * min(bbox[1], bbox[3])) / rounding_coefficient
                max_x = ceil(rounding_coefficient * max(bbox[0], bbox[2])) / rounding_coefficient
                max_y = ceil(rounding_coefficient * max(bbox[1], bbox[3])) / rounding_coefficient
                node = records[i][self.node_id]
                shapes[i].bbox_round = [min_x,min_y, max_x, max_y]
                self.g.add_node(node)
                
            state_index = columns.index("STATEFP")
            for i in range(len(self.g)):
                shape_i = shapes[i]
                district_i = records[i][self.node_id]
                bbox_i = Bbox(shape_i.bbox)
                self.g.position[district_i] = bbox_i.middle()
                bbox_i = Bbox(shape_i.bbox_round)
                print i
                state_i = records[i][state_index]
                for j in range(i+1,len(self.g)):
                    if records[j][state_index] != state_i:
                        continue
                    shape_j = shapes[j]
                    district_j = records[j][self.node_id]
                    bbox_j = Bbox(shape_j.bbox_round)
                    if(bbox_j.isin(bbox_i)):
                        for p in shape_i.points:
                            if p in shape_j.points:
                                self.g.add_edge(district_i, district_j)
                                break
                            else :
                                contains = False
                                for c in shape_j.points:
                                    if fabs(p[0] - c[0]) <= 0.001 and fabs(p[1] - c[1]) <= 0.001:
                                        self.g.add_edge(district_i, district_j)
                                        contains = True
                                        break
                                if contains:
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
                        
        