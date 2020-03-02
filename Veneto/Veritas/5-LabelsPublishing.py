import acqua.labelCollection as lc
import os,logging
path = '/Users/andrea/PycharmProjects/Acqua/Veneto/Veritas/'
os.chdir(path)
geoJsonFile = 'Veritas.geojson'
ll = lc.removeEtichette('Veritas')
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))
