import acqua.geoCode as gc
import acqua.aqueduct as aq
gestore = "AcqueBresciane"
aq.setEnv('Lombardia//'+gestore)
locationListFile = 'Metadata/LocationList.csv'
geoReferencedLocationsFile = 'Metadata/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_lombardia(escl_Milano).geojson'
mapFile = gestore+'.html'
#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)
