##
#Location di interesse per i parametri dell'acqua

#targetLocation = 'Isola Morosini Via due fiumi'
#targetLocation = "San Canzian d'isonzo via monfalcone"
targetLocation = "Luson"


import folium,os,geojson as js,logging
from geopy.geocoders import Nominatim
import pymongo as py
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

# So...
# Draw the maps, closer than i can
m = folium.Map( location=[location.latitude, location.longitude], control_scale=True )
# Draw the point for targetLocation
popup = location.address
marker = folium.Marker( [location.latitude, location.longitude], popup=popup,
                        icon=folium.Icon( color='red', icon='info-sign' ) )
m.add_child( marker )
# done.

# Find the Water supply network target
searcingString = {"geometry": {
    "$geoIntersects": {"$geometry": {"type": "Point", "coordinates": [location.longitude, location.latitude]}}}}
listAcquedotti = list( db.rete_acuquedotti.find( searcingString ) )
try:
    rete_acquedotto = listAcquedotti[0]
    rete_acquedotto['geometry']
except:
    print( "Water supply network not found for target location!" )

# Searcing for labels within Water supply network target
searcingString = {"geometry": {"$geoWithin": {"$geometry": rete_acquedotto['geometry']}}}
listEtichette = list( db.etichette.find( searcingString ) )
closerLabel = listEtichette[0]

# Convert dict to geoJSON for rete_acquedotto
ra = {"type": rete_acquedotto["type"], "geometry": rete_acquedotto["geometry"],
      "properties": rete_acquedotto["properties"]}
popup = '<table align="left">'
popup = rete_acquedotto["properties"]['name']
gj = folium.GeoJson( data=ra )
# gj.add_child(folium.Popup(popup))
gj.add_to( m )

# Draw reference geometry
i = 0
for label in listEtichette:
    i += 1
    gjson = {"type": label["type"], "geometry": label["geometry"], "properties": label["properties"]}

    popup = '<table align="left">'
    l = label["properties"]
    for k, v in l.items():
        popup += "<tr><td>" + k + "</td><td>" + v + "<td></tr>"
    popup += "</table>"
    if i == 1: firstPopup = popup
    gj = folium.GeoJson( data=gjson )
    gj.add_child( folium.Popup( l['reference'] ) )
    # print(l['reference'],l['gestore'])
    gj.add_to( m )

# Draw the lab
import webbrowser
output_file = "index.html"
m.save(output_file)
webbrowser.open(output_file, new=2)  # open in new tab
print(firstPopup)
##

