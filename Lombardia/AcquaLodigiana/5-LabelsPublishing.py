##
import acqua.labelCollection as lc,os,logging
#os.chdir('D://Python//Acqua')
os.chdir('//Users//andrea//PycharmProjects//Acqua')
os.chdir('Lombardia//AcquaLodigiana')
geoJsonFile = 'AcquaLodigiana.geojson'
ll = lc.removeEtichette('AcquaLodigiana')
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))
