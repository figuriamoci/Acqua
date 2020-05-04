##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging,pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
import numpy as np
gestore = "CuneeseAcqua"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.acda.it/analisi-delle-acque/'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
#
locationList = pd.read_csv('Metadata/LocationList.csv')
dataReportCollection = pd.DataFrame()
#locationList = locationList.iloc[27:30]
for i,location in locationList.iterrows():
    #i=0
    #location = locationList.iloc[i]
    driver = webdriver.Chrome( "chromedriver", options=options )
    driver.implicitly_wait( 10 )  # seconds
    driver.get( url )
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    selectComuniWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "id_comune" ) ) )
    Select(selectComuniWebElement).select_by_visible_text(alias_city)
    submitWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_css_selector( ".btn" ) ) )
    driver.execute_script("arguments[0].click();", submitWebElement)
    time.sleep(1)
    tableWebElement = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_class_name( "table-striped" ) ) )
    tableHtml = tableWebElement.get_attribute('outerHTML')
    tableHtml_ = tableHtml.replace('<thead>','').replace('</thead>','') #workaround: la tabella ha due thead e quindi sintatticamente errata e non leggibile
    table = pd.read_html(tableHtml_,decimal=',',thousands='.')[0]
    table.columns = table.loc[0]
    table.set_index( ['Parametro'], inplace=True )
    parms = table.loc[parametersAdmitted]['Valore rilevato']
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    data_report = driver.find_element_by_class_name("data_analisi").text
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( "Hacked %s/%s (%s/%s)!", alias_city, alias_address, i + 1, len( locationList ) )
    driver.close()
##
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection_ = dataReportCollection[dataReportCollection['data_report']!=""] #Esclude le righe vuote
dataReportCollection_.to_csv('Metadata/DataReportCollection.csv',index=False)
