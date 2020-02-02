##
import acqua.labelCollection as lc
import os
import logging
path = '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/HydroGEA/'
os.chdir(path)
geoJsonFile = 'HydroGEA.geojson'
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))
