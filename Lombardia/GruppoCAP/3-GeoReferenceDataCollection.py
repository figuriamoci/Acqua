import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/Lombardia/GruppoCAP')

locationListFile = 'Definitions/LocationList.csv'
quartieriFile = '../ReteAcquedotti/rete_acquedotti_lombardia(escl_Milano).geojson'
geoReferencedLocationsFile = 'Definitions/GeoReferencedLocationsList.csv'
mapFile = 'GruppoCAP.html'

#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
#gc.findGeoName(geoReferencedLocationsFile)
#gc.findCoordinates(geoReferencedLocationsFile)
gc.createChoroplethDataCollection(geoReferencedLocationsFile,quartieriFile,mapFile)

