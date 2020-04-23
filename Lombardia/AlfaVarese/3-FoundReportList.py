##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging,pandas as pd
import acqua.aqueduct as aq
gestore = "AlfaVarese"
aq.setEnv('Lombardia//'+gestore)
url = "https://www.alfasii.it/la-societa/servizi/acquedotto.html"
#
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
locationList = pd.read_csv("Metadata/LocationList.csv")
#locationList = locationList[0:10]
foundReportList = pd.DataFrame()
##
for i,loc in locationList.iterrows():
    driver = webdriver.Chrome( "chromedriver", options=options )
    driver.implicitly_wait( 10 )  # seconds
    driver.get( url )
    time.sleep( 5 )
    try:
        alias_city = loc['alias_city']
        alias_address = loc['alias_address']
        divWebElement = WebD riverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "sl_sidebar" ) ) )
        listWebElement = divWebElement.find_elements_by_tag_name("div")
        listWebElement[0].text.split("\n")
        cityWebElement = [c for c in listWebElement if c.text.split("\n")[0] == alias_city and c.text.split("\n")[1] == alias_address][0]
        driver.execute_script( "arguments[0].click();", cityWebElement )
        time.sleep(2)
        logging.info("Extract report for %s/%s (%s/%s)...",alias_city,alias_address,i+1,len(locationList))
        reportLinkWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_link_text("Scarica la tabella dei valori") ) )
        urlReport = reportLinkWebElement.get_attribute("href")
        row = {"alias_city":alias_city,"alias_address":alias_address,"urlReport":urlReport}
        foundReportList = foundReportList.append(row,ignore_index=True)
    except:
        logging.critical("Skip %s/%s",alias_city,alias_address)
    driver.close()
##
foundReportList.to_csv('Metadata/ReportFoundList.csv',index=False)


