##
import acqua.labelCollection as lc
import os
import logging
path = '/Users/andrea/PycharmProjects/Acqua/Veneto/Lta/'
os.chdir(path)
geoJsonFile = 'Lta.geojson'
ll = lc.to_mongoDB(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))
