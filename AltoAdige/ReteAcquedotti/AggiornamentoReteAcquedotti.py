import os, geojson, logging, acqua.labelCollection as lc

def create_water_supply_network(geoJsonfile, regione):
    logging.info( "reading %s from %s...", geoJsonfile, regione )
    with open( geoJsonfile ) as f:
        geo = geojson.load( f )
    fc = []
    for f in geo['features']:
        if f['geometry']['type'] == 'Point':
            logging.info('Skip %s',f)
        else:
            nameIta = f['properties']['nome_com']
            nameAut = f['properties']['nome_ted']
            new_properties = {'name': nameIta + '/' + nameAut, 'regione': regione}
            f['properties'] = new_properties
            fc.append( f )

    feature_collection = geojson.FeatureCollection( fc )
    logging.info( "Collected %s feature(s).", len( fc ) )
    return feature_collection

os.chdir( '/Users/andrea/PycharmProjects/Acqua/AltoAdige/ReteAcquedotti' )

geoJsonFile = 'confini_comuni_alto_adige.geojson'
geoJsonFile_standardized = 'rete_acquedotti_alto_adige.geojson'
regione = 'Alto Adige'

fc = create_water_supply_network( geoJsonFile,regione)
lc.to_file( fc, geoJsonFile_standardized )
ll = lc.to_mongoDB_ReteAcuquedotti( 'rete_acquedotti_alto_adige.geojson' )
