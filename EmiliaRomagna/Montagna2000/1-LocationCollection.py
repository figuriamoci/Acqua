##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
from selenium import webdriver
gestore = "Montagna2000"
aq.setEnv('EmiliaRomagna//'+gestore)
url = 'https://www.montagna2000.com/servizio-idrico-integrato/analisi-acqua-online/'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
#options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
soup = BeautifulSoup(driver.page_source, 'html.parser')
##
addressWrapperList = soup.find("ul", {"class":"posts-list-wrapper"})
addressList = addressWrapperList.find_all("a")
alias_city = [a['title'] for a in addressList]
#
geoStringList = soup.find_all("span", {"class":"address"})
georeferencingString = [a.text.strip() for a in geoStringList]
#
driver.close()
locationList = pd.DataFrame({'alias_city':alias_city, 'georeferencingString':georeferencingString})
locationList['alias_address'] = 'Territorio'
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)

