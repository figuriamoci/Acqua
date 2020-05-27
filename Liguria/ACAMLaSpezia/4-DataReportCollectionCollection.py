##
import tabula,io,numpy as np
import pandas as pd,requests
import acqua.aqueduct as aq,logging
import PyPDF2 as py
import acqua.parametri as parm
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "ACAMLaSpezia"
aq.setEnv('Liguria//'+gestore)
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
#Da cambiare di volta in volta dalla lista presente in https://www.acamspa.com/qualit%C3%A0-delle-acque-0
urlReport = 'https://www.acamacque.it/sites/default/files/allegati2019/Dati%20web%202019.pdf'
mypdf = py.PdfFileReader(io.BytesIO( requests.get( urlReport ).content ))
nPage = mypdf.getNumPages()
dataReport = pd.DataFrame()
for p in range(0,nPage,1):
    table = tabula.read_pdf( io.BytesIO( requests.get( urlReport ).content ),pages=p)
    for i in range(0,table.shape[0],1):
        if pd.notna(table.iloc[i]['DATA PRELIEVO']): data_report = table.iloc[i]['DATA PRELIEVO']
        row = {'data_report': data_report}
        row.update(table.iloc[i,:])
        dataReport = dataReport.append(row,ignore_index=True)
    logging.info('Processed %s on %s',p,nPage)
#
dataReport.rename(columns={'COMUNE':'alias_city','LUOGO':'alias_address'},inplace=True)
dataReport.set_index(['alias_city','alias_address','data_report'],inplace=True)
##
locationList = pd.read_csv('Metadata/LocationListReviewed.csv')
dataReportCollection = pd.DataFrame()
for i,location in locationList.iterrows():
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    data_report = location['data_report']
    a = dataReport.loc[alias_city,alias_address,data_report]
    parms = dict(list(zip(a['PARAMETRO'],a['VALORE'])))
    stdParms = parm.standardize( useThisDictionary, parms)
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update(stdParms)
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( 'Processed %s on %s', i, len(locationList) )
##
dataReportCollection = dataReportCollection.replace('N.D.',np.nan)
dataReportCollection = dataReportCollection.replace('U.V.',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
