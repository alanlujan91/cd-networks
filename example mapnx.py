# -*- coding: utf-8 -*-
"""
Created on Sun Mar 01 01:05:03 2015

@author: Alan
"""

from mapnxdf import MapNetworkxDF
from mpl_toolkits.basemap import Basemap

mnx = MapNetworkxDF(source = '..\source\cb_2013_us_county_500k.shp', key = 'GEOID')

for state in mnx.df['STATEFP'].unique():
    mnx.filtered_graph('STATEFP', state).draw()
    
m = Basemap()
m.drawstates(linewidth = 1, color = 'red')
m.drawcounties(linewidth = 0.5, color = 'blue')