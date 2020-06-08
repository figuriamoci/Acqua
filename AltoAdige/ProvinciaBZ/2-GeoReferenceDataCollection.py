import acqua.geoCode as gc
import acqua.aqueduct as aq
gestore = "ProvinciaBZ"
aq.setEnv('AltoAdige//'+gestore)
locationListFile = 'Metadata/LocationList.csv'
geoReferencedLocationsFile = 'Metadata/GeoReferencedLocationsList.csv'
reteAquedottiFile = '../ReteAcquedotti/rete_acquedotti_alto_adige.geojson'
mapFile = gestore+'.html'
gc.createGeoReferencedLocationsList(locationListFile,geoReferencedLocationsFile)
gc.findGeoName(geoReferencedLocationsFile)
gc.findCoordinates(geoReferencedLocationsFile)
gc.createMapOnGeoReferencedDataCollection(geoReferencedLocationsFile,reteAquedottiFile,mapFile)



import pandas as pd
geoRLL = pd.read_csv( 'Metadata/GeoReferencedLocationsList.csv' )
howManyGeoCode = geoRLL.groupby('alias_city').count()['geocode']
howManyGeoCode = howManyGeoCode.to_frame()
howNull = howManyGeoCode[howManyGeoCode['geocode']==0]
print(howNull)