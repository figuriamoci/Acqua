##
import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import os,logging,pandas as pd,tabula

os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Veritas')
logging.basicConfig(level=logging.DEBUG)
idGestore = 'Veritas'
##
reportFoundList = pd.read_csv('Definitions/ReportFoundList.csv')
useThisDictionary = parm.crea_dizionario('Definitions/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Definitions/SynParametri.csv')
ll = []
for i,reportFound in reportFoundList.iterrows():
    #i=5
    #reportFound = reportFoundList.iloc[i]
    alias = (reportFound['alias_city'],reportFound['alias_address'])
    logging.info('>>> %s[%s]...',alias,i)
    table_ = tabula.read_pdf( reportFound['url_report'], stream=True, pages="all" )
    table_.rename(columns={'Unnamed: 0':'parametro'},inplace=True)
    table = table_.set_index('parametro').iloc[:,-1]
    parametersPresent = set(table.index).intersection(set(parametersAdmitted))
    table = table.loc[parametersPresent]
    label = table.to_dict()
    data_report = reportFound['data_report']
    lb = al.create_label( useThisDictionary, idGestore, data_report, label )
    glb = al.addGeocodeData( lb, alias, 'Definitions/GeoReferencedLocationsList.csv' )
    ll.extend( glb )
    logging.info( 'Done.' )
##
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file( fc, 'Veritas.geojson' )
coll.display(fc)

