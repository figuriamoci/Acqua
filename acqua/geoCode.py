import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import logging
import os

def geoJson(location):
    if pd.isnull(location):
        return ''
    else:
        return {"type": "Point", "coordinates": [location.longitude, location.latitude] if location else None}

def apply(locationListFile,geoReferencedLocationsListFile):
    os.path.abspath(locationListFile)
    df = pd.read_csv(locationListFile)
    logging.info('Load locationList File...waiting')
    geolocator = Nominatim(user_agent="water")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    df['geocode'] = df['georeferencingString'].apply(geocode)
    df['geometry'] = df['geocode'].apply(geoJson)
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
