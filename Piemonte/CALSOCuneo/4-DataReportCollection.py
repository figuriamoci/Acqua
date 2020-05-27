##
from bs4 import BeautifulSoup,re
import logging,numpy as np
import pandas as pd,requests
import acqua.aqueduct as aq
import acqua.parametri as parm
gestore = "CALSOCuneo"
aq.setEnv('Piemonte//'+gestore)
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
reportFoundList = pd.read_csv('Metadata/ReportFoundList.csv')
dataReportCollection = pd.DataFrame()
for i,report in reportFoundList.iterrows():
    #i=0
    #report = reportFoundList.loc[i]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    page = requests.get(urlReport)
    soup = BeautifulSoup(page.text, 'html.parser')
    premessa = soup.body.findAll( text=re.compile( 'data analisi: ' ) )[0]
    data_report = re.search("\d\d/\d\d/\d\d\d\d", premessa).group()
    htmlTable = soup.find( "table")
    table = pd.read_html( str( htmlTable ), decimal=',', thousands='.' )[0]
    table.set_index(0,inplace=True)
    parms = table.loc[parametersAdmitted].iloc[:,1]
    stdParms = parm.standardize( useThisDictionary, parms )
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( "Hacked %s/%s (%s/%s)", alias_city, alias_address,i+1,len(reportFoundList))
##
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
