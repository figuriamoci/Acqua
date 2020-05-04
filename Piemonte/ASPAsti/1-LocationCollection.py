##
from selenium import webdriver
import logging,pandas as pd
import acqua.aqueduct as aq
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
tablElement = driver.find_element_by_css_selector( ".fusion-column-wrapper > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1)" )
tableHtml = tablElement.get_attribute('outerHTML')
driver.close()
table = pd.read_html(tableHtml)
##
alias_address = []
for t in table: alias_address.extend(list(t.iloc[:,1]))
locationList = pd.DataFrame({"alias_address":alias_address})
locationList['alias_city'] = "Asti"
locationList['georeferencingString'] = locationList['alias_address']+", "+locationList['alias_city']+", 14100, Asti, AT"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
