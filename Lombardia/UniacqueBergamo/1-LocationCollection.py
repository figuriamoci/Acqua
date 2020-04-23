##
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging,pandas as pd
import acqua.aqueduct as aq
gestore = "UniacqueBergamo"
aq.setEnv('Lombardia//'+gestore)
url = "https://www.uniacque.bg.it/qualita-dellacqua/i-parametri-del-tuo-comune/"
#
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
time.sleep(2)
#
selectHtml = driver.find_element_by_name('comuneId')
comuniWebElementList = selectHtml.find_elements_by_tag_name("option")
comuniList = [comune.text for i,comune in enumerate(comuniWebElementList) if i>0]
##
addressList = []
selectComuni = Select(selectHtml)
for i,comune in enumerate(comuniList):
    driver.get( url )
    #time.sleep(1)
    WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_tag_name( "comuneId" ) ) )
    selectComuni = Select(driver.find_element_by_name('comuneId'))
    selectComuni.select_by_visible_text(comune)
    WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_css_selector( "#page-complete > div > form > input[type=submit]" ) ) )
    submit = driver.find_element_by_css_selector("#page-complete > div > form > input[type=submit]")
    submit.send_keys(Keys.ENTER)
    #
    time.sleep(2)
    locationList = pd.DataFrame()
    WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_css_selector( "#page-complete > div > form > label > select" ) ) )
    indirizzoHtml = driver.find_element_by_css_selector("#page-complete > div > form > label > select")
    WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_tag_name( "option"") ) )

    indirizziWebElementList = indirizzoHtml.find_elements_by_tag_name("option")
    for indirizzo in indirizziWebElementList:
        row = {'alias_city': comune, 'alias_address': indirizzo.text}
        addressList.append( row )
    logging.info("Processed %s (%s/%s)",comune,i+1,len(comuniList))
##
driver.close()
locationList = pd.DataFrame(addressList)
locationList['georeferencingString'] = locationList['alias_address'].str.replace("FONTANELLA","").str.strip()+", "+locationList['alias_city']+", Bergamo, Lombardia, Italia"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)


