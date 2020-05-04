##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging,pandas as pd
import acqua.aqueduct as aq
import string
gestore = "HeraER"
aq.setEnv('EmiliaRomagna//'+gestore)
url = 'https://www.gruppohera.it/gruppo/attivita_servizi/business_acqua/canale_acqua/'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
#options.add_argument( '--headless' )
#
alias_city = []
digitList = list(string.ascii_lowercase[:26])
digitList = ['i','h']
for digit in digitList:
    driver = webdriver.Chrome( "chromedriver", options=options )
    driver.implicitly_wait( 10 )  # seconds
    driver.get( url )
    time.sleep( 5 )
    divWebElement = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_class_name( "form_scopricosabevi_campi" ) ) )
    inputWebElement = divWebElement.find_element_by_class_name("ui-autocomplete-input")
    inputWebElement.clear()
    inputWebElement.send_keys(digit)
    time.sleep(5)
    try:
        popUpWebElement = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_id( "ui-id-2" ) ) )
        loc = [l.text.strip() for l in popUpWebElement.find_elements_by_tag_name("li")]
        alias_city.extend(loc)
        logging.info("Processed '%s' found %s locations.",digit,len(loc))
    except:
        divWebElement = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_class_name( "form_scopricosabevi_campi" ) ) )
        inputWebElement = divWebElement.find_element_by_class_name( "ui-autocomplete-input" )
        city = inputWebElement.text
        if city != "":
            alias_city.extend([city])
        else:
            logging.critical("Not found address for '%s'",digit)

    driver.close()
##
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", Emilia Romagna"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
