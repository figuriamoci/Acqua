##
import logging,datetime
import acqua.aqueduct as aq
import pandas as pd,re
import tabula
import acqua.parametri as parm
import numpy as np
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "SSISPAVercelli"
aq.setEnv('Piemonte//'+gestore)
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
reportFoundList = pd.read_csv('Metadata/ReportFoundList.csv')
dataReportCollection = pd.DataFrame()
##
for i,report in reportFoundList.iterrows():
    #i=1
    #report = reportFoundList.loc[i]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    table = tabula.read_pdf(urlReport)
    lastRow = table.shape[0]-1
    data_report = table.iloc[lastRow,0]
    parms = table[parametersAdmitted].loc[lastRow]
    stdParms = parm.standardize( useThisDictionary, parms)
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( "Hacked %s/%s (%s/%s) !", alias_city, alias_address, i, len( reportFoundList )-1 )
#
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
logging.info('End: %s',datetime.datetime.now())
