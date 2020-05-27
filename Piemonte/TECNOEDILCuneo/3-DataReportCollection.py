##
from bs4 import BeautifulSoup
import io,pdfquery,requests,tabula
import requests,logging
import acqua.aqueduct as aq
import pandas as pd
import acqua.parametri as parm
import numpy as np
logging.basicConfig(level=logging.INFO)
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "TECNOEDILCuneo"
aq.setEnv('Piemonte//'+gestore)
url = 'http://www.egea.it/idrico/ciclo-idrico-integrato/analisi-tecnoedil/'
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
#
def cityRectCoordinates():
    #leftUpperCorner
    q = "LTPage[page_index='0'] LTTextLineHorizontal:contains('%s')" % 'Comuni serviti dalla fonte'
    textLine = pdf.pq( q )
    leftCorner = float( textLine.attr( 'x1' ) )
    upperCorner = float( textLine.attr( 'y1' ) )+3 #Un po di tolleranza che non guasta
    #bottomRightCorner
    q = "LTPage[page_index='0'] LTTextLineHorizontal:contains('%s')" % 'Ente gestore'
    textLine = pdf.pq( q )
    rightCorner = 400
    bottomCorner = float( textLine.attr( 'y1' ) )
    return {'x0':leftCorner,'y0':upperCorner,'x1':rightCorner,'y1':bottomCorner}
#
def city_elements():
    rect = cityRectCoordinates()
    return float( this.get( 'y0', 0 ) ) >= rect['y1'] and float( this.get( 'y1', 0 ) ) <= rect['y0'] and float(
        this.get( 'x0', 0 ) ) >= rect['x0']
#
def getDataReport(pdf):
    label = 'Rapporto di prova N.'
    import numpy as np
    q = "LTPage:contains('%s')" % (label)
    page = pdf.pq( q )
    page_index = page.attr( 'page_index' )
    if page_index is None: return np.nan
    q = "LTPage:contains('%s') LTTextLineHorizontal:contains('%s')" % (page_index, label)
    textLine = pdf.pq( q )
    bottom_corner = float( textLine.attr( 'y0' ) )
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (page_index, 230, bottom_corner, 360, bottom_corner + 10)
    text = pdf.pq( s ).text()
    import re
    return re.search( "\d\d/\d\d/\d\d\d\d", text ).group()
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
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (page_index, 320, bottom_corner, 410, bottom_corner + 10)
    text = pdf.pq( s ).text()
    return text.strip()
##
webPage = requests.get( url )
soup = BeautifulSoup( webPage.text, 'html.parser' )
div = soup.find(id="coldx")
address = div.find_all('address')
urlReport = [a.find('a')['href'] for i,a in enumerate(address) if i>1 and a.text.strip() != '']
dataReportCollection = pd.DataFrame()
##
for i,report in enumerate(urlReport):
    #i=2
    #report = urlReport[i]
    file = io.BytesIO( requests.get( report ).content )
    pdf = pdfquery.PDFQuery( file )
    pdf.load()
    locations = pdf.pq( 'LTPage[page_index="0"] *' ).filter( city_elements )
    data_report = getDataReport(pdf)
    parms = {p:getValueParm(pdf,p) for p in parametersAdmitted}
    stdParms = parm.standardize( useThisDictionary, parms)
    for l in locations:
        alias_city = l.text.strip()
        alias_address = 'Comune'
        row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        row.update( stdParms )
        dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info('Found %s address for %s', len(locations),report)
##
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
