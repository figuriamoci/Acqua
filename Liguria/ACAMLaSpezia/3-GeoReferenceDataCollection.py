import acqua.geoCode as gc
import acqua.aqueduct as aq
gestore = "ACAMLaSpezia"
aq.setEnv('Liguria//'+gestore)
locationListFile = 'Metadata/LocationListReviewed.csv'
geoReferencedLocationsFile = 'Metadata/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_liguria.geojson'
mapFile = gestore+'.html'
#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)
