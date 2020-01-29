##
import acqua.labelCollection as lc
import os
import logging
path = '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC/'
os.chdir(path)
geoJsonFile = 'CAFC.geojson'
ll = lc.to_mongoDB(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))

