##
from bs4 import BeautifulSoup
import requests,logging
import acqua.aqueduct as aq
import pandas as pd
import acqua.parametri as parm
import numpy as np
gestore = "CordarBiella"
aq.setEnv('Piemonte//'+gestore)
#
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
reportFoundList = pd.read_csv('Metadata/ReportFoundList.csv')
dataReportCollection = pd.DataFrame()
#
for i,report in reportFoundList.iterrows():
    #i=0
    #report = reportFoundList.loc[i]
    #alias_city = report['alias_city']
    #alias_address = report['alias_address']
    urlReport = report['urlReport']
    webPage = requests.get(urlReport)
    soup = BeautifulSoup(webPage.text, 'html.parser')
    ##
    htmlTableList = soup.find_all('table')
    propertiesTable = pd.read_html( str( htmlTableList[0]) )[0]
    properties = propertiesTable.set_index(0)
    alias_city = properties.loc['Acquedotto'][1]
    alias_address = properties.loc['Punto di prelievo'][1]
    data_report = properties.loc['Data Prelievo'][1]
    #
    tableHtml = pd.read_html( str( htmlTableList[1]), decimal='.', thousands=',' )[0]
    table = tableHtml.set_index(1)
    parms = table.loc[parametersAdmitted].iloc[:,1]
    parms = parms.str.replace('inferiore a','<')
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( "Hacked %s/%s (%s/%s)!", alias_city, alias_address, i + 1, len( reportFoundList ) )
##
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
