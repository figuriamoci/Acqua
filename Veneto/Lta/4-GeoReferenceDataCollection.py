import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Lta')

locationListFile = 'Medadata/GeoReferencingLocationList.csv'
geoReferencedLocationsFile = 'Medadata/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_veneto.geojson'
mapFile = 'LTA.html'

#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
#gc.findGeoName(geoReferencedLocationsFile)
#gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)
