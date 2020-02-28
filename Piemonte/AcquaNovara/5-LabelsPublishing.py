##
import acqua.labelCollection as lc,os,logging
#os.chdir('D://Python//Acqua')
os.chdir('//Users//andrea//PycharmProjects//Acqua')
os.chdir('Piemonte//AcquaNovara')
geoJsonFile = 'AcquaNovara.geojson'
ll = lc.removeEtichette('AcquaNovara')
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))
