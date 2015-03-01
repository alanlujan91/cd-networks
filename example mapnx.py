# -*- coding: utf-8 -*-
"""
Created on Sun Mar 01 01:05:03 2015

@author: Alan
"""

from mapnx import MapNetwork

mnx = MapNetwork('cb_2013_us_county_500k', 'GEOID')

for state in mnx.df['STATEFP'].unique():
    mnx.filtered_graph('STATEFP', state).draw()