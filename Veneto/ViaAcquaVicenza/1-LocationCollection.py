##
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd,datetime,logging,time
import acqua.aqueduct as aq
aq.setEnv('Veneto//ViaAcquaVicenza')
url = 'https://www.viacqua.it/it/clienti/acquedotto/qualita-acqua/'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(10)
driver.get(url)
##
selectComune = Select(driver.find_element(By.ID,'local_comune'))
comuniList = [comune.text for i,comune in enumerate(selectComune.options) if i>0]
locationList = pd.DataFrame()
##
for i,alias_city in enumerate(comuniList):
    logging.info('>>> %s (%s/%s)',alias_city,i,len(comuniList)-1)
    selectComune.select_by_visible_text(alias_city)
    time.sleep(2)
    #identifica l'elenco delle vie
    selectAliasAddress = Select(driver.find_element(By.ID,'local_impianto'))
    alias = [{'alias_city':alias_city, 'alias_address':alias_address.text} for i,alias_address in enumerate(selectAliasAddress.options) if i>0]
    alias = alias[0:10]###########
    locationList = locationList.append(alias,ignore_index=True)
##
locationList['georeferencingString'] = locationList['alias_address']+', '+locationList['alias_city']+", Veneto, Italia"
locationList['type'] = 'POINT'
##
driver.close()
locationList.to_csv('Medadata/LocationList.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
