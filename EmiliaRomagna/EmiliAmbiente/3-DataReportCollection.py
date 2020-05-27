##
import pandas as pd,requests,io,pdfquery,warnings,logging
import acqua.aqueduct as aq
import acqua.parametri as parm
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
urlReport = 'https://www.emiliambiente.it/files/uploads/Tabelle-composizione-acqua-per-sito_II-semestre-2019.pdf'
gestore = "EmiliAmbiente"
aq.setEnv('EmiliaRomagna//'+gestore)
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
#
def getSection(pdf,alias_city):
    p = "LTPage:contains('%s')" % (alias_city)
    textLine = pdf.pq( p )
    page_index = textLine.attr( 'page_index' )
    q = 'LTPage[page_index="%s"] LTTextLineHorizontal:contains("%s")' % (page_index, alias_city)
    textLine = pdf.pq( q )
    textLine.text()
    bottom_corner = float( textLine.attr( 'y0' ) )
    reportCoords = {'page_index':page_index,'y0': bottom_corner, 'y1': bottom_corner - 330}
    return reportCoords
#
def getValue(pdf,label,reportCoords):
    page_index = reportCoords['page_index']
    q = 'LTPage[page_index="%s"] LTTextLineHorizontal:contains("%s")' % (page_index, label)
    textLine = pdf.pq( q )
    elemValue = [t for t in textLine if float( t.get( 'y0', 0 ) ) <= reportCoords['y0'] and float( t.get( 'y0', 0 ) ) >= reportCoords['y1']][0]
    baseLine = float( elemValue.get( 'y0', 0 ) )
    s = 'LTPage[page_index="%s"] LTTextBoxHorizontal:in_bbox("%s, %s, %s, %s")' % ( page_index, 300, baseLine-3, 390, baseLine + 15)
    textLine = pdf.pq( s )
    value = textLine[0].text.strip()
    return value
#
def getDateReport(pdf,reportCoords):
    import re
    page_index = reportCoords['page_index']
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (
    page_index, 40, reportCoords['y0'] - 30, 150, reportCoords['y0'] - 3)
    textLine = pdf.pq( s )
    premessa = textLine.text()
    data_report = re.search( "\d\d/\d\d/\d\d\d\d", premessa ).group()
    return data_report
##
file = io.BytesIO( requests.get( urlReport ).content )
pdf = pdfquery.PDFQuery( file )
pdf.load()
locationList = pd.read_csv('Metadata/LocationList.csv')
dataReportCollection = pd.DataFrame()
for i,location in locationList.iterrows():
    #i=4
    #location = locationList.loc[i]
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    reportCoords = getSection(pdf,alias_city)
    parms = {p:getValue(pdf,p,reportCoords) for p in parametersAdmitted}
    stdParms = parm.standardize(useThisDictionary,parms)
    data_report = getDateReport(pdf,reportCoords)
    row = {'alias_city':alias_city,'alias_address':alias_address,'data_report':data_report}
    row.update(stdParms)
    dataReportCollection = dataReportCollection.append(row,ignore_index=True)
    logging.info('Hacked %s/%s (%s/%s)',alias_city,alias_address,i,len(locationList)-1)
##
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
