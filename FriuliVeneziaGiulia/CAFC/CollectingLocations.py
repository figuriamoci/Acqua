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
listaComuni = ['UDINE']#,'AMARO']

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
    
    for indirizzo in listaIndirizzi:
        #indirizzo = listaIndirizzi[1]
        if str(indirizzo).strip() != '':
            control_indirizzi = Select(driver.find_element_by_id('indirizzi'))  
            control_indirizzi.select_by_visible_text(indirizzo)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            #print(soup.prettify())
            ###tipologia fonte
            #fonte = soup.find("td", text="Fonte :")
            #tipo_fonte = fonte.parent.find('h5').get_text()
            #nome = soup.find("td", text="Nome:")
            #nome_fonte = nome.parent.find('h5').get_text()
            ##url documento analisi
            ##Scarica il certificato di analisi dell'acqua: 
            urlassoluto=''
            a = soup.find('a')
            urlrelativo = a.attrs['href']
            urlassoluto = 'https://www.cafcspa.com/solud/'+urlrelativo
                
            locationList_row = {}
            locationList_row['location'] = comune+' '+indirizzo
            #locationList_row['indirizzo'] = indirizzo
            locationList_row['provincia'] = 'Friuli'
            #locationList_row['nome_fonte'] = nome_fonte
            #locationList_row['tipo_fonte'] = tipo_fonte
            locationList_row['alias'] = comune
            locationList_row['url'] = urlassoluto
            locationList = locationList.append(locationList_row,ignore_index=True)
            
locationList.to_csv('Definitions/LocationList.csv',index=False)
print('Finish: ',datetime.datetime.now())