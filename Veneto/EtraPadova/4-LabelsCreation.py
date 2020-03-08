import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import logging,pandas as pd,numpy as np
import acqua.aqueduct as aq
idGestore = 'EtraPadova'
aq.setEnv('Veneto//'+idGestore)
##
reportFoundList = pd.read_csv('Definitions/ReportFoundList.csv')
useThisDictionary = parm.crea_dizionario('Definitions/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Definitions/SynParametri.csv')
ll = []
for i,reportFound in reportFoundList.iterrows():
    alias = (reportFound['alias_city'],reportFound['alias_address'])
    logging.info('>>> %s[%s]...',alias,i)
    #
    label = reportFound.reindex(parametersAdmitted).replace('-',np.nan).dropna().to_dict()
    data_report = reportFound['data_report']
    lb = al.create_label( useThisDictionary, idGestore, data_report, label )
    glb = al.addGeocodeData( lb, alias, 'Definitions/GeoReferencedLocationsList.csv' )
    ll.extend( glb )
##
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file( fc, idGestore+'.geojson' )
coll.display(fc)

