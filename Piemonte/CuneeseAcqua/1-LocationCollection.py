##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging,pandas as pd
import acqua.aqueduct as aq
gestore = "CuneeseAcqua"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.acda.it/analisi-delle-acque/'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
time.sleep(5)
selectComuniWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "id_comune" ) ) )
locations = selectComuniWebElement.find_elements_by_tag_name("option")
alias_city = [l.text for i,l in enumerate(locations) if i > 1 ]
driver.close()
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
