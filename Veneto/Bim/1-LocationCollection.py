#%%
from selenium import webdriver
import pandas as pd,datetime,os,logging,time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Bim')
logging.basicConfig(level=logging.INFO)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
#driver = webdriver.Chrome("D:\EmporioADV\chromedriver", options=options)
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(10)
foundReportList = {}
driver.get("https://www.bimgsp.it/idrico/acqua-di-rubinetto-pura-e-controllata/")

#Estrazione dell'elenco dei comuni
#element = WebDriverWait(firefox, wait_for_element).until(EC.element_to_be_clickable((By.CLASS_NAME, "but selected'")))
#Attivazione lista valori comuni
#webElement = WebDriverWait(driver, 10).until(EC.find_element_by_class_name('ui-select-placeholder'))
webElement = driver.find_element_by_class_name('ui-select-placeholder')
driver.execute_script("arguments[0].click();", webElement)
webElement_comuni = driver.find_element_by_id("ui-select-choices-0")
webElement_listaComuni = webElement_comuni.find_elements_by_class_name("ui-select-choices-row")
###
listaComuni = [e.text for e in webElement_listaComuni]
locationList = pd.DataFrame()
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
for i,nomeComune in enumerate(listaComuni):

    webElement = driver.find_element_by_class_name('ui-select-placeholder')
    driver.execute_script("arguments[0].click();", webElement)
    webElement_comuni = driver.find_element_by_id("ui-select-choices-0")
    webElement_listaComuni = webElement_comuni.find_elements_by_class_name("ui-select-choices-row")

    comune = webElement_listaComuni[i]
    alias_city = comune.text
    driver.execute_script("arguments[0].click();", comune)
    ########################
    #Estrazione dei web element dell'elenco delle vie
    webElement_vie = driver.find_element_by_xpath("/html/body/div[1]/section[1]/div/div/div[1]/section[1]/div/div/div/div[1]/div[2]/div/span/span[1]")
    driver.execute_script("arguments[0].click();", webElement_vie)
    #Estrazione dei web element dell'elenco delle vie
    webElement_vie = driver.find_element_by_id("ui-select-choices-1")

    time.sleep(2)
    webElement_listaVie = webElement_vie.find_elements_by_class_name( "ui-select-choices-row-inner" )
    listaVie = [e.text for e in webElement_listaVie]

    for j,alias_address in enumerate(listaVie):
        row = {'alias_city':alias_city,'alias_address':alias_address,'georeferencingString':alias_city+' '+alias_address}
        logging.info("Insered %s (%s/%s)",row,i,len(listaComuni))
        locationList = locationList.append(row,ignore_index=True)

locationList.to_csv('Definitions/LocationList.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
