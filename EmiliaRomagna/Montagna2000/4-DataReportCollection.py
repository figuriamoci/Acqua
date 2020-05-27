##
from bs4 import BeautifulSoup
from selenium import webdriver
import time,numpy as np
import logging,pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
gestore = "Montagna2000"
aq.setEnv('EmiliaRomagna//'+gestore)
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
url = 'https://www.montagna2000.com/servizio-idrico-integrato/analisi-acqua-online/'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
#options.add_argument( '--headless' )
##
reportFoundList = pd.read_csv('Metadata/ReportFoundList.csv')
dataReportCollection = pd.DataFrame()
for i,report in reportFoundList.iterrows():
    #i=2
    #location = reportFoundList.loc[i]
    alias_city = report['alias_city']
    alias_address = report['alias_address']
    urlReport = report['urlReport']
    driver = webdriver.Chrome( "chromedriver", options=options )
    driver.implicitly_wait( 10 )  # seconds
    driver.get( urlReport )
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    logging.info( 'Processing %s/%s (%s/%s).', alias_city, alias_address,i,len(reportFoundList))
    #
    premessa = soup.find("a", {"class":"date"})
    data_report = premessa.text
    #
    rawTable = soup.find("table")
    table = pd.read_html( str(rawTable), decimal='.', thousands=',' )[0]
    table.set_index( 'Desc. Campione', inplace=True )
    parms = table.loc[parametersAdmitted]['Valore']
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( 'Hacked %s/%s!', alias_city, alias_address )
    driver.close()
#
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)

