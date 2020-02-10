import acqua.labelCollection as lc
import os
import logging
path = '/Users/andrea/PycharmProjects/Acqua/Veneto/'
os.chdir(path)
geoJsonFile = 'confini_comunali_veneto.geojson
ll = lc.to_mongoDB_ReteAcuquedotti(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))

