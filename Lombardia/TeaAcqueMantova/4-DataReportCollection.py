##
from bs4 import BeautifulSoup
import pandas as pd,requests,io
import acqua.aqueduct as aq
import acqua.parametri as parm
import logging,re
gestore = "TeaAcqueMantova"
aq.setEnv('Lombardia//'+gestore)
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
reportFoundList = pd.read_csv("Metadata/ReportFoundList.csv")
dataReportCollection = pd.DataFrame()
#
for i,report in reportFoundList.iterrows():
    #i=2
    #report=reportFoundList.iloc[i]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    #
    page = requests.get(urlReport)
    soup = BeautifulSoup(page.text, 'html5lib')
    #
    rawTable = soup.findAll("table", {"frame": "VOID"})
    table = pd.read_html( str( rawTable ), decimal=',', thousands='.', index_col=0, header=0 )[0]
    parms = table.loc[parametersAdmitted].iloc[:, 0]
    #
    data_report = soup.findAll("p", text=re.compile('Dati aggiornati al'))[0].get_text()
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    #
    logging.info( 'Hacked %s/%s (%s/%s)', alias_city, alias_address, i, len( reportFoundList ) - 1 )
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
##
#dataReportCollection = dataReportCollection.replace('-',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
