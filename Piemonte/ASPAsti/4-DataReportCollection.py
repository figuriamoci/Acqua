##
import tabula,logging
import pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
import warnings,io,pdfquery,requests
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "ASPAsti"
aq.setEnv('Piemonte//'+gestore)
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
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
dataReportCollection = pd.DataFrame()
reportFoundList = pd.read_csv( 'Metadata/ReportFoundList.csv' )
for i,report in reportFoundList.iterrows():
    #i=0
    #report = reportFoundList.iloc[0]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    table = tabula.read_pdf(urlReport,stream=True,encoding='utf-8',multiple_tables=True)[0]
    table.set_index(table.columns[0],inplace=True)
    parms = table.loc[parametersAdmitted].iloc[:, 1]
    ##
    file = io.BytesIO( requests.get( urlReport ).content )
    pdf = pdfquery.PDFQuery( file )
    pdf.load()
    data_report = getText( pdf, 'Periodo di riferimento:', 0 )
    #
    logging.info('Hacked %s/%s (%s/%s)',alias_city,alias_address,i,len(reportFoundList)-1)
    row = {'alias_city':alias_city,'alias_address':alias_address,'data_report':data_report}
    stdParms = parm.standardize(useThisDictionary,parms.to_dict())
    row.update(stdParms)
    dataReportCollection = dataReportCollection.append(row,ignore_index=True)
##
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)