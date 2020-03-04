import acqua.geoCode as gc
import acqua.aqueduct as aq
id_gestore = "ViaAcquaVicenza"
aq.setEnv('Veneto//'+id_gestore)
locationListFile = 'Definitions/LocationList.csv'
geoReferencedLocationsFile = 'Definitions/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_veneto.geojson'
mapFile = id_gestore+'.html'
#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)
