##%%
import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import os,logging,pickle
#os.chdir('D://Python//Acqua')
os.chdir('//Users//andrea//PycharmProjects//Acqua')
os.chdir('Lombardia//AcquaLodigiana')
logging.basicConfig(level=logging.DEBUG)
idGestore = 'AcquaLodigiana'
useThisDictionary = parm.crea_dizionario('Medadata/SynParametri.csv')
with open( 'Metadata/ReportListFound.pickle', 'rb' ) as f: foundReportList = pickle.load( f )
#%%
parametersAdmitted = parm.getParametersAdmitted('Medadata/SynParametri.csv')
ll = []
for alias,report in foundReportList.items():
    data_report = report['data_report']
    parameters = report['parameters']
    label = {k:v for k,v in parameters.items() if k in parametersAdmitted}
    lb = al.create_label(useThisDictionary,idGestore, data_report, label )
    glb = al.addGeocodeData( lb, alias, 'Medadata/GeoReferencedLocationsList.csv' )
    ll.extend( glb )
##
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file( fc, 'AcquaLodigiana.geojson' )
coll.display(fc)

