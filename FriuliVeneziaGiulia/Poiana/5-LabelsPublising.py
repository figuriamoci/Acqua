##
import acqua.labelCollection as lc
import os
import logging
path = '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/Poiana/'
os.chdir(path)
geoJsonFile = 'Poiana.geojson'
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))

