##
import acqua.labelCollection as lc
import os,logging
path = '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/IRISAcque/'
os.chdir(path)
geoJsonFile = 'IRISAcque.geojson'
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))

