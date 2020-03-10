import acqua.labelCollection as lc,logging
import acqua.aqueduct as aq
idGestore = "AcqueVeronesi"
aq.setEnv('Veneto//'+idGestore)

geoJsonFile = idGestore+'.geojson'
ll = lc.removeEtichette(idGestore)
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))
