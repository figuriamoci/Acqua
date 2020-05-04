from selenium import webdriver
import logging,pandas as pd
import acqua.aqueduct as aq
import time
gestore = "ASPAsti"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.asp.asti.it/idrico-integrato/acquedotto/qualita-dellacqua/'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
locationList = pd.read_csv("Metadata/LocationList.csv")
reportFoundList = pd.DataFrame()
for i,location in locationList.iterrows():
    #i=0
    #location = locationList.loc[i]
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    logging.info( "Updating reportFoundList (%s) for %s, %s", i, alias_city, alias_address )
    time.sleep(1)
    tablElement = driver.find_element_by_css_selector(".fusion-column-wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1)" )
    try:
        urlWebElement = tablElement.find_element_by_link_text(alias_address)
        urlReport = urlWebElement.get_attribute('href')
        row = {'alias_city':alias_city,'alias_address':alias_address,'urlReport':urlReport}
        reportFoundList = reportFoundList.append( row, ignore_index=True )
        locationList.to_csv('Metadata/LocationList.csv',index=False)
    except:
        logging.critical("Location not found for %s. Skiped!", alias_address)
#
driver.close()
reportFoundList.to_csv("Metadata/ReportFoundList.csv",index=False)