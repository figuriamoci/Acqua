##
import os,pandas as pd,logging
import acqua.geoCode as gc
logging.basicConfig(level=logging.INFO)
os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Bim')
locationListFile = 'Definitions/LocationList.csv'
quartieriFile = '../ReteAcquedotti/rete_acquedotti_veneto.geojson'
geoReferencedLocationsFile = 'Definitions/GeoReferencedLocationsList.csv'
mapFile = 'Bim.html'

def rimuoviTermini():
    gc.createGeoReferencedLocationsList( locationListFile, geoReferencedLocationsFile )
    df = pd.read_csv( geoReferencedLocationsFile )
    df['georeferencingString'] = df['georeferencingString'].apply(
        lambda s: s.replace( 'FRAZIONE', '' ).replace( "LOCALITA'", '' ) )
    df.to_csv( geoReferencedLocationsFile, index=False )
    return 0
##
#rimuoviTermini():
#gc.findGeoName(geoReferencedLocationsFile)
#gc.findCoordinates(geoReferencedLocationsFile)
gc.createChoroplethDataCollection(geoReferencedLocationsFile,quartieriFile,mapFile)
