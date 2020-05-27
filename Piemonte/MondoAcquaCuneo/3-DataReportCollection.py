##
import tabula,requests,io
import pandas as pd,requests
import acqua.aqueduct as aq,logging
import PyPDF2 as py,pdfquery
import acqua.parametri as parm
import numpy as np
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "MondoAcquaCuneo"
aq.setEnv('Piemonte//'+gestore)
#Da cambiare di volta in volta dalla lista presente in http://www.alpiacque.it/Sportello-utenti
urlReport = 'https://www.mondoacqua.com/wp/wp-content/uploads/2019/11/H2O-POTABILI_per-SITO-WEB-1.pdf'
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
#
def getDataReport(pdf,label,page):
    def clean_text(text):  return text.split(label)[1].strip()
    q = "LTPage[page_index='%s'] LTTextLineHorizontal:contains('%s')" %(page,label)
    textLine = pdf.pq(q)
    left_corner = float(textLine.attr('x0'))
    bottom_corner = float(textLine.attr('y0'))
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' %(page,left_corner, bottom_corner, left_corner+400, bottom_corner+20)
    text = pdf.pq(s).text()
    return clean_text(text)
#
mypdf = py.PdfFileReader(io.BytesIO( requests.get( urlReport ).content ))
nPage = mypdf.getNumPages()
alias_city = []
dataReportCollection = pd.DataFrame()
for page in range(0,nPage,1):
    #page=1
    file = io.BytesIO( requests.get( urlReport ).content )
    pdf = pdfquery.PDFQuery( file )
    pdf.load()
    data_report = getDataReport(pdf,'Periodo di riferimento:',page)
    #
    table = tabula.read_pdf( io.BytesIO( requests.get( urlReport ).content ), lattice=True, multiple_tables=True, pages=page )[0]
    alias_city = table.iloc[0,0]
    alias_address = 'Comune'
    table.set_index(table.columns[0],inplace=True)
    parms = table.loc[parametersAdmitted].iloc[:,1]
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( "Hacked %s/%s (%s/%s)!", alias_city, alias_address, page, nPage )
##
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)