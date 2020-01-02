import pandas as pd
df = pd.read_csv('Definitions/LocationList.csv') 

def geoJson(location): return [location.longitude,location.latitude] if location else None
def getLongitude(location): return location.longitude if location else None
def getLatitude(location): return location.latitude if location else None

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="water")
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

df['location'] = df['name']+', '+df['provincia']
df['geocode'] = df['location'].apply(geocode)
df['longitude'] = df['geocode'].apply(getLongitude)
df['latitude'] = df['geocode'].apply(getLatitude)

df.to_csv('Definitions/GeoReferencedLocationsList.csv',index=False)
