##
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd,datetime,os,logging,time,numpy as np
import acqua.aqueduct as aq,re
aq.setEnv('Veneto//AcqueVeronesi')
url = 'http://www.acqueveronesi.it/qualita-acqua.asp?IdPagina=16'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(20)
driver.get(url)
#
WebDriverWait( driver, 20 ).until(EC.presence_of_element_located( (By.ID, "elenco_comuni2")))
selectComune = Select(driver.find_element(By.ID,'elenco_comuni2'))
listaComuni = [comune.text for comune in selectComune.options]
#
WebDriverWait( driver, 20 ).until(EC.presence_of_element_located( (By.ID, "indirizzi_comune_chosen")))
indirizziElement = driver.find_element(By.ID,'indirizzi_comune_chosen')
#
WebDriverWait( indirizziElement, 20 ).until(EC.presence_of_element_located( (By.TAG_NAME, "a")))
indirizziElement.find_element_by_tag_name('a').click()
#
WebDriverWait( indirizziElement, 20 ).until(EC.presence_of_element_located( (By.TAG_NAME, "input")))
indirizziElement.find_element_by_tag_name('input').send_keys('Via')
#
WebDriverWait( indirizziElement, 20 ).until(EC.presence_of_element_located( (By.CLASS_NAME, "active-result")))
resultElement = indirizziElement.find_elements_by_class_name('active-result')
listaIndirizzi = [indirizzo.text for indirizzo in resultElement]
driver.close()
########################
alias_city = pd.DataFrame(listaComuni,columns=['alias_city'])
alias_city['citta'] = alias_city['alias_city'].str.upper()
#
alias_address = pd.DataFrame(listaIndirizzi,columns=['indirizzo'])
alias_address['citta'] = alias_address['indirizzo'].apply(lambda s: re.findall('\(.+\)',s)[0].replace('(','').replace(')',''))
alias_address['alias_address'] = alias_address['indirizzo'].apply(lambda s: s.split(re.findall('\(.+\)',s)[0])[0].strip())
#
locationList_ = pd.merge(alias_city, alias_address, how='inner', on='citta')
#
locationList = locationList_[['alias_city','alias_address']]
locationList['georeferencingString'] = locationList_['alias_address']+', '+locationList_['alias_city']+', Verona, Veneto, Italia'
locationList['type'] = 'POINT'
#
locationList.to_csv('Definitions/LocationList.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
