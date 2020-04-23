import acqua.geoCode as gc
import acqua.aqueduct as aq
cod_gestore = "HydroGEA"
aq.setEnv('FriuliVeneziaGiulia//'+cod_gestore)
##
locationListFile = 'Medadata/LocationList.csv'
geoReferencedLocationsFile = 'Medadata/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_fvg.geojson'
mapFile = cod_gestore+'.html'
##
#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
#gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)
