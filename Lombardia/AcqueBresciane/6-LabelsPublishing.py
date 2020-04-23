import acqua.labelCollection as lc
import logging
import acqua.aqueduct as aq
gestore = "AcqueBresciane"
aq.setEnv('Lombardia//'+gestore)
geoJsonFile = gestore+'.geojson'
ll = lc.removeEtichette(gestore)
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))
