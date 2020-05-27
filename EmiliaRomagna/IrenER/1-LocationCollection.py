##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging,pandas as pd
import acqua.aqueduct as aq
gestore = "IrenER"
aq.setEnv('EmiliaRomagna//'+gestore)
url = 'https://serviziweb.gruppoiren.it/QualitaAcqua/custom/VisualizzaAnalisi.aspx?codiceRegione=08'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
time.sleep(5)
elencoProvince = ['PR','PC','RE']
alias_city =[]
alias_address = []
alias_address_value = []
alias_province = []
for provincia in elencoProvince:
    selectProvinceWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "cmbProvincie" ) ) )
    Select(selectProvinceWebElement).select_by_value(provincia)
    time.sleep(1)
    #
    selectComuneWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_name( "cmbComuni" ) ) )
    elencoComuni_ = selectComuneWebElement.text.split("\n")
    elencoComuni = [c.strip() for i,c in enumerate(elencoComuni_) if i > 0 and c.strip()!=""]
    for i,comune in enumerate(elencoComuni):
        selectComuneWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_name( "cmbComuni" ) ) )
        Select(selectComuneWebElement).select_by_visible_text(comune)
        time.sleep(1)
        #
        selectZoneWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_name( "cmbZone" ) ) )
        elencoZone_ = selectZoneWebElement.find_elements_by_tag_name("option")
        elencoZone = [c.text.strip() for i,c in enumerate(elencoZone_) if i > 0 and c.text.strip()!=""]
        elencoValoriZone = [c.get_attribute("value") for i, c in enumerate( elencoZone_ ) if i > 0 and c.text.strip() != ""]
        #
        alias_address.extend(elencoZone)
        alias_address_value.extend(elencoValoriZone)
        alias_city.extend([comune for z in elencoZone])
        alias_province.extend( [provincia for z in elencoZone] )
        logging.info("Processed %s (%s) of %s address (%s/%s)",comune,provincia,len(elencoZone),i+1,len(elencoComuni))
##
driver.close()
locationList = pd.DataFrame({'alias_province':alias_province,'alias_city':alias_city, 'alias_address':alias_address, 'alias_address_value':alias_address_value})
locationList['georeferencingString'] = locationList['alias_address'].str.replace('E Tutte Le Altre Zone','').str.replace('Tutte Le Zone','').str.replace('S.','San')+", "+locationList['alias_city']+", "+locationList['alias_province']+", Emilia Romagna"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
