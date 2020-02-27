##
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd,datetime,os,logging

os.chdir('/Users/andrea/PycharmProjects/Acqua/Piemonte/AcquaNovara')
logging.basicConfig(level=logging.INFO)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.get("https://www.acquanovaravco.eu/AnalisiAcqua?id=qualita-dell-acqua")
##
soup = BeautifulSoup(driver.page_source, 'html.parser')
listaComuni_ = soup.find(id="Comune").findAll('option')
listaComuni = [comune.get_text() for comune in listaComuni_]
alias_city = {'alias_city':listaComuni}
locationList = pd.DataFrame(alias_city).drop(axis=1,index=0)
locationList['alias_address'] = 'Comune'
locationList['georeferencingString'] = locationList['alias_city']+', Piemonte, Italia'
locationList['type'] = 'POINT'
driver.close()
locationList.to_csv('Definitions/LocationList.csv',index=False)
