###
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import acqua.aqueduct as aq
gestore = "ASMVercelli"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.asmvercelli.it/Idrico/Qualita-e-tariffe/Livelli-di-qualita.html'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
selectComuniWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "city" ) ) )
optionsWebElement = selectComuniWebElement.find_elements_by_tag_name('option')
alias_city = [o.text for i,o in enumerate(optionsWebElement) if i>0]
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", Vercelli, Piemonte"
locationList['type'] = 'POINT'
#locationList.to_csv('Metadata/LocationList.csv',index=False)

import acqua.aqueduct as aq