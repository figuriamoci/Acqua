##
import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import os,logging,pickle
#os.chdir('D://Python//Acqua')
os.chdir('//Users//andrea//PycharmProjects//Acqua')
os.chdir('Piemonte//SMATTorino')
logging.basicConfig(level=logging.DEBUG)
idGestore = 'SMATTorino'
useThisDictionary = parm.crea_dizionario('Definitions/SynParametri.csv')
with open('Definitions/FoundReportList.pickle', 'rb') as f: foundReportList = pickle.load(f)
##
parametersAdmitted = parm.getParametersAdmitted('Definitions/SynParametri.csv')
ll = []
for alias,report in foundReportList.items():
    #logging.info("Creating geolabel for %s..",alias)
    data_report = report['data_report']
    parameters = report['parameters']
    label = {k:v for k,v in parameters.items() if k in parametersAdmitted}
    lb = al.create_label(useThisDictionary,idGestore, data_report, label )
    glb = al.addGeocodeData( lb, alias, 'Definitions/GeoReferencedLocationsList.csv' )
    ##logging.info("Done.")
    ll.extend( glb )
##
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file( fc, 'SMATTorino.geojson' )
coll.display(fc)