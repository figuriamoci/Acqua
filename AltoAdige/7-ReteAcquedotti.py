import os,geojson,logging,acqua.labelCollection as lc

def create_water_supply_network(geoJsonfile,regione):
    logging.info("reading %s from %s...",geoJsonfile,regione)
    regione = 'Alto Adige'
    with open(geoJsonfile) as f: geo = geojson.load(f)
    fc = []
    for f in geo['features']:
        if f['properties']['type']=='Point': break
        nameIta = f['properties']['nome_com']
        nameAut = f['properties']['nome_ted']
        prop = {'name':nameIta+'/'+nameAut, 'regione':regione}
        new_properties = {'properties':prop }
        f['properties'] = new_properties
        fc.append(f)
        
    feature_collection = geojson.FeatureCollection( fc )
    logging.info("Collected %s feature(s).",len(fc))
    return feature_collection

path = '/Users/andrea/PycharmProjects/Acqua/AltoAdige/'
os.chdir(path)

geoJsonFile = 'confini_comuni_alto_adige.geojson'
geoJsonFile_standardized = 'acquedotti_alto_adige.geojson'

fc = create_water_supply_network(geoJsonFile)
lc.to_file(fc,geoJsonFile_standardized)
ll = lc.to_mongoDB_ReteAcuquedotti(geoJsonFile_standardized)
