##
import pandas as pd,requests,io,pdfquery,warnings,logging
import acqua.aqueduct as aq
import acqua.parametri as parm
import pdfquery,io
warnings.simplefilter(action='ignore', category=FutureWarning)
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
urlReport = 'http://www.paviaacque.it/attivita/qualita-dellacqua/'
gestore = "PaviaAcque"
aq.setEnv('Lombardia//'+gestore)
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
##
def getDataReport(pdf,label,page):
    def clean_text(text):  return text.split(label)[1].strip()
    q = "LTPage[page_index='%s'] LTTextLineHorizontal:contains('%s')" %(page,label)
    textLine = pdf.pq(q)
    left_corner = float(textLine.attr('x0'))
    bottom_corner = float(textLine.attr('y0'))
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' %(page,left_corner, bottom_corner, left_corner+200, bottom_corner+10)
    text = pdf.pq(s).text()
    return clean_text(text)
#
def getLocation(pdf,label,page):
    def clean_text(text):  return text.split(label)[1].strip()
    q = "LTPage[page_index='%s'] LTTextLineHorizontal:contains('%s')" %(page,label)
    textLine = pdf.pq(q)
    left_corner = float(textLine.attr('x0'))
    bottom_corner = float(textLine.attr('y0'))
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' %(page,left_corner, bottom_corner-3, left_corner+300, bottom_corner+10)
    text = pdf.pq(s).text()
    return clean_text(text)
#
def getValueParm(pdf,label):
    import numpy as np
    q = "LTPage:contains('%s')" % (label)
    page = pdf.pq( q )
    page_index = page.attr( 'page_index' )
    if page_index is None: return np.nan
    q = "LTPage:contains('%s') LTTextLineHorizontal:contains('%s')" % (page_index, label)
    textLine = pdf.pq( q )
    bottom_corner = float( textLine.attr( 'y0' ) )
    s = 'LTPage[page_index="%s"] LTTextBoxHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (page_index, 230, bottom_corner, 280, bottom_corner + 10)
    text = pdf.pq( s ).text()
    return text
##
reportFoundList = pd.read_csv('Metadata/ReportFoundList.csv')
dataReportCollection = pd.DataFrame()
for i,report in reportFoundList.iterrows():
    #i=0
    #report = reportFoundList.loc[i]
    try:
        alias_city = report['alias_city']
        alias_address = report['alias_address']
        urlReport = report['urlReport']
        #
        file = io.BytesIO( requests.get( urlReport ).content )
        pdf = pdfquery.PDFQuery( file )
        pdf.load()
        data_report = getDataReport( pdf, 'Data Rapporto di Prova',0 )
        location = getLocation( pdf, 'Descrizione Camp.:',0 )
        parms = {p:getValueParm(pdf,p) for p in parametersAdmitted}
        stdParms = parm.standardize( useThisDictionary, parms)
        row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        row.update( stdParms )
        dataReportCollection = dataReportCollection.append( row, ignore_index=True )
        logging.info( 'Hacked %s/%s (%s/%s)', alias_city, alias_address, i, len( reportFoundList ) - 1 )
    except:
        logging.critical('Skiped %s/%s !',alias_city,alias_address)
##
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
