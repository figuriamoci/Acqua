##
import pymongo,folium,geojson,logging,json,pandas as pd,os
from geojson import Point, Feature, FeatureCollection
from shapely.geometry import Point,Polygon,MultiPolygon,shape
logging.basicConfig(level=logging.INFO)
os.chdir('//Users//andrea//PycharmProjects//Acqua')
os.chdir( 'Dashboard' )

# Connecting to MongoDB/Acqua
mongoString = 'mongodb+srv://Acqua:nato1968@principal-4g7w8.mongodb.net/test?retryWrites=true&w=majority'
conn = pymongo.MongoClient( mongoString )
db = conn.Acqua
##
searcingString = {}
e = db.etichette.find({})
points = [ Point( e_['geometry']['coordinates'] ) for e_ in e]
for e_ in e:
    coordinates = e_['geometry']['coordinates']
    p = Point( coordinates )
    points.append(p)
##
# Find the Water supply network target
searcingString = {"properties.regione":"Veneto"}
searcingString = {"properties.regione":"Friuli Venezia Giulia"}
#searcingString = {"properties.regione":"Lombardia"}
f = db.rete_acuquedotti.find( {} )
features = []
for m in f:
    geometry = m['geometry']
    properties = m['properties']
    ff = Feature(geometry=geometry,properties=properties)
    features.append(ff)
feature_collection = geojson.FeatureCollection( features )
##
counters = {f['properties']['name']:0 for f in features}
for feature in features:
    polygonName = feature['properties']['name']
    logging.info('>> %s',polygonName)
    polygon_ = json.dumps( feature['geometry'] )
    polygon = shape(geojson.loads( polygon_ ))
    n = counters[polygonName]
    for p in points:
        if polygon.contains(p):
            n += 1
            lastPoint = p
    counters[polygonName] = min(n,5)
##
coords = list(lastPoint.coords)[0]
latitude = coords[0]
longitude = coords[1]
fc = json.loads(geojson.dumps(feature_collection))#['features']
counters_ = pd.DataFrame.from_dict(counters, orient='index')
max_value = max(counters_.max().iloc[0],3)
# Draw the maps, closer than i can
map = folium.Map( location=[longitude,latitude], control_scale=True )
map.choropleth( geo_data=fc,data=counters,highlight=True, name='Aree di uniformità parametrica',fill_color='YlOrRd',fill_opacity=0.5,line_opacity=0.2,legend_name="Nummero etichette per area di uniformità parametrica",key_on='feature.properties.name' )
map.save('DensitaParametrica.html')

