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
urlReport = [a['href'] for a in addressList]
#
driver.close()
reportFoundList = pd.DataFrame({'alias_city':alias_city, 'urlReport':urlReport})
reportFoundList['alias_address'] = 'Territorio'
reportFoundList.to_csv('Metadata/ReportFoundList.csv',index=False)

