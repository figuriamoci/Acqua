import acqua.geoCode as gc
import acqua.aqueduct as aq
gestore = "MondoAcquaCuneo"
aq.setEnv('Piemonte//'+gestore)
locationListFile = 'Metadata/Locationlist.csv'
geoReferencedLocationsFile = 'Metadata/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_piemonte.geojson'
mapFile = gestore+'.html'
gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)
