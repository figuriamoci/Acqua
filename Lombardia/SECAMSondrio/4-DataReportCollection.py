##
import tabula,logging
import pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
import warnings,numpy as np
import requests,io,pdfquery
warnings.simplefilter(action='ignore', category=FutureWarning)
id_gestore = "SECAMSondrio"
aq.setEnv('Lombardia//'+id_gestore)
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
dataReportCollection = pd.DataFrame()
reportFoundList = pd.read_csv( 'Metadata/ReportFoundList.csv' )
for i,report in reportFoundList.iterrows():
    #report = reportFoundList.iloc[2]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    table = tabula.read_pdf(urlReport,lattice=True,pages='all',encoding='utf-8',multiple_tables=True)[0]
    table.set_index(table.columns[0],inplace=True)
    parms = table.loc[parametersAdmitted].iloc[:, 1]
    #
    filePdf = io.BytesIO(requests.get(urlReport).content)
    pdf = pdfquery.PDFQuery(filePdf)
    pdf.load()
    data_report = pdf.pq('LTTextLineHorizontal:contains("Analisi effettuata il")').text()
    #
    logging.info('Hacked %s/%s (%s/%s)',alias_city,alias_address,i,len(reportFoundList)-1)
    row = {'alias_city':alias_city,'alias_address':alias_address,'data_report':data_report}
    stdParms = parm.standardize(useThisDictionary,parms.to_dict())
    row.update(stdParms)
    dataReportCollection = dataReportCollection.append(row,ignore_index=True)
##
#dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)