import acqua.geoCode as gc
import acqua.aqueduct as aq
id_gestore = "SECAMSondrio"
aq.setEnv('Lombardia//'+id_gestore)
locationListFile = 'Metadata/LocationList.csv'
geoReferencedLocationsFile = 'Metadata/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_lombardia(escl_Milano).geojson'
mapFile = id_gestore+'.html'
#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)
