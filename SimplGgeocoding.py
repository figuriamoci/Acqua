import pandas as pd
loc = ['Udine', 'Gorizia']
df = pd.DataFrame(loc,columns = ['name'])

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="water")
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

df['geocode'] = df['name'].apply(geocode)
#def geoJson(coord): return [coord.latitude,coord.longitude]
#
#df['coordinates'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)

def geoJson(location): return {'type':'Point','coordinates':[location.latitude,location.longitude] }

df['location'] = df['geocode'].apply(geoJson)

pp=df[['name','location']]
pp.to_json('x.json',orient='records')
#df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
#db.spatial.find( { location: { $near: { $geometry: { type: "Point",  coordinates: [45.50,13.12] }, $maxDistance: 5000 } } } )

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
location = geolocator.geocode("175 5th Avenue NYC")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)
