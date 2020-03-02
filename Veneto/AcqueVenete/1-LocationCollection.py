from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd,datetime,os,logging,time,numpy as np
os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Bim')
logging.basicConfig(level=logging.INFO)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument('--incognito')
#options.add_argument('--headless')
#driver = webdriver.Chrome("D:\EmporioADV\chromedriver", options=options)
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(10)
locationList = pd.DataFrame()
driver.get("https://qualitacqua.mys.it/?nolay=true")
selectComune = Select(driver.find_element(By.ID,'comune'))
selectCentrale = Select(driver.find_element(By.ID,'centrale'))

selectComune.options[6].click()




soup = BeautifulSoup(driver.page_source, "html.parser")
#
selectComuni = soup.findAll('option')
alias_city = [c.get_text() for c in selectComuni if c.get_text()!='seleziona']











listaComuni = ['AGORDO', 'ALLEGHE', 'ALPAGO', "ARSIE'", 'AURONZO DI CADORE', 'BELLUNO', 'BORCA DI CADORE', 'CALALZO DI CADORE', "CANALE D'AGORDO", 'CENCENIGHE AGORDINO', 'CESIOMAGGIORE', "CHIES D'ALPAGO", 'CIBIANA DI CADORE', 'COLLE SANTA LUCIA', 'COMELICO SUPERIORE', "CORTINA D'AMPEZZO", 'DANTA DI CADORE', 'DOMEGGE DI CADORE', 'FALCADE', 'FELTRE', 'FONZASO', 'GOSALDO', 'LA VALLE AGORDINA', 'LAMON', 'LENTIAI', 'LIMANA', 'LIVINALLONGO DEL COL DI LANA', 'LONGARONE', 'LORENZAGO DI CADORE', 'LOZZO DI CADORE', 'MEL', 'OSPITALE DI CADORE', 'PEDAVENA', 'PERAROLO DI CADORE', 'PIEVE DI CADORE', 'PONTE NELLE ALPI', 'RIVAMONTE AGORDINO', 'ROCCA PIETORE', 'SAN GREGORIO NELLE ALPI', 'SAN PIETRO DI CADORE', 'SAN TOMASO AGORDINO', 'SAN VITO DI CADORE', 'SANTA GIUSTINA', 'SANTO STEFANO DI CADORE', 'SAPPADA', 'SEDICO', 'SELVA DI CADORE', 'SEREN DEL GRAPPA', 'SOSPIROLO', 'SOVERZENE', 'SOVRAMONTE', 'TAIBON AGORDINO', "TAMBRE D'ALPAGO", 'TRICHIANA', 'VAL DI ZOLDO', 'VALLADA AGORDINA', 'VALLE DI CADORE', 'VIGO DI CADORE', 'VODO DI CADORE', 'VOLTAGO AGORDINO', "ZOPPE' DI CADORE"]

for i,comune in enumerate(listaComuni):

    logging.info(">>> %s (%s/%s)",comune,i,len(listaComuni))
    webElement = driver.find_element_by_class_name( 'ui-select-placeholder' )
    driver.execute_script( "arguments[0].click();", webElement )
    a = driver.find_element_by_xpath('//*[@id="analisiacque-page"]/div/div/div[1]/div[1]/input[1]')
    a.send_keys(comune)
    driver.execute_script( "arguments[0].click();", webElement )
    b = driver.find_element_by_css_selector('#ui-select-choices-row-0-0 > a > div > span')
    driver.execute_script( "arguments[0].click();", b )

    alias_city = comune
    # Estrazione dei web element dell'elenco delle vie
    webElement_vie = driver.find_element_by_xpath("/html/body/div[1]/section[1]/div/div/div[1]/section[1]/div/div/div/div[1]/div[2]/div/span/span[1]" )
    driver.execute_script( "arguments[0].click();", webElement_vie )
    # Estrazione dei web element dell'elenco delle vie
    webElement_vie = driver.find_element_by_id( "ui-select-choices-1" )

    time.sleep( 2 )
    webElement_listaVie = webElement_vie.find_elements_by_class_name( "ui-select-choices-row-inner" )
    listaVie = [e.text for e in webElement_listaVie]

    for j,alias_address in enumerate(listaVie):
        row = {'alias_city':alias_city,'alias_address':alias_address,'georeferencingString':alias_address+', '+alias_city+', Belluno, Veneto, Italia'}
        #logging.info("Insered %s (%s/%s)",row,i,len(listaComuni))
        locationList = locationList.append(row,ignore_index=True)

locationList.to_csv('Definitions/LocationList.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
