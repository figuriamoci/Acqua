#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 00:05:42 2019

@author: andrea
"""

class LabelsCollection:
    """Class for creating and managing water labels collection"""
    labelList = []
    def __init__(self,ll):
        self.labelList = ll
        
    def append(self,e):
        self.labelList.append(e)        
        
    def __str__(self):
        """Template printing"""
        return str(self.labelList)
    
    def to_geojson(self):
        geojson = '{"type": "FeatureCollection","features": '
        feature = '['
        first = 1
        for i in self.labelList: 
            if first==1: 
                feature = feature + i.to_geojson()
                first = 0
            else: 
                feature = feature + ','+ i.to_geojson()
        return geojson+feature+']}'
            
    def to_js(self):
        output_filename = 'dataset.js'
        #with open(output_filename, 'wb') as output_file:
        #output_file.write('var dataset = ')
        #json.dump(geojson, output_file, indent=2) 
        
    def display(self):
        import geopandas as gpd
        import geojsonio
        geojsonio.display(self.to_geojson())

    
