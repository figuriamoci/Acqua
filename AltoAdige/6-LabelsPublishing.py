import acqua.labelCollection as lc
import os,logging
path = '/Users/andrea/PycharmProjects/Acqua/AltoAdige/'
os.chdir(path)
geoJsonFile = 'AltoAdige.geojson'
ll = lc.to_mongoDBInsert(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))
