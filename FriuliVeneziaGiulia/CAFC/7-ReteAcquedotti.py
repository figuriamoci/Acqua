import acqua.labelCollection as lc
import os
import logging
path = '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC/'
os.chdir(path)
geoJsonFile = 'Definitions/ConfiniComuniFVG.geojson'
ll = lc.to_mongoDB_ReteAcuquedotti(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))

