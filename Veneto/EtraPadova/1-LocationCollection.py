##
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd,datetime,logging,time
import acqua.aqueduct as aq
aq.setEnv('Veneto//EtraPadova')
url = 'https://www.etraspa.it/resana/impresa/acqua/analisi-dellacqua'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(10)
driver.get(url)
##
selectComuniElement = Select(driver.find_element_by_class_name('form-wrapper').find_element_by_tag_name('select'))
alias_city = [c.text for i,c in enumerate(selectComuniElement.options) if i>1]
locationList = pd.DataFrame(alias_city,columns=['alias_city'])
locationList['alias_address'] = 'Comune'
locationList['georeferencingString'] = locationList['alias_city']+", Veneto, Italia"
locationList['type'] = 'POINT'
##
driver.close()
locationList.to_csv('Definitions/LocationList.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
