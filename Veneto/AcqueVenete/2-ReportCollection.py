from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd,datetime,os,logging,time,numpy as np
import acqua.aqueduct as aq
aq.setEnv('Veneto//AcqueVenete')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
#driver = webdriver.Chrome("D:\EmporioADV\chromedriver", options=options)
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(10)
##http://www.acquevenete.it/it_IT/consulta-le-analisi
driver.get("https://qualitacqua.mys.it/?nolay=true")
locationList = pd.read_csv('Definitions/LocationList.csv')
data_report = '06/11/2019'
reportFoundList = pd.DataFrame()

for i,location in locationList.iterrows():
    alias_city = location['alias_city']
    alias_acqueduct = location['alias_acqueduct']
    logging.info('>>> %s, %s.',alias_city,alias_acqueduct)
    selectComune = Select(driver.find_element(By.ID,'comune'))
    selectComune.select_by_visible_text(alias_city)
    selectCentrali = Select(driver.find_element(By.ID,'centrale'))
    selectCentrali.select_by_visible_text(alias_acqueduct)
    time.sleep(2)
    
    htmlTable = driver.find_element(By.TAG_NAME,'table')
    rowTable = pd.read_html(htmlTable.get_attribute('outerHTML'),thousands=',',decimal='.')[0]
    parameters = rowTable.set_index('Parametro')['ultimo valore'].to_dict()
    report = {'alias_city':alias_city, 'alias_acqueduct':alias_acqueduct,'data_report': data_report }
    report.update(parameters)
    reportFoundList = reportFoundList.append(report,ignore_index=True)

reportFoundList.to_csv('Medadata/DataReportCollection.csv',decimal='.',index=False)
logging.info('Finish: %s',datetime.datetime.now())
