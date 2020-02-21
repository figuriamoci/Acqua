##
import acqua.labelCollection as lc,os,logging
path = '/Users/andrea/PycharmProjects/Acqua/Lombardia/GruppoCAP/'
os.chdir(path)
geoJsonFile = 'GruppoCAP.geojson'
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))
