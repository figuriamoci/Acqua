##
import tabula,logging
import pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
import warnings,numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)
aq.setEnv('Veneto//AcegasApsAmga')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
dataReportCollection = pd.DataFrame()
reportFoundList = pd.read_csv( 'Metadata/ReportFoundList.csv' )
for i,report in reportFoundList.iterrows():
    #report = reportFoundList.iloc[0]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    logging.info( 'Reading %s ...', urlReport )
    table = tabula.read_pdf(urlReport,pages='all',encoding='utf-8',multiple_tables=True)[0]
    table.set_index(table.columns[0],inplace=True)
    parms = table.loc[parametersAdmitted].iloc[:, 1]
    data_report = report['data_report']
    logging.info('Hacked %s',alias_city)
    row = {'alias_city':alias_city,'alias_address':alias_address,'data_report':data_report}
    stdParms = parm.standardize(useThisDictionary,parms.to_dict())
    row.update(stdParms)
    dataReportCollection = dataReportCollection.append(row,ignore_index=True)
##
dataReportCollection = dataReportCollection.replace('---',np.nan).replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
