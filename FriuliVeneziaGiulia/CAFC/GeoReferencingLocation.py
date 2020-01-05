import pandas as pd
import os
os.path.abspath("Definitions/LocationList.csv")
#df = pd.read_csv('D:\Python\WebScraping\FriuliVeneziaGiulia\CAFC\Definitions\LocationList.csv')
df = pd.read_csv('Definitions/LocationList.csv') 

def geoJson(location): 
    if pd.isnull(location):
        return ''
    else:
        return {"type":"Point","coordinates":[location.longitude,location.latitude] if location else None}
    
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="water")
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
df['geocode'] = df['location'].apply(geocode)
df['geometry'] = df['geocode'].apply(geoJson)

#df.to_csv('D:\Python\WebScraping\FriuliVeneziaGiulia\CAFC\Definitions\GeoReferencedLocationsList.csv',index=False)
df.to_csv('Definitions/GeoReferencedLocationsList.csv',index=False)
