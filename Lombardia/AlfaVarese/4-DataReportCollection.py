##
import logging
import pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
import warnings
import numpy as np
import pdfquery, io, requests
import pdfminer

warnings.simplefilter( action='ignore', category=FutureWarning )
gestore = "AlfaVarese"
aq.setEnv( 'Lombardia//' + gestore )
parametersAdmitted = parm.getParametersAdmitted( 'Metadata/SynParametri.csv' )
useThisDictionary = parm.crea_dizionario( 'Metadata/SynParametri.csv' )
dataReportCollection = pd.DataFrame()
reportFoundList = pd.read_csv( 'Metadata/ReportFoundList.csv' )


def getData(pdf, label, page):
    def clean_text(text):  return text.replace( label, '' ).strip()

    q = "LTPage[page_index='%s'] LTTextLineHorizontal:contains('%s')" % (page, label)
    textLine = pdf.pq( q )
    left_corner = float( textLine.attr( 'x0' ) )
    bottom_corner = float( textLine.attr( 'y0' ) )
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (
    page, left_corner, bottom_corner, left_corner + 400, bottom_corner + 20)
    text = pdf.pq( s ).text()
    return clean_text( text )


def getValueParm(pdf, label):
    import numpy as np
    def clean_text(text): return text.split()[0].strip() if text != "" else np.nan
    q = "LTPage:contains('%s')" % (label)
    page = pdf.pq( q )
    page_index = page.attr( 'page_index' )
    if page_index is None: return np.nan
    q = "LTPage:contains('%s') LTTextLineHorizontal:contains('%s')" % (page_index, label)
    textLine = pdf.pq( q )
    bottom_corner = float( textLine.attr( 'y0' ) )
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (
    page_index, 240, bottom_corner, 265, bottom_corner + 10)
    text = pdf.pq( s ).text()
    return clean_text( text )
#
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
for i, report in reportFoundList.iterrows():
    # i=0
    # report = reportFoundList.iloc[i]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    ##
    logging.info( "Processing %s/%s (%s/%s)...", alias_city, alias_address,i,len(reportFoundList) )
    try:
        file = io.BytesIO( requests.get( urlReport ).content )
        pdf = pdfquery.PDFQuery( file )
        pdf.load()
        parms_ = {k: getValueParm( pdf, k ) for k in parametersAdmitted}
        parms = {k: v for k, v in parms_.items() if v is not np.nan}
        stdParms = parm.standardize( useThisDictionary, parms )
        try:
            data_report = getData( pdf, 'Data di emissione:', 0 )
        except:
            data_report = getData( pdf, 'Data accettazione:', 0 )
        #
        row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        row.update( stdParms )
        dataReportCollection = dataReportCollection.append( row, ignore_index=True )
        logging.info( 'Hacked %s/%s!', alias_city, alias_address )
    except pdfminer.pdfparser.PDFSyntaxError:
        logging.critical( "PDF %s not readble. Skiped!", urlReport )
##
dataReportCollection = dataReportCollection.replace( 'n.r.', np.nan )
# dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv( 'Metadata/DataReportCollection.csv', index=False )
