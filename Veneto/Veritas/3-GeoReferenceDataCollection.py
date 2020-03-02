import os,logging
import acqua.geoCode as gc
logging.basicConfig(level=logging.INFO)
os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Veritas')
locationListFile = 'Definitions/LocationList.csv'
quartieriFile = '../ReteAcquedotti/rete_acquedotti_veneto.geojson'
geoReferencedLocationsFile = 'Definitions/GeoReferencedLocationsList.csv'
mapFile = 'Veritas.html'
#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createChoroplethDataCollection(geoReferencedLocationsFile,quartieriFile,mapFile)

