##
import os
import geojson as gj
import  as py
import logging
path = '/Users/andrea/PycharmProjects/Acqua'
GEOJsonFile = 'FriuliVeneziaGiulia/HydroGEA/HydroGEA.geojson'
os.chdir(path)
logging.info(path)
logging.basicConfig(level=logging.INFO)
##
logging.info("Loading GEOJson file '%s'...done",GEOJsonFile)
with open(GEOJsonFile) as f:
    geojson = gj.load(f)
##
listFeature = geojson['features']
##
logging.info("Connecting to MongoDB...')
conn = py.MongoClient("mongodb+srv://Acqua:nato1968@principal-4g7w8.mongodb.net/test?retryWrites=true&w=majority")
db = conn.Acqua
logging.info("Done.')
collection = db.etichette
logging.info("Saving GeoJeson Features....')
collection.insert_many(listFeature)
logging.info("Done. Safe %s feature(s)',len(listFeature))




##

