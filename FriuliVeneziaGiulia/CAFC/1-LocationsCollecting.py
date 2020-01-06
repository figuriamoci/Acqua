from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import pandas as pd
import datetime

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
#driver = webdriver.Chrome("D:\EmporioADV\chromedriver", chrome_options=options)
driver = webdriver.Chrome("chromedriver", chrome_options=options)
driver.get("https://www.cafcspa.com/solud/it-_qualita_acqua.cfm")
#print('Http status: ',page.status_code)

soup = BeautifulSoup(driver.page_source, 'html.parser')
listaComuni = soup.find(id="comuni").findAll('option')
listaComuni = [comune.get_text() for comune in listaComuni]
listaComuni = ['FAGAGNA']#,'AMARO']

print('Start: ',datetime.datetime.now())
locationList = pd.DataFrame()

nComuni=0
totComuni = len(listaComuni)

for comune in listaComuni:
    control_comuni = Select(driver.find_element_by_id('comuni'))
    control_comuni.select_by_visible_text(comune)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #print(soup.prettify())
    
    listaIndirizzi = soup.find('select',id="indirizzi").findAll('option')
    listaIndirizzi = [indirizzo.get_text() for indirizzo in listaIndirizzi]
    nComuni = nComuni+1
    print('Comune:',comune,'(',nComuni,'/',totComuni,')')
    i=0
    for indirizzo in listaIndirizzi:
        i=i+1
        print('indirizzo:', indirizzo, '(', i, '/', len(listaIndirizzi), ')')
        if str(indirizzo).strip() != '':
            control_indirizzi = Select(driver.find_element_by_id('indirizzi'))  
            control_indirizzi.select_by_visible_text(indirizzo)
            soup = BeautifulSoup(driver.page_source, 'html.parser')             
            locationList_row = {}
            locationList_row['location'] = comune+' '+indirizzo
            locationList_row['region'] = 'Friuli'
            locationList_row['alias_city'] = comune
            locationList_row['alias_address'] = indirizzo
            locationList = locationList.append(locationList_row,ignore_index=True)
            
locationList.to_csv('Definitions/LocationList.csv',index=False)
print('Finish: ',datetime.datetime.now())