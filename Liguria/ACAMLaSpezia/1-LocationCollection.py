import tabula,io
import pandas as pd,requests
import PyPDF2 as py
import acqua.aqueduct as aq,logging
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "ACAMLaSpezia"
aq.setEnv('Liguria//'+gestore)
#Da cambiare di volta in volta dalla lista presente in https://www.acamspa.com/qualit%C3%A0-delle-acque-0
urlReport = 'https://www.acamacque.it/sites/default/files/allegati2019/Dati%20web%202019.pdf'
mypdf = py.PdfFileReader(io.BytesIO( requests.get( urlReport ).content ))
nPage = mypdf.getNumPages()
locationList = pd.DataFrame()
for p in range(0,nPage,1):
    table_ = tabula.read_pdf( io.BytesIO( requests.get( urlReport ).content ),pages=p)
    table = table_[table_['DATA PRELIEVO'].notnull()].copy()
    table.rename(columns={'COMUNE':'alias_city','LUOGO':'alias_address','DATA PRELIEVO':'data_report'},inplace=True)
    row = table[['alias_city','alias_address','data_report']]
    locationList = locationList.append(row,ignore_index=True)
    logging.info('Processed %s/%s',p,nPage)
#
locationList['georeferencingString'] = locationList['alias_address'].str.replace('Acquedotto','').str.strip()+', '+locationList['alias_city']+", SP, Liguria"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
