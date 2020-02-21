##
import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import os,logging,pandas as pd

os.chdir('/Users/andrea/PycharmProjects/Acqua/Lombardia/GruppoCAP')
logging.basicConfig(level=logging.DEBUG)
idGestore = 14177 ##CAP HOLDING S.P.A,
useThisDictionary = parm.crea_dizionario('Definitions/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Definitions/SynParametri.csv')

df = pd.read_csv('Source/Medie ponderate comuni 2018.csv',sep=';',keep_default_na=False,thousands='.',decimal=',')
reportFound = df[1:]
reportFound.set_index('Comune',inplace=True)

aliasCityList = list(reportFound.index)
ll = []
##
for i,alias_city in enumerate(aliasCityList):
    alias_address = 'Territorio comunale'
    alias = (alias_city,alias_address)

    report = reportFound.loc[alias_city,parametersAdmitted]
    label = report.to_dict()
    data_report = 'Medie ponderate 2018'
    lb = al.create_label( useThisDictionary, idGestore, data_report, label )
    glb = al.addGeocodeData( lb, alias, 'Definitions/GeoReferencedLocationsList.csv' )
    ll.extend( glb )
##
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file( fc, 'GruppoCAP.geojson' )
coll.display(fc)


##

