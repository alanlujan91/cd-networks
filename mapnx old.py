# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 20:01:24 2015

@author: Alan
"""

class MapNetwork(object):
    import shapefile as sf
    import pandas as pd
    import networkx as nx
    import matplotlib.pylab as plt
    from bbox import Bbox
    
    def __init__(self, shapefile, node_f):
        shapefile = sf.Reader(shapefile)
        columns = [field[0] for field in shapefile.fields[1:]]
        shapes = shapefile.shapes()
        records = shapefile.records()
        self.df = pd.DataFrame(shapefile.records(), columns = columns)
        self.df['SHAPE'] = shapefile.shapes()
        
        self.g = nx.Graph()
        [self.g.add_node(n) for n in self.df[node_f]]
        
        for i in range(len(self.g)):
            shape_i = self.df.iloc[i]
            district_i = shape_i[node_f]
            bbox_i = Bbox(shape_i['SHAPE'].bbox)
            print i
            for j in range(i+1,len(self.g)):
                shape_j = self.df.iloc[j]
                district_j = shape_j[node_f]
                bbox_j = Bbox(shape_j['SHAPE'].bbox)
                if(bbox_j.isin(bbox_i)):
                    for p in shape_i['SHAPE'].points:
                        if p in shape_j['SHAPE'].points:
                            self.g.add_edge(district_i, district_j)
                            break