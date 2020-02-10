import acqua.labelCollection as lc
import os
import logging
path = '/Users/andrea/PycharmProjects/Acqua/AltoAdige/'
os.chdir(path)
geoJsonFile = 'confini_comuni_alto_adige.geojson'
ll = lc.to_mongoDB_ReteAcuquedotti(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))

