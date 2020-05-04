##
from bs4 import BeautifulSoup
import requests,logging
import acqua.aqueduct as aq
import pandas as pd,re
import acqua.parametri as parm
gestore = "GestAcquaAlessandria"
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
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    page = requests.get(urlReport)
    soup = BeautifulSoup(page.text, 'html.parser')
    #data del report
    premessa = soup.body.findAll(text=re.compile('Periodo di riferimento:'))[0]
    data_report = re.search("\d\d/\d\d/\d\d\d\d", premessa).group()
    htmlTable = soup.find("table", { "class" : "eael-data-table" })
    table = pd.read_html( str( htmlTable ), decimal=',', thousands='.' )[0]
    table.set_index('Parametro*', inplace=True )
    parms = table.loc[parametersAdmitted]['Media']
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( "Hacked %s/%s (%s/%s)!", alias_city, alias_address, i + 1, len( reportFoundList ) )
##
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
