##Prologo
import logging,pandas as pd,numpy as np
import acqua.aqueduct as aq
import warnings,tabula
import acqua.parametri as parm
gestore = "STETTrentinoEst"
aq.setEnv('Trentino//'+gestore)
warnings.simplefilter(action='ignore', category=FutureWarning)
#Caricamento dizionari
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
#
reportFoundList = pd.read_csv('Metadata/ReportFoundList.csv')
dataReportCollection = pd.DataFrame()
for i,loc in reportFoundList.iterrows():
    #i=1
    #loc = reportFoundList.iloc[i]
    alias_city = loc['alias_city']
    alias_address = loc['alias_address']
    urlReport = loc['urlReport']
    data_report = loc['data_report']
    #
    table = tabula.read_pdf( urlReport,multiple_tables=False,lattice=True,silent=True)
    #table.set_index(table.columns[0],inplace=True)
    parms = table.loc[parametersAdmitted].iloc[:,1]
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( 'Hacked %s/%s (%s/%s)', alias_city, alias_address, i, len( reportFoundList ) - 1 )
##
dataReportCollection = dataReportCollection.replace('-',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)