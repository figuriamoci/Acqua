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

    def getPolygon(x):
        try:
            return areas[x]
        except KeyError:
            return ''

    dfPoint = pd.DataFrame()
    dfPolygon = pd.DataFrame()

    if len(df[polygon]) > 0:
        #Retrive polygon definitions
        with open( polygonFile ) as data_file: data = json.load( data_file )
        feature_collection = json.FeatureCollection( data )
        listFeatures = feature_collection['features']
        areas_name = [listFeatures[i]['properties']['name'] for i,k in enumerate(listFeatures)]
        areas_geometry = [listFeatures[i]['geometry'] for i,k in enumerate(listFeatures)]
        areas = dict(zip(areas_name,areas_geometry))
        #Instance Nominatim
        geolocator = Nominatim(user_agent="water")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        dfPolygon = df[polygon]
        dfPolygon['geocode'] = dfPolygon['georeferencingString'].apply( geocode )
        dfPolygon['geometry'] = dfPolygon['polygonKey'].apply( getPolygon )

    if len( df[point]) > 0:
        geolocator = Nominatim(user_agent="water")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        dfPoint = df[point]
        dfPoint['geocode'] = dfPoint['georeferencingString'].apply( geocode )
        dfPoint['geometry'] = dfPoint['geocode'].apply(geoJson)

    df = pd.concat([dfPoint,dfPolygon],sort=True)

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

def retryPolygon(geoReferencedLocationsListFile,polygonFile):

    def getPolygon(x):
        try:
            return areas[x]
        except KeyError:
            return ''

    import numpy as np
    with open( polygonFile ) as data_file: data = json.load( data_file )
    feature_collection = json.FeatureCollection( data )
    listFeatures = feature_collection['features']
    areas_name = [listFeatures[i]['properties']['name'] for i, k in enumerate( listFeatures )]
    areas_geometry = [listFeatures[i]['geometry'] for i, k in enumerate( listFeatures )]
    areas = dict( zip( areas_name, areas_geometry ) )

    df = pd.read_csv(geoReferencedLocationsListFile)
    logging.info('Load geoReferencedLocationsListFile...waiting')
    n = df[df['type']=='POLYGON']
    logging.info( 'Row %s to be geocode of %s.', len( n ), len( df ) )
    df_ = df[df['type']=='POLYGON'].copy()
    df_['geometry'] = df_['polygonKey'].apply( getPolygon )
    dfR = df[df['type']=='POINT']
    dfT = pd.concat([df_,dfR])
    dfT.to_csv(geoReferencedLocationsListFile, index=False)
    n = df['type']=='POLYGON'
    logging.info('Not found %s geocode of %s.',len(n),len(df))
    return len(df)

def findGeoName(geoReferencedLocationsListFile):
    """
    Search and find geocode address for a query string
        If not possible geocode set nan.
        You can apply repeteable.

        Args: Name of file to georeferencing with 'georeferencingString' and 'geocode' fields.

        Ret: Number of addresses that could not be georeferenced
    """

    df = pd.read_csv(geoReferencedLocationsListFile)
    logging.info('Load geoReferencedLocationsListFile. Waiting...')

    geolocator = Nominatim(user_agent="water")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    n = df[df['geocode'].isnull()]
    logging.info( 'Address %s to be geocode of %s.', len( n ), len( df ) )
    df_ = df[df['geocode'].isnull()].copy()
    df_['geocode'] = df_['georeferencingString'].apply(geocode)

    dfR = df[df['geocode'].notnull()]
    dfT = pd.concat([df_,dfR])
    dfT.to_csv(geoReferencedLocationsListFile, index=False)

    n = dfT[dfT['geocode'].isnull()]
    logging.info('Sorry...not found %s geocode of %s.',len(n),len(df))

    return len(n)

def findGeometry(geoReferencedLocationsListFile,polygonFile):

    logging.info('Load locationList File...waiting')
    df = pd.read_csv(geoReferencedLocationsListFile)
    #Point elaboration
    point = df['type'] == 'POINT'
    polygon = df['type'] == 'POLYGON'

    def getPolygon(x):
        try:
            return areas[x]
        except KeyError:
            return ''

    dfPoint = pd.DataFrame()
    dfPolygon = pd.DataFrame()

    if len(df[polygon]) > 0:

        #Retrive polygon definitions
        with open( polygonFile ) as data_file: data = json.load( data_file )
        feature_collection = json.FeatureCollection( data )
        listFeatures = feature_collection['features']
        areas_name = [listFeatures[i]['properties']['name'] for i,k in enumerate(listFeatures)]
        areas_geometry = [listFeatures[i]['geometry'] for i,k in enumerate(listFeatures)]
        areas = dict(zip(areas_name,areas_geometry))

        dfPolygon = df[polygon]
        dfPolygon['geometry'] = dfPolygon['polygonKey'].apply( getPolygon )

    if len( df[point]) > 0:

        #Istantiate Nominatim
        geolocator = Nominatim(user_agent="water")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        dfPoint_ = df[point].copy()
        dfPoint = dfPoint_[dfPoint_['geometry'].isnull() & dfPoint_['geocode'].notnull()]
        dfAltro = dfPoint_[-(dfPoint_['geometry'].isnull() & dfPoint_['geocode'].notnull())]

        dfPoint['geometry'] = dfPoint['geocode'].apply( geocode ).apply(geoJson)

    df = pd.concat([dfPoint,dfAltro,dfPolygon],sort=True)
    df.to_csv(geoReferencedLocationsListFile, index=False)

    n = df[df['geocode'].isnull()]
    logging.info('Not found %s geocode of %s.',len(n),len(df))

    return len(df)