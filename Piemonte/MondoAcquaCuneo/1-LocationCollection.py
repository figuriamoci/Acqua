##
import tabula,requests,io
import pandas as pd,requests
import acqua.aqueduct as aq,logging
import PyPDF2 as py
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "MondoAcquaCuneo"
aq.setEnv('Piemonte//'+gestore)
#Da cambiare di volta in volta dalla lista presente in http://www.alpiacque.it/Sportello-utenti
urlReport = 'https://www.mondoacqua.com/wp/wp-content/uploads/2019/11/H2O-POTABILI_per-SITO-WEB-1.pdf'
#
mypdf = py.PdfFileReader(io.BytesIO( requests.get( urlReport ).content ))
nPage = mypdf.getNumPages()
alias_city = []
for page in range(0,nPage,1):
    #page=0
    table = tabula.read_pdf( io.BytesIO( requests.get( urlReport ).content ), lattice=True, multiple_tables=True, pages=page )[0]
    lacation = table.iloc[0,0]
    alias_city.append(lacation)
#
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city'].str.replace('\n','')+", CN, Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
