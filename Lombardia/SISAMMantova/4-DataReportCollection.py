##
import tabula,logging
import pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
import warnings
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)
gestore = "SISAMMantova"
aq.setEnv('Lombardia//'+gestore)
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
dataReportCollection = pd.DataFrame()
reportFoundList = pd.read_csv( 'Metadata/ReportFoundList.csv' )
for i,report in reportFoundList.iterrows():
    #i=1
    #report = reportFoundList.iloc[i]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    data_report = report['data_report']
    table_ = tabula.read_pdf(urlReport,stream=True,encoding='utf-8')
    table = table_[table_['INDIRIZZO DI FORNITURA'].notna()]
    table.set_index(table.columns[0],inplace=True)
    parms = table.loc[parametersAdmitted].iloc[:, 1]
    row = {'alias_city':alias_city,'alias_address':alias_address,'data_report':data_report}
    stdParms = parm.standardize(useThisDictionary,parms.to_dict())
    row.update(stdParms)
    dataReportCollection = dataReportCollection.append(row,ignore_index=True)
    logging.info('Hacked %s/%s (%s/%s)',alias_city,alias_address,i,len(reportFoundList)-1)
#
dataReportCollection = dataReportCollection.replace("\\",np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
##

