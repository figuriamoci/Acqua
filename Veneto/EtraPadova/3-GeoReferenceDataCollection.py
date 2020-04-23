import acqua.geoCode as gc
import acqua.aqueduct as aq
id_gestore = "EtraPadova"
aq.setEnv('Veneto//'+id_gestore)
locationListFile = 'Medadata/LocationList.csv'
geoReferencedLocationsFile = 'Medadata/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_veneto.geojson'
mapFile = id_gestore+'.html'
#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)
