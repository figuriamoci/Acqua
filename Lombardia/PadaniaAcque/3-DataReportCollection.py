##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging,pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
gestore = "PadaniaAcque"
aq.setEnv('Lombardia//'+gestore)
url = 'https://www.padania-acque.it/it-IT/analisi-on-line.aspx'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 20 )  # seconds
driver.get( url )
time.sleep(5)
##
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
locationList = pd.read_csv('Metadata/LocationList.csv')
dataReportCollection = pd.DataFrame()
for i,location in locationList.iterrows():
    #i=0
    #location = locationList.iloc[i]
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    selectComuneWebElement = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_name( "ddl-acquedotto" ) ) )
    selectComune = Select( selectComuneWebElement )
    selectComune.select_by_visible_text( alias_city )
    #
    selectPPWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_name( "ddl-pdp" ) ) )
    selectPP = Select( selectPPWebElement )
    selectPP.select_by_visible_text( alias_address )
    #
    divTable = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_class_name( "fixed-table-body" ) ) )
    rawTable = driver.find_element_by_class_name("table")
    tableHtml = rawTable.get_attribute( 'outerHTML' )
    table = pd.read_html( tableHtml, decimal=',', thousands='.' )[0]
    table.set_index( ['Parametro'], inplace=True )
    parms = table.loc[parametersAdmitted]['Valore']
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    #
    premessa = 'Dati aggiornati al'
    riferimento_data = driver.find_elements_by_xpath('//h5[contains(text(), "' + premessa + '")]')[0].text
    data_report = riferimento_data.split(premessa)[1]
    #
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( "Hacked %s/%s (%s/%s)!", alias_city,alias_address, i + 1, len( locationList ) )
##
driver.close()
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
