##
import acqua.labelCollection as lc
import os
import logging
path = '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/AceGasAmga/'
os.chdir(path)
geoJsonFile = 'AceGasAmga.geojson'
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))

