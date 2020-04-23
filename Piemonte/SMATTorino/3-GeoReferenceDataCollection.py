import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)
#os.chdir('D://Python//Acqua')
os.chdir('//Users//andrea//PycharmProjects//Acqua')
os.chdir('Piemonte//SMATTorino')
locationListFile = 'Medadata/LocationList.csv'
quartieriFile = '../ReteAcquedotti/rete_acquedotti_piemonte.geojson'
geoReferencedLocationsFile = 'Medadata/GeoReferencedLocationsList.csv'
mapFile = 'SMATTorino.html'
#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createChoroplethDataCollection(geoReferencedLocationsFile,quartieriFile,mapFile)

