##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging,pandas as pd
import acqua.aqueduct as aq
gestore = "AlfaVarese"
aq.setEnv('Lombardia//'+gestore)
#
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
url = "https://www.alfasii.it/la-societa/servizi/acquedotto.html"
driver.get( url )
time.sleep(5)
##
listWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "sl_sidebar" ) ) )
locations_ = listWebElement.text.split("\n")
locationList = pd.DataFrame()
for i in range(0,len(locations_),2):
    row = {'alias_city':locations_[i],'alias_address':locations_[i+1]}
    locationList = locationList.append( row, ignore_index=True )
##
driver.close()
locationList['georeferencingString'] = locationList['alias_address']+", "+locationList['alias_city']+", Lombardia"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)


