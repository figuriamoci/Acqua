##
import tabula,logging
import pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
from PyPDF2 import PdfFileReader
aq.setEnv('Veneto//GardesanaServizi')
useThisDictionary = parm.crea_dizionario('Medadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Medadata/SynParametri.csv')
dataReportCollection = pd.DataFrame()
reportFoundList = pd.read_csv( 'Medadata/ReportFoundList.csv' )
reportFoundList = reportFoundList.iloc[0:7]
for i,report in reportFoundList.iterrows():
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    logging.info( 'Reading %s...', urlReport )
    table = tabula.read_pdf(urlReport,pages='all',encoding='utf-8',multiple_tables=True)[0]
    table.set_index(table.columns[0],inplace=True)
    parms = table.reindex(parametersAdmitted).iloc[:,3]
    logging.info('Hacked %s',alias_city)
    #
    pdf = PdfFileReader(urlReport)
    text = pdf.getPage(0).extractText().split()
    data_report = [t for t in text if 'analisi' in t.lower()][0]
    #
    row = {'alias_city':alias_city,'alias_address':alias_address,'data_report':data_report}
    stdParms = parm.standardize(useThisDictionary,parms.to_dict())
    row.update(stdParms)
    dataReportCollection = dataReportCollection.append(row,ignore_index=True)
#
dataReportCollection.to_csv('Medadata/DataReportCollection.csv',index=False)

