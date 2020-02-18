import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/Lombardia/Milano')

locationListFile = 'Definitions/LocationList.csv'
quartieriFile = 'Definitions/Quartieri_Milano.geojson'
geoReferencedLocationsFile = 'Definitions/GeoReferencedLocationsList.csv'
mapFile = 'MILANO.html'

gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,quartieriFile,mapFile)
