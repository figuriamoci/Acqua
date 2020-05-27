##
import pandas as pd
import acqua.aqueduct as aq,logging
import tabula,requests,io
import acqua.parametri as parm
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "AlpiAcqueCuneo"
aq.setEnv('Piemonte//'+gestore)
#Da cambiare di volta in volta dalla lista presente in http://www.alpiacque.it/Sportello-utenti
fileReport = 'Datasource/'+ 'Statistiche+analisi+acque+potabili+-+Riepilogo+tutti+i+comuni+media+anno+2019+pubblicato+2020-2.pdf'
data_report = '24/01/2020'
urlReport = 'http://www.alpiacque.it/DesktopModules/ArtmediaFileManager/downloadBlob.ashx?UID=6D17B708-832C-4BCF-92F0-CC85C56DCE72'
file = io.BytesIO( requests.get( urlReport ).content )
table = tabula.read_pdf(io.BytesIO( requests.get( urlReport ).content ),stream=True)
table.set_index(table.columns[0],inplace=True)
#
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
cols = ['durezza','ph','conducibilita','residuo_fisso','sodio','potassio','calcio','magnesio','solfato','ammoniaca','nitrito','nitrato']
table.columns = cols
#
locationList = pd.read_csv('Metadata/LocationList.csv')
dataReportCollection = pd.DataFrame()
for i,location in locationList.iterrows():
    #i=0
    #location = locationList.loc[i]
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    parms = table.loc[alias_city]
    #
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( 'Hacked %s/%s (%s/%s)', alias_city, alias_address, i, len( locationList ) - 1 )
#
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
