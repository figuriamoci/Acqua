##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging,pandas as pd
import acqua.aqueduct as aq
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
#
selectComuneWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_name( "ddl-acquedotto" ) ) )
elencoComuni_ = selectComuneWebElement.text.split("\n")
elencoComuni = [c.strip() for i,c in enumerate(elencoComuni_) if i > 0 and c.strip()!=""]
#
alias_city = []
alias_address = []
for i,comune in enumerate(elencoComuni):
    selectComuneWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_name( "ddl-acquedotto" ) ) )
    selectComune = Select(selectComuneWebElement)
    selectComune.select_by_visible_text(comune)
    time.sleep(1)
    selectPPWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_name( "ddl-pdp" ) ) )
    elencoPP_ = selectPPWebElement.text.split("\n")
    elencoPP = [c.strip() for i,c in enumerate(elencoPP_) if i > 0 and c.strip()!=""]
    elencoCity = [comune for pp in elencoPP]
    alias_city.extend(elencoCity)
    alias_address.extend(elencoPP)
    logging.info( "Retrived %s (%s,%s)", comune, i +1, len( elencoComuni ) )

##
driver.close()
locationList = pd.DataFrame({'alias_city':alias_city, 'alias_address':alias_address})
locationList['georeferencingString'] = locationList['alias_address'].str.replace('F.P. - ','')+", "+locationList['alias_city']+", Lombardia"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
