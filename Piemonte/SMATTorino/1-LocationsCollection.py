from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd,os,logging
os.chdir('//Users//andrea//PycharmProjects//Acqua')
#os.chdir('D://Python//Acqua')
os.chdir('Piemonte//SMATTorino')
logging.basicConfig(level=logging.INFO)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.get("https://www.smatorino.it/monitoraggio-acque/")
##
soup = BeautifulSoup(driver.page_source, 'html.parser')
htmlTable = soup.find( "table", {"id": "lista-comuni"} )
df = pd.read_html( str( htmlTable ), decimal=',', thousands='.' )[0]
##
alias_city = {'alias_city':list(df.iloc[:,0])}
locationList = pd.DataFrame(alias_city)
locationList['alias_address'] = 'Comune'
locationList['georeferencingString'] = locationList['alias_city']+', Piemonte, Italia'
locationList['type'] = 'POINT'
##
locationList = locationList[locationList['alias_city']!='TORINO']
driver.close()
locationList.to_csv('Definitions/LocationList.csv',index=False)
