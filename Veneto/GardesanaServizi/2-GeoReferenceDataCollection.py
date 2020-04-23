import acqua.geoCode as gc
import acqua.aqueduct as aq
aq.setEnv('Veneto//GardesanaServizi')

locationListFile = 'Medadata/LocationList.csv'
geoReferencedLocationsFile = 'Medadata/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_veneto.geojson'
mapFile = 'GardesanaServizi.html'

gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)
