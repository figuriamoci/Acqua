import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import logging,os
import geojson as json

def geoJson(location):
    if pd.isnull(location):
        return ''
    else:
        return {"type": "Point", "coordinates": [location.longitude, location.latitude] if location else None}

def apply(locationListFile,geoReferencedLocationsListFile,polygonFile):
    os.path.abspath(locationListFile)
    df = pd.read_csv(locationListFile)
    logging.info('Load locationList File...waiting')
    #Point elaboration
    point = df['type'] == 'POINT'
    polygon = df['type'] == 'POLYGON'

    if len( df[point] ) > 0:
        geolocator = Nominatim(user_agent="water")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        df_ = df[point]
        df_['geocode'] = df_['georeferencingString'].apply(geocode)
        df_['geometry'] = df_['geocode'].apply(geoJson)
        df = df_

    if len(df[polygon]) > 1:
        with open( polygonFile ) as data_file: data = json.load( data_file )
        feature_collection = json.FeatureCollection( data )
        listFeatures = feature_collection['features']
        areas_name = [listFeatures[i]['properties']['name'] for i,k in enumerate(listFeatures)]
        areas_geometry = [listFeatures[i]['geometry'] for i,k in enumerate(listFeatures)]
        areas = dict(zip(areas_name,areas_geometry))
        df_ = df[polygon]
        df_['geocode'] = df_['georeferencingString']
        df_['geometry'] = df_['georeferencingString'].apply( lambda x: areas[x] )
        df = df_

    df.to_csv(geoReferencedLocationsListFile, index=False)
    n = df[df['geocode'].isnull()]
    logging.info('Not found %s geocode of %s.',len(n),len(df))
    return len(df)

def retry(geoReferencedLocationsListFile):
    import numpy as np
    df = pd.read_csv(geoReferencedLocationsListFile)
    logging.info('Load geoReferencedLocationsListFile...waiting')
    geolocator = Nominatim(user_agent="water")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    n = df[df['geocode'].isnull()]
    logging.info( 'Row %s to be geocode of %s.', len( n ), len( df ) )
    df_ = df[df['geocode'].isnull()].copy()
    df_['geocode'] = df_['georeferencingString'].apply(geocode)
    df_['geometry'] = df_['geocode'].apply(geoJson)
    dfR = df[df['geocode'].notnull()]
    dfT = pd.concat([df_,dfR])
    dfT.to_csv(geoReferencedLocationsListFile, index=False)
    n = dfT[dfT['geocode'].isnull()]
    logging.info('Not found %s geocode of %s.',len(n),len(df))
    return len(df)
