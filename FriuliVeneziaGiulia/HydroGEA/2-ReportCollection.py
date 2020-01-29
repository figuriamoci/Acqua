from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import pandas as pd
import datetime
import os
os.path.abspath("Definitions/LocationList.csv")

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
#driver = webdriver.Chrome("D:\EmporioADV\chromedriver", chrome_options=options)
driver = webdriver.Chrome("chromedriver", chrome_options=options)
driver.get("https://www.cafcspa.com/solud/it-_qualita_acqua.cfm")
#print('Http status: ',page.status_code)

soup = BeautifulSoup(driver.page_source, 'html.parser')
df = pd.read_csv('Definitions/LocationList.csv') 
comune = 'FAGAGNA'
alias_addressList = df['alias_address'].tolist()

print('Start: ',datetime.datetime.now())
locationList = pd.DataFrame()
naddress=0
totaddress = len(alias_addressList)
#alias_addressList = ['PIAZZA DELLA CHIESA']

control_comuni = Select(driver.find_element_by_id('comuni'))
control_comuni.select_by_visible_text(comune)
reportList = pd.DataFrame()
i=0
for indirizzo in alias_addressList:
    i=i+1
    naddress = naddress+1
    print('indirizzo:',indirizzo,'(',naddress,'/',totaddress,')')
    control_indirizzi = Select(driver.find_element_by_id('indirizzi'))  
    control_indirizzi.select_by_visible_text(indirizzo)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    a = soup.find('a')
    urlrelativo = a.attrs['href']
    urlassoluto = 'https://www.cafcspa.com/solud/'+urlrelativo
    row = df.iloc[i-1].to_dict()
    row['url'] = urlassoluto
    reportList = reportList.append(row,ignore_index=True)
    #print(soup.prettify())
    ###tipologia fonte
    #fonte = soup.find("td", text="Fonte :")
    #tipo_fonte = fonte.parent.find('h5').get_text()
    #nome = soup.find("td", text="Nome:")
    #nome_fonte = nome.parent.find('h5').get_text()
    ##url documento analisi
    ##Scarica il certificato di analisi dell'acqua: 
            
reportList.to_csv('Definitions/FoundReportList.csv',index=False)
print('Finish: ',datetime.datetime.now())
##
r = reportList.groupby('url').count()
print('Report found:',len(r))
##
print(r)
##

