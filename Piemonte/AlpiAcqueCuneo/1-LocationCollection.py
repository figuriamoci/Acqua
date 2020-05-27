import tabula,requests,io
import pandas as pd,requests
import acqua.aqueduct as aq,logging
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "AlpiAcqueCuneo"
aq.setEnv('Piemonte//'+gestore)
#Da cambiare di volta in volta dalla lista presente in http://www.alpiacque.it/Sportello-utenti
urlReport = 'http://www.alpiacque.it/DesktopModules/ArtmediaFileManager/downloadBlob.ashx?UID=6D17B708-832C-4BCF-92F0-CC85C56DCE72'
file = io.BytesIO( requests.get( urlReport ).content )
table = tabula.read_pdf( file )
alias_city = list(table.iloc[:,0])
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", CN, Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
