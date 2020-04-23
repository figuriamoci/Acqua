#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd,datetime,os,logging
import acqua.aqueduct as aq
aq.setEnv('Veneto//AcqueVenete')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
#driver = webdriver.Chrome("D:\EmporioADV\chromedriver", options=options)
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(10)
#http://www.acquevenete.it/it_IT/consulta-le-analisi
driver.get("https://qualitacqua.mys.it/?nolay=true")
selectComune = Select(driver.find_element(By.ID,'comune'))
comuniList = selectComune.options
locationList = pd.DataFrame()
##
for i,comune in enumerate(comuniList):
    if i>0: #Salta la prima riga
        comune.click()
        centrale = driver.find_element_by_css_selector('[data-id="centrale"]')
        row = [{'alias_city':comune.text, 'alias_acqueduct':centrale.text.replace('\n','').strip()}  ]
        locationList = locationList.append(row)
##
locationList['georeferencingString'] = locationList['alias_city']+", Veneto, Italia"
locationList['type'] = 'POINT'
driver.close()
locationList.to_csv('Medadata/LocationList.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
