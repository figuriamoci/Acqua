##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging,pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
gestore = "ASVTValtrompia"
aq.setEnv('Lombardia//'+gestore)
url = "https://qualitaacqua.asvt-spa.it/QualitaH2oWeb/"
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 20 )  # seconds
driver.get( url )
locationList = pd.read_csv("Metadata/ReviewedLocationList.csv")
time.sleep(10)
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
##
dataReportCollection = pd.DataFrame()
for i,location in locationList.iterrows():
    try:
        alias_city = location['alias_city']
        alias_address = location['alias_address']
        georeferencingString = location['georeferencingString']
        driver.get( url)
        time.sleep( 10 )
        logging.info( "Processing %s... (%s/%s)", georeferencingString, i + 1, len( locationList ) )
        input = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "autocomplete" ) ) )
        input.clear()
        input.send_keys( georeferencingString )
        input.send_keys( Keys.ENTER )
        time.sleep( 5 )
        #
        tableWebElement = driver.find_element_by_id("parameters")
        tableHtml = tableWebElement.get_attribute('outerHTML')
        table = pd.read_html(tableHtml,decimal=',',thousands='.')[0]
        table.set_index(['Parametro'],inplace=True)
        #
        parms = table.loc[parametersAdmitted]['Valore']
        data_report = table['Data ultimo aggiornamento'].iloc[0]
        #
        row = {'alias_city':alias_city,'alias_address':alias_address,'data_report':data_report}
        stdParms = parm.standardize(useThisDictionary,parms.to_dict())
        row.update(stdParms)
        dataReportCollection = dataReportCollection.append(row,ignore_index=True)
        logging.info("Hacked %s (%s/%s)!",georeferencingString,i+1,len(locationList))
    except:
        logging.critical("Skip %s.",georeferencingString)
#
driver.close()
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)


