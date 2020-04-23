import os,logging,acqua.geoCode as gc

os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Ats')
logging.basicConfig(level=logging.INFO)

locationListFile = 'Medadata/LocationList.csv'
geoReferencedLocationsFile = 'Medadata/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_veneto.geojson'
mapFile = 'ATS.html'

#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
#gc.findGeoName(geoReferencedLocationsFile)
#gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)
