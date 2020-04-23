##
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import pandas as pd
import datetime
import os
import logging

os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Lta')
logging.basicConfig(level=logging.INFO)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.get("https://www.lta.it/le-analisi-della-tua-acqua")
##
logging.info('Start: %s',datetime.datetime.now())
soup = BeautifulSoup(driver.page_source, 'html.parser')
ListaAddress = soup.find(id="punto-di-analisi").findAll('option')
ListaAddress = [addr.get_text() for addr in ListaAddress]
ListaAddress = ListaAddress[1:] #Drop del pimo elemento in quanto non signficativo
ListaCity = [addr.split('-',1)[0] for addr in ListaAddress]
#Creazione dataframe
data = {'alias_city':ListaCity,'alias_address':ListaAddress}
df = pd.DataFrame(data)
#Output
df.to_csv('Medadata/LocationList.csv',index=False)

logging.info('Finish: %s',datetime.datetime.now())