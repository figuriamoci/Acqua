#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 04:44:35 2020

@author: andreaf
"""
import acqua.label as al
import geojsonio,geojson,logging,random,sys
import geojson as js
import pymongo as py

def toHex(rgb):
    return '%02x%02x%02x' % rgb

def getRGB():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return toHex((r,g,b))

def to_geojson(geoLabel,**kwargs):
    import pandas as pd
    rgb = kwargs.get('rgb', '000000')
    ll = []
    feature_collection = []
    for geo in geoLabel:
        try:
            ll.append(al.to_geojson(geo,rgb))
        except:
            logging.critical('Skip label for %s',geo)


    feature_collection = geojson.FeatureCollection( ll )
    return feature_collection

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
    geojsonio.display(geojson.dumps( geoLabel ))

def to_file(featureCollection, fileName):
    file = open(fileName, 'w')
    file.write(geojson.dumps(featureCollection))
    file.close()
    return fileName

def to_mongoDBInsertMany(geoJsonfile):
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

def to_mongoDBInsert(geoJsonfile):
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

    for feature in listFeature:
        geoname = feature['properties']['geoname']
        logging.info( 'Inserting %s...',geoname)
        collection.insert(feature)
        logging.info( 'Insered.' )

    logging.info("Done. Safe %s feature(s)",len(listFeature))
    return listFeature

def to_mongoDB_ReteAcuquedotti(geoJsonfile):
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
    logging.info("Switch to Acqua/rete_acuquedotti collection...")
    collection = db.rete_acuquedotti
    logging.info("Saving GeoJeson Features to Acqua/etichette collection....")

    for feature in listFeature:
        geoname = feature['properties']['name']
        logging.info( 'Inserting %s...',geoname)
        collection.insert(feature)
        logging.info( 'Insered.' )

    logging.info("Done. Safe %s feature(s)",len(listFeature))
    return listFeature



def createChoroplethDataCollection(geoReferencedLocationsFile,reteAcquedottiFile,output_file):
    ##
    import pandas as pd, folium, os, logging, geojson
    from folium.plugins import MarkerCluster  # for clustering the markers

    points = pd.read_csv( geoReferencedLocationsFile )

    pointNotNull_ = points[-points['geometry'].isnull()]
    points = pointNotNull_['geometry']
    firstPoint = points.iloc[0]
    firstPointGeoJSON = geojson.loads( firstPoint.replace( "'", '"' ) )


    map = folium.Map( location=[firstPointGeoJSON['coordinates'][1], firstPointGeoJSON['coordinates'][0]],control_scale=True )

    from shapely.geometry import Point, Polygon
    with open( reteAcquedottiFile ) as f: fc = geojson.load( f )
    listFeature = fc['features']
    f = pd.DataFrame()
    for i,feature in enumerate(listFeature):
        a = feature['geometry']['coordinates'][0]
        if len(a)>=1: a = a[0]
        poligonGeoJson = Polygon(a)
        n = 0
        for j,poi in enumerate(points):
             b = geojson.loads( poi.replace( "'", '"' ) )
             c = b['coordinates']
             pointJson = Point(c)
             if pointJson.within(poligonGeoJson): n += 1

        item = {'name':feature['properties']['name'],'points' : int(n)}
        f = f.append(item,ignore_index=True)
    ##
    a = dict(fc)
    map.choropleth( geo_data = fc,name='Aree di uniformità parametrica',data=f,columns=['name','points'],fill_color='YlGn', fill_opacity=0.5, line_opacity=0.9,legend_name="Nummero parametri per area di uniformità",key_on='feature.properties.name')

    pointLayer = folium.FeatureGroup( name='Punti parametrici', show=True )
    map.add_child( pointLayer )
    marker_cluster = MarkerCluster().add_to( pointLayer )  # create marker clusters

    map.add_child( pointLayer )
    # add a marker for every record in the filtered data, use a clustered view
    for i, location in pointNotNull_.iterrows():
        # logging.info('Create Marker for (%s) %s',i,location)
        point = geojson.loads( location['geometry'].replace( "'", '"' ) )
        latitude = point['coordinates'][1]
        longitude = point['coordinates'][0]
        geocode = location['geocode']
        alias = location['alias_city'] + '/' + location['alias_address']
        folium.Marker( [latitude, longitude],popup=geocode, icon=folium.Icon( color='blue', icon='info-sign' ),tooltip=alias ).add_to( marker_cluster )

    folium.LayerControl().add_to( map )
    logging.info( 'Saving new maps...' )
    map.save( output_file )


