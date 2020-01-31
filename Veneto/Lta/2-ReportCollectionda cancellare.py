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
#driver = webdriver.Chrome("D:\EmporioADV\chromedriver", chrome_options=options)
driver = webdriver.Chrome("chromedriver", options=options)
driver.get("https://www.cafcspa.com/solud/it-_qualita_acqua.cfm")
#print('Http status: ',page.status_code)
df = pd.read_csv('Definitions/LocationList.csv')
comuneList = [comune for comune in df['alias_city'].drop_duplicates()]
reportList = pd.DataFrame()
logging.info( 'Start: %s', datetime.datetime.now() )
for k,comune in enumerate(comuneList):
    df_ = df[df['alias_city'] == comune]
    alias_addressList = df_['alias_address'].tolist()
    locationList = pd.DataFrame()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    control_comuni = Select(driver.find_element_by_id('comuni'))
    control_comuni.select_by_visible_text(comune)
    for i,indirizzo in enumerate(alias_addressList):
        logging.info('Analyzing: %s (%s/%s) - %s (%s/%s).',comune,k+1,len(comuneList),indirizzo,i+1,len(alias_addressList))
        control_indirizzi = Select(driver.find_element_by_id('indirizzi'))
        control_indirizzi.select_by_visible_text(indirizzo)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        a = soup.find('a')
        urlrelativo = a.attrs['href']
        if urlrelativo == 'http://www.cafcspa.com':
            urlassoluto = ''
        else:
            urlassoluto = 'https://www.cafcspa.com/solud/' + urlrelativo

        row = {}
        row['alias_city'] = comune
        row['alias_address'] = indirizzo
        row['url'] = urlassoluto
        reportList = reportList.append(row,ignore_index=True)
        #print(soup.prettify())
        #tipologia fonte
        #fonte = soup.find("td", text="Fonte :")
        #tipo_fonte = fonte.parent.find('h5').get_text()
        #nome = soup.find("td", text="Nome:")
        #nome_fonte = nome.parent.find('h5').get_text()
        #url documento analisi
        #Scarica il certificato di analisi dell'acqua:
            
reportList.to_csv('FriuliVeneziaGiulia/CAFC/Definitions/FoundReportList.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
logging.info('Report found: %s',len(reportList))

