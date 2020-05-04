##
from bs4 import BeautifulSoup
import pandas as pd,logging,tabula
import acqua.aqueduct as aq
import acqua.parametri as parm
import io,pdfquery,requests
import numpy as np
logging.basicConfig(level=logging.INFO)
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "AMCASALE"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.amcasale.it/it/la-tua-acqua/composizione-analitica-dell-acqua.html'
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
#urlReport è ricavato dalla pagina in url.
urlReport = 'https://www.amcasale.it/admin/public/pagina/c1cd6764b2ad41ffbef5ef902b603ae3/Composizione_Analitica_Acqua_II_Semestre_2019.pdf'
locationList = pd.read_csv('Metadata/LocationList.csv')
location = list(locationList['alias_city'])
#
def getText(pdf,label,page):
    def clean_text(text):  return text.replace(label,'').strip()
    q = "LTPage[page_index='%s'] LTTextLineHorizontal:contains('%s')" %(page,label)
    textLine = pdf.pq(q)
    left_corner = float(textLine.attr('x0'))
    bottom_corner = float(textLine.attr('y0'))
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' %(page,left_corner, bottom_corner, left_corner+400, bottom_corner+20)
    text = pdf.pq(s).text()
    return clean_text(text)
#
file = io.BytesIO( requests.get( urlReport ).content )
pdf = pdfquery.PDFQuery( file )
pdf.load()
data_report = getText( pdf, 'Periodo di riferimento :', 0 )
#
rawTable = tabula.read_pdf( urlReport, lattice=True, encoding='utf-8', multiple_tables=True )[0]
rawTable.set_index( rawTable.columns[0], inplace=True )
table = rawTable.loc[parametersAdmitted].T
index = ['UM','LM'] #Sono le prime due righe di table
index.extend(location) #Aggiungiamo le località presenti nella Location List.
#dato che cols saranno le colonne di table vediamo se numericamente sono coerenti
#
if len(index) != len(table.index):
    raise Exception("Tabella non coerente con le colonne previste di seguito",cols)
else:
    table.index = index
#
dataReportCollection = pd.DataFrame()
for i,location in locationList.iterrows():
    #i=0
    #location = locationList.loc[i]
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    parms = table.loc[alias_city].to_dict()
    stdParms = parm.standardize( useThisDictionary, parms)
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( "Hacked %s/%s (%s/%s)!", alias_city, alias_address, i + 1, len( locationList ) )
#
dataReportCollection = dataReportCollection.replace('-',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)

