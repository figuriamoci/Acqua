import os, geojson, logging, acqua.labelCollection as lc
import acqua.geoCode as gc

def create_water_fountain_network(geoJsonfile):
    #logging.info( "reading %s from %s...", geoJsonfile, regione )
    with open( geoJsonfile ) as f:
        geo = geojson.load( f )
    fc = []
    for f in geo['features']:
        logging.info(f)
        if f['geometry']['type'] == 'Point':
            coordinates = f['geometry']['coordinates']
            geoname = gc.getGeoName(coordinates)
            new_properties = {'geoname': geoname, 'tipologia': 'casa_acqua'}
            f['properties'] = new_properties
            fc.append( f )
        else:
            logging.info('Skip %s',f)

    feature_collection = geojson.FeatureCollection( fc )
    logging.info( "Collected %s feature(s).", len( fc ) )
    return feature_collection

os.chdir( '/Users/andrea/PycharmProjects/Acqua/Lombardia/Milano' )

geoJsonFile = 'Source/Case_acqua_MM.geojson'
geoJsonFile_standardized = 'Definitions/Case_acqua_MM_standard.geojson'

fc = create_water_fountain_network( geoJsonFile)
lc.to_file( fc, geoJsonFile_standardized )
#ll = lc.to_mongoDB_ReteAcuquedotti( geoJsonFile_standardized )
