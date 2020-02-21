##
import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import os,logging,pickle

os.chdir('/Users/andrea/PycharmProjects/Acqua/Lombardia/Milano')
logging.basicConfig(level=logging.DEBUG)
idGestore = 13800 ##MM S.P.A.
useThisDictionary = parm.crea_dizionario('Definitions/SynParametri.csv')

with open('Definitions/FoundReportList.pkl', 'rb') as f: foundReportList = pickle.load(f)
##
parametersAdmitted = parm.getParametersAdmitted('Definitions/SynParametri.csv')
ll = []
for alias,report in foundReportList.items():
    parms_ = report['parameters'].set_index('Parametro')
    parms = parms_.loc[parametersAdmitted,'Campione']
    label = parms.to_dict()
    data_report = report['data_report']
    lb = al.create_label(useThisDictionary,idGestore, data_report, label )

    glb = al.addGeocodeData( lb, alias, 'Definitions/GeoReferencedLocationsList.csv' )
    ll.extend( glb )
##
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file( fc, 'Milano.geojson' )
coll.display(fc)

