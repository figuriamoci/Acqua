##
import requests,logging,datetime
import acqua.aqueduct as aq
import pandas as pd,re
import pdfquery,io
import acqua.parametri as parm
import numpy as np
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "SISIAcqueAlba"
aq.setEnv('Piemonte//'+gestore)
#
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
reportFoundList = pd.read_csv('Metadata/ReportFoundList.csv')
dataReportCollection = pd.DataFrame()
##
def getValueParm(pdf,label):
    import numpy as np
    q = "LTPage:contains('%s')" % (label)
    page = pdf.pq( q )
    page_index = page.attr( 'page_index' )
    if page_index is None: return np.nan
    q = "LTPage:contains('%s') LTTextLineHorizontal:contains('%s')" % (page_index, label)
    textLine = pdf.pq( q )
    bottom_corner = float( textLine.attr( 'y0' ) )
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (page_index, 310, bottom_corner, 410, bottom_corner + 10)
    text = pdf.pq( s ).text()
    return text.split()[0].strip()
#
def getDataReport(pdf,label):
    import numpy as np
    q = "LTPage:contains('%s')" % (label)
    page = pdf.pq( q )
    page_index = page.attr( 'page_index' )
    if page_index is None: return np.nan
    q = "LTPage:contains('%s') LTTextLineHorizontal:contains('%s')" % (page_index, label)
    textLine = pdf.pq( q )
    bottom_corner = float( textLine.attr( 'y0' ) )
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (page_index, 200, bottom_corner, 400, bottom_corner + 10)
    text = pdf.pq( s ).text()
    return text.split(label)[1].strip()
##
logging.info('Start: %s',datetime.datetime.now())
for i,report in reportFoundList.iterrows():
    #i=0
    #report = reportFoundList.loc[i]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    ##
    file = io.BytesIO( requests.get( urlReport ).content )
    pdf = pdfquery.PDFQuery( file )
    pdf.load()
    parms = {p:getValueParm(pdf,p) for p in parametersAdmitted}
    stdParms = parm.standardize( useThisDictionary, parms)
    data_report = getDataReport(pdf,'Data prelievo:')
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( "Hacked %s/%s (%s/%s) !", alias_city, alias_address, i + 1, len( reportFoundList ))
##
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
logging.info('End: %s',datetime.datetime.now())