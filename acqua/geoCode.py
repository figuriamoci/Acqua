import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os

def geoJson(location):
    if pd.isnull(location):
        return ''
    else:
        return {"type": "Point", "coordinates": [location.longitude, location.latitude] if location else None}

def apply(locationListFile,geoReferencedLocationsListFile):
    os.path.abspath(locationListFile)
    # df = pd.read_csv('D:\Python\WebScraping\FriuliVeneziaGiulia\CAFC\Definitions\LocationList.csv')
    df = pd.read_csv(locationListFile)
    geolocator = Nominatim(user_agent="water")

    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    df['geocode'] = df['location'].apply(geocode)
    df['geometry'] = df['geocode'].apply(geoJson)

    # df.to_csv('D:\Python\WebScraping\FriuliVeneziaGiulia\CAFC\Definitions\GeoReferencedLocationsList.csv',index=False)
    df.to_csv(geoReferencedLocationsListFile, index=False)
    return len(df)
