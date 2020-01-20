#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 04:44:35 2020

@author: andrea
"""
import acqua.label as al
import geojsonio
import geojson as js
import logging
import pymongo as py

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

def to_MDBCollection(geoLabel):
    json = '['
    for i in geoLabel:
        if json == '[':
            json = json + al.to_geojson(i)
        else:
            f = al.to_geojson(i)
            if f != '': json = json + ','+ f
    return json+']'

def display(geoLabel):
    from github3 import login
    geojsonio.display(geoLabel)

def to_file(feature, fileName):
    file = open(fileName, 'w')
    file.write(feature)
    file.close()
    return fileName

def to_mongoDB(geoJsonfile):
    logging.basicConfig(level=logging.INFO)
    logging.info("Loading GEOJson file '%s'...",geoJsonfile)
    with open(geoJsonfile) as f:
        geojson = js.load(f)
    listFeature = geojson['features']
    logging.info('Feature(s) load.')
    logging.info("Connecting to MongoDB...")
    mongoString = 'mongodb+srv://Acqua:nato1968@principal-4g7w8.mongodb.net/test?retryWrites=true&w=majority'
    conn = py.MongoClient(mongoString)
    db = conn.Acqua
    logging.info("Connected!")
    logging.info("Switch to Acqua/etichette collection...")
    collection = db.etichette
    logging.info("Saving GeoJeson Features to Acqua/etichette collection....")
    collection.insert_many(listFeature)
    logging.info("Done. Safe %s feature(s)",len(listFeature))
    return listFeature