##
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging,pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
import time
import numpy as np
gestore = "ASMVercelli"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.asmvercelli.it/Idrico/Qualita-e-tariffe/Livelli-di-qualita.html'
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
    #i=1
    #location = locationList.iloc[i]
    driver = webdriver.Chrome( "chromedriver", options=options )
    driver.implicitly_wait( 10 )  # seconds
    driver.get( url )
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    selectComuniWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "city" ) ) )
    Select(selectComuniWebElement).select_by_visible_text(alias_city)
    buttonWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "form" ) ) )
    button = buttonWebElement.find_elements_by_tag_name("button")[0]
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)
    try:
        monitoraggioAcque = driver.find_element_by_link_text("Monitoraggio acque")
        monitoraggioAcque.click()
        divWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "idr" ) ) )
        parametriWebElement = divWebElement.find_elements_by_class_name("row") #Putroppo non è una tabella ma una sequenza di <div> dove ogni riga è class="row"
        elementList = [p.text.split("\n") for p in parametriWebElement if p.text!=""]
        table = pd.DataFrame(elementList)
        table.set_index(0, inplace=True )
        parms = table.loc[parametersAdmitted][3]
        stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
        data_report = divWebElement.find_element_by_css_selector("#idr > h5").text.split("Ultima misurazione:")[1].strip()
        row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        row.update( stdParms )
        dataReportCollection = dataReportCollection.append( row, ignore_index=True )
        logging.info( "Hacked %s/%s (%s/%s)!", alias_city, alias_address, i + 1, len( locationList ) )
    except:
        logging.critical("Label not found for %s. Skipped!",alias_city)
    driver.close()
##
dataReportCollection = dataReportCollection.replace('None',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
