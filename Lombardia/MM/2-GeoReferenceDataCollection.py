import acqua.geoCode as gc
import acqua.aqueduct as aq
aq.setEnv('Lombardia//MM')

locationListFile = 'Medadata/LocationList.csv'
quartieriFile = 'ReteAcquedotti/rete_acquedotti_milano.geojson'
geoReferencedLocationsFile = 'Medadata/GeoReferencedLocationsList.csv'
mapFile = 'MM.html'

#gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
#gc.findGeoName(geoReferencedLocationsFile)
#gc.findCoordinates(geoReferencedLocationsFile)
gc.createChoroplethDataCollection(geoReferencedLocationsFile,quartieriFile,mapFile)

