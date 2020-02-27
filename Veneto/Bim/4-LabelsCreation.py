##
import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import os,logging,pickle

os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Bim')
logging.basicConfig(level=logging.DEBUG)
idGestore = 692 ##BIM GESTIONE SERVIZI PUBBLICI SPA,
useThisDictionary = parm.crea_dizionario('Definitions/SynParametri.csv')

with open('Definitions/FoundReportList.pickle', 'rb') as f: foundReportList = pickle.load(f)

##
parametersAdmitted = parm.getParametersAdmitted('Definitions/SynParametri.csv')
ll = []
for alias,report in foundReportList.items():
    parms_ = report['parametri']
    parms = parms_.loc[parametersAdmitted,'Rilevamento']
    label = parms.to_dict()
    data_report = report['data_report']
    lb = al.create_label(useThisDictionary,idGestore, data_report, label )
    glb = al.addGeocodeData( lb, alias, 'Definitions/GeoReferencedLocationsList.csv' )
    ll.extend( glb )
##
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file( fc, 'Bim.geojson' )
coll.display(fc)

