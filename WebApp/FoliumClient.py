#Location di interesse per i parametri dell'acqua
#targetLocation = 'Isola Morosini Via due fiumi'
##
targetLocation = "CUOA Altavilla Vicentina"

import folium,os,geojson as js,logging
from geopy.geocoders import Nominatim
import pymongo as py
os.chdir('/Users/andrea/PycharmProjects/Acqua/WebApp' )
geolocator = Nominatim(user_agent="Acqua")
location = geolocator.geocode(targetLocation)
print(location)
##
# Convert Geopy to GeoJSON model for targetLocation
import geojson
from geojson import Feature, Point

point = geojson.Point( (location.longitude, location.latitude) )
name = location.address
properties = {"name": name}
loc = Feature( geometry=point, properties=properties )

# Connecting to MongoDB/Acqua
mongoString = 'mongodb+srv://Acqua:nato1968@principal-4g7w8.mongodb.net/test?retryWrites=true&w=majority'
conn = py.MongoClient( mongoString )
db = conn.Acqua

# Draw the maps, closer than i can
m = folium.Map( location=[location.latitude, location.longitude], control_scale=True )

# Find the Water supply network target
searcingString = {"geometry": {"$geoIntersects": {"$geometry": {"type": "Point", "coordinates": [location.longitude, location.latitude]}}}}
listAcquedotti = list( db.rete_acuquedotti.find( searcingString ) )
try:
    rete_acquedotto = listAcquedotti[0]
    #rete_acquedotto['geometry']
except:
    logging.critical( "Water supply network not found for target location!" )

try:
    # Searcing for labels within Water supply network target
    searcingString = {"geometry": {"$geoWithin": {"$geometry": rete_acquedotto['geometry']}}}
    listEtichette = list( db.etichette.find( searcingString ) )
    closerLabel = listEtichette[0]
except:
    logging.critical( "Label not found!" )


# Convert dict to geoJSON for rete_acquedotto
ra = {"type": rete_acquedotto["type"], "geometry": rete_acquedotto["geometry"], "properties": rete_acquedotto["properties"]}
# popup = rete_acquedotto["properties"]['name']

gj = folium.GeoJson( data=ra )
#gj.add_child( folium.Popup( popup ) )
gj.add_to( m )

##
# Draw reference geometry
for i,label in enumerate(listEtichette):
    latitude = label['geometry']['coordinates'][1]
    longitude =  label['geometry']['coordinates'][0]
    #tooltip
    popup = '<table>'
    l = label["properties"]
    for k, v in l.items():
        popup += "<tr><td>" + k + "</td><td>" + v + "<td></tr>"
    popup += "</table>"

    if i==0:
        marker = folium.Marker( [latitude, longitude], popup=popup,icon=folium.Icon( color='blue', icon='info-sign' ) )
        firstPopUp = popup
    else:
        marker = folium.Marker( [latitude, longitude], popup=popup )

    m.add_child( marker )

# Draw the point for targetLocation
if len(listEtichette)==0:
    firstPopUp = "Non è stata trovata l'eticehtta dell'acqua."
    colorIcon = 'red'
else:
    colorIcon = 'green'

tooltip = location.address
marker = folium.Marker( [location.latitude, location.longitude],popup=firstPopUp,icon=folium.Icon( color=colorIcon, icon='home',tooltip=tooltip ) )
m.add_child( marker )
# done.
m.save('index.html')

