import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/Piemonte/AcquaNovara')

locationListFile = 'Definitions/LocationList.csv'
quartieriFile = '../ReteAcquedotti/rete_acquedotti_piemonte.geojson'
geoReferencedLocationsFile = 'Definitions/GeoReferencedLocationsList.csv'
mapFile = 'AcquaNovara.html'

#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createChoroplethDataCollection(geoReferencedLocationsFile,quartieriFile,mapFile)

