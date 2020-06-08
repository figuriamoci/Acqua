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
#
searcingString = {}
e = db.etichette.find({})
points = [ Point( e_['geometry']['coordinates'] ) for e_ in e]
for e_ in e:
    coordinates = e_['geometry']['coordinates']
    p = Point( coordinates )
    points.append(p)
##
# Find the Water supply network target
#searcingString = {"properties.regione":"Veneto"}
#searcingString = {"properties.regione":"Lombardia"}
#searcingString = {"properties.regione":"EmiliaRomagna"}
#searcingString = {"properties.regione":"Piemonte"}
searcingString = {"properties.regione":"Trentino"}
#searcingString = {"properties.regione":"Friuli Venezia Giulia"}
f = db.rete_acuquedotti.find( searcingString )
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
    counters[polygonName] = min(n,1)
##
coords = list(lastPoint.coords)[0]
latitude = coords[0]
longitude = coords[1]
fc = json.loads(geojson.dumps(feature_collection))#['features']
counters_ = pd.DataFrame.from_dict(counters, orient='index')
max_value = max(counters_.max().iloc[0],3)
# Draw the maps, closer than i can
map = folium.Map( location=[longitude,latitude], control_scale=True )
map.choropleth( geo_data=fc,data=counters,highlight=True, name='Aree di uniformità parametrica',fill_color='YlGnBu',fill_opacity=0.3,line_opacity=0.2,legend_name="Nummero etichette per area di uniformità parametrica",key_on='feature.properties.name' )
map.save('DensitaParametrica.html')

#
from area import area
obj = {'type':'Polygon','coordinates':[[[-180,-90],[-180,90],[180,90],[180,-90],[-180,-90]]]}
area(obj)
features[1]

a = {"coordinates": [[[13.098978, 46.362483, 0], [13.101009, 46.362297, 0], [13.106685, 46.362194, 0], [13.115101, 46.362407, 0], [13.117086, 46.362907, 0], [13.119225, 46.363998, 0], [13.119517, 46.36438, 0], [13.120028, 46.365323, 0], [13.120139, 46.365897, 0], [13.120104, 46.366289, 0], [13.119836, 46.369028, 0], [13.118807, 46.371905, 0], [13.118773, 46.372086, 0], [13.123075, 46.380614, 0], [13.123375, 46.381046, 0], [13.123398, 46.381074, 0], [13.12342, 46.381101, 0], [13.124564, 46.382241, 0], [13.12496, 46.382558, 0], [13.134889, 46.388453, 0], [13.1382, 46.389322, 0], [13.138887, 46.38942, 0], [13.143073, 46.389856, 0], [13.145281, 46.389982, 0], [13.147709, 46.389882, 0], [13.158472, 46.389412, 0], [13.163506, 46.393504, 0], [13.163512, 46.395655, 0], [13.161555, 46.398134, 0], [13.159135, 46.400059, 0], [13.142797, 46.409298, 0], [13.141824, 46.40959, 0], [13.105129, 46.419304, 0], [13.099387, 46.416918, 0], [13.09845, 46.416893, 0], [13.086779, 46.417267, 0], [13.080829, 46.417668, 0], [13.079956, 46.417673, 0], [13.076578, 46.416097, 0], [13.074549, 46.414549, 0], [13.07419, 46.414067, 0], [13.074913, 46.413096, 0], [13.075892, 46.411936, 0], [13.076863, 46.410528, 0], [13.077069, 46.41013, 0], [13.078331, 46.407663, 0], [13.078514, 46.407301, 0], [13.078501, 46.406883, 0], [13.077925, 46.405149, 0], [13.076813, 46.402367, 0], [13.075881, 46.401873, 0], [13.070849, 46.399213, 0], [13.066571, 46.396953, 0], [13.064096, 46.395601, 0], [13.05978, 46.392933, 0], [13.058069, 46.391644, 0], [13.056558, 46.390307, 0], [13.053056, 46.386728, 0], [13.051658, 46.384437, 0], [13.051397, 46.38401, 0], [13.050277, 46.381831, 0], [13.051283, 46.381341, 0], [13.053408, 46.379731, 0], [13.054706, 46.37833, 0], [13.055874, 46.37656, 0], [13.057222, 46.374496, 0], [13.058311, 46.372677, 0], [13.05833, 46.372644, 0], [13.058379, 46.372562, 0], [13.0584, 46.372527, 0], [13.059046, 46.371448, 0], [13.060584, 46.369134, 0], [13.062039, 46.366971, 0], [13.062461, 46.366799, 0], [13.070952, 46.364169, 0], [13.071494, 46.364008, 0], [13.074403, 46.363141, 0], [13.074799, 46.363022, 0], [13.074946, 46.362978, 0], [13.076142, 46.362629, 0], [13.07707, 46.362358, 0], [13.077245, 46.362307, 0], [13.077792, 46.36226, 0], [13.078235, 46.362231, 0], [13.079199, 46.362196, 0], [13.081919, 46.362455, 0], [13.084947, 46.362868, 0], [13.090053, 46.363311, 0], [13.093618, 46.363606, 0], [13.095624, 46.363494, 0], [13.097223, 46.363126, 0], [13.098978, 46.362483, 0]]], "type": "Polygon"}
area(a)/1000000


features[1]