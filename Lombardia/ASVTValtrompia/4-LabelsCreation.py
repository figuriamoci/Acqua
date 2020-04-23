##
import acqua.label as al
import acqua.labelCollection as coll
import logging,pandas as pd
import acqua.aqueduct as aq
import numpy as np
gestore = "ASVTValtrompia"
aq.setEnv('Lombardia//'+gestore)
dataReportCollection = pd.read_csv('Metadata/DataReportCollection.csv')
ll = []
for i,reportFound in dataReportCollection.iterrows():
    alias = (reportFound['alias_city'],reportFound['alias_address'])
    logging.info('>>> %s[%s]...',alias,i)
    #
    label = reportFound.dropna().to_dict()
    data_report = reportFound['data_report']
    lb = al.create_label( np.nan, gestore, data_report, label )
    glb = al.addGeocodeData( lb, alias, 'Metadata/GeoReferencedLocationsList.csv' )
    ll.extend( glb )
    logging.info( 'Done.' )
##
fc = coll.to_geojson(ll)
print(fc)
coll.to_file( fc, gestore+'.geojson' )
coll.display(fc)

