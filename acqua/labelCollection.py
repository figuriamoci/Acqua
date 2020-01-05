#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 04:44:35 2020

@author: andrea
"""
import acqua.label as al
import geopandas as gpd
import geojsonio

def to_geojson(geoLabel):
    geojson = '{"type": "FeatureCollection","features": '
    feature = '['
    for i in geoLabel: 
        if feature == '[':
            feature = feature + al.to_geojson(i)
        else:
            f = al.to_geojson(i)
            if f != '': feature = feature + ','+ f
    return geojson+feature+']}'

def display(geoLabel):
    geojsonio.display(geoLabel)