##
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd,datetime,os,logging,time,numpy as np
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import acqua.aqueduct as aq,re
aq.setEnv('Veneto//AcqueVeronesi')
url = 'http://www.acqueveronesi.it/qualita-acqua.asp?IdPagina=16'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(20)
##
locationList = pd.read_csv( 'Definitions/ReviewedLocationList.csv' )
reportFoundList = pd.DataFrame()
for i,location in locationList.iterrows():
    try:
        driver.get(url)
        alias_city = locationList.iloc[i]['alias_city']
        alias_address = locationList.iloc[i]['alias_address']
        #
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "elenco_comuni2")))
        selectComune = Select(driver.find_element(By.ID,'elenco_comuni2'))
        selectComune.select_by_visible_text(alias_city)
        #
        time.sleep(5)
        selectVie = WebDriverWait(driver, 29).until(EC.presence_of_element_located((By.ID, "indirizzi_comune_chosen")))
        anchor = WebDriverWait(selectVie, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "a")))
        anchor.click()
        WebDriverWait(selectVie, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "input"))).send_keys(alias_address)
        WebDriverWait(selectVie, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "li"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn:nth-child(12)"))).click()
        ##
        premessaElement = driver.find_element_by_tag_name('article').find_element_by_tag_name('div')
        premessa = premessaElement.text.split('\n')
        data_report = premessa[2]
        htmlTable = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rowTable = htmlTable.get_attribute( 'outerHTML' )
        parametriRaw = (pd.read_html( rowTable, thousands='.', decimal=',', na_values='-' ))[0]
        #
        table_ = parametriRaw.T
        table_.set_index(0,inplace=True)
        table = table_.T
        #
        parametri = table[['Descrizione','Valore']].set_index('Descrizione').to_dict()['Valore']
        #
        report = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        report.update( parametri )
        reportFoundList = reportFoundList.append( report, ignore_index=True )
        logging.info('Haked %s/%s (%s/%s)!',alias_city,alias_address,i,len(locationList)-1)
    except:
        logging.critical('Skip %s/%s !',alias_city,alias_address)
##
driver.close()
reportFoundList.to_csv('Medadata/DataReportCollection.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
