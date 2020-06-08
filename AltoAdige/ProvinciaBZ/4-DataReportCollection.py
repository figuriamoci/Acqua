##
import acqua.parametri as parm
import pandas as pd
import numpy as np
import os,logging,datetime
import acqua.aqueduct as aq
#
gestore = "ProvinciaBZ"
aq.setEnv('AltoAdige//'+gestore)
logging.basicConfig(level=logging.DEBUG)
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
#
reportFoundList = pd.read_csv( 'Metadata/ReportFoundList.csv' )#
xls = pd.read_csv( 'ReportAnalisiAltoAdige.csv' )
df = xls.rename(columns={'Comune / Gemeinde':'alias_city','Punto di prelievo / Entnahmepunkt':'alias_address'})
df['data_report'] = pd.to_datetime(xls['Data prelievo / Entnahme Datum ']).dt.strftime('%d/%m/%Y')
df.set_index(['alias_city','alias_address','data_report'],inplace=True)
dataReportCollection = pd.DataFrame()
##
for i,rep in reportFoundList.iterrows():
    #i=0
    #rep = reportFoundList.loc[i]
    parms_ = df.loc[(rep[0],rep[1],rep[2]),parametersAdmitted]
    parms = pd.DataFrame(parms_.values,columns=parms_.columns)
    stdParms = parm.standardize( useThisDictionary, parms.loc[0].to_dict() )
    row = rep.to_dict()
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( 'Hacked %s/%s (%s/%s)', rep[0], rep[1], i, len( reportFoundList ) - 1 )
##
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
