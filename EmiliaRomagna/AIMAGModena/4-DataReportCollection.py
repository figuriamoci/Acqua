##
import pandas as pd,requests,io,pdfquery,warnings,logging
import acqua.aqueduct as aq
import acqua.parametri as parm
import tabula,pdfquery,io
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
urlReport = 'https://www.emiliambiente.it/files/uploads/Tabelle-composizione-acqua-per-sito_II-semestre-2019.pdf'
gestore = "AIMAGModena"
aq.setEnv('EmiliaRomagna//'+gestore)
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
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
##
reportFoundList = pd.read_csv('Metadata/ReportFoundList.csv')
dataReportCollection = pd.DataFrame()
for i,report in reportFoundList.iterrows():
    #i=0
    #report = reportFoundList.loc[i]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    #
    file = io.BytesIO( requests.get( urlReport ).content )
    pdf = pdfquery.PDFQuery( file )
    pdf.load()
    data_report = getDataReport( pdf, 'Periodo:',0 )
    #
    table = tabula.read_pdf(urlReport,encoding='utf-8')
    table.set_index( table.columns[0], inplace=True )
    parms = table.loc[parametersAdmitted].iloc[:, 3]
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( 'Hacked %s/%s (%s/%s)', alias_city, alias_address, i, len( reportFoundList ) - 1 )
##
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
