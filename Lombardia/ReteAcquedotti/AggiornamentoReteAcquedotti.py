##
import os, geojson, logging, acqua.labelCollection as lc

def create_water_supply_network(geoJsonfile, regione):
    #logging.info( "reading %s from %s...", geoJsonfile, regione )
    with open( geoJsonfile ) as f:
        geo = geojson.load( f )
    fc = []
    for f in geo['features']:
        logging.info(f)
        if f['geometry']['type'] == 'Point':
            logging.info('Skip %s',f)
        else:
            name = f['properties']['Name']
            new_properties = {'name': name, 'regione': regione}
            f['properties'] = new_properties
            fc.append( f )

    feature_collection = geojson.FeatureCollection( fc )
    logging.info( "Collected %s feature(s).", len( fc ) )
    return feature_collection

os.chdir( '/Users/andrea/PycharmProjects/Acqua/Lombardia/ReteAcquedotti' )

geoJsonFile = 'ComuniLombardia.geojson'
geoJsonFile_standardized = 'rete_acquedotti_lombardia(escl_Milano).geojson'
regione = 'Lombardia'
##
fc = create_water_supply_network( geoJsonFile,regione)
lc.to_file( fc, geoJsonFile_standardized )
ll = lc.to_mongoDB_ReteAcuquedotti( geoJsonFile_standardized )
