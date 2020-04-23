import acqua.labelCollection as lc
import logging
import acqua.aqueduct as aq
idGestore = 'MM'
aq.setEnv('Lombardia//'+idGestore)
geoJsonFile = idGestore+'.geojson'
ll = lc.removeEtichette(idGestore)
ll = lc.to_mongoDBInsertMany(geoJsonFile)
logging.info("Safe %s record(s) to MongoDB.",len(ll))
