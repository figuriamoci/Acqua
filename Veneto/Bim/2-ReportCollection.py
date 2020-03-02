# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd, datetime, os, logging,time
os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Bim')
logging.basicConfig( level=logging.INFO )
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
# driver = webdriver.Chrome("D:\EmporioADV\chromedriver", options=options)
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )
foundReportList = {}
driver.get( "https://www.bimgsp.it/idrico/acqua-di-rubinetto-pura-e-controllata/" )

# Estrazione dell'elenco dei comuni
# element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement"))
# Attivazione lista valori comuni
# webElement = WebDriverWait(driver, 10).until(EC.find_element_by_class_name('ui-select-placeholder'))
listaComuni = ['AGORDO', 'ALLEGHE', 'ALPAGO', "ARSIE'", 'AURONZO DI CADORE', 'BELLUNO', 'BORCA DI CADORE', 'CALALZO DI CADORE', "CANALE D'AGORDO", 'CENCENIGHE AGORDINO', 'CESIOMAGGIORE', "CHIES D'ALPAGO", 'CIBIANA DI CADORE', 'COLLE SANTA LUCIA', 'COMELICO SUPERIORE', "CORTINA D'AMPEZZO", 'DANTA DI CADORE', 'DOMEGGE DI CADORE', 'FALCADE', 'FELTRE', 'FONZASO', 'GOSALDO', 'LA VALLE AGORDINA', 'LAMON', 'LENTIAI', 'LIMANA', 'LIVINALLONGO DEL COL DI LANA', 'LONGARONE', 'LORENZAGO DI CADORE', 'LOZZO DI CADORE', 'MEL', 'OSPITALE DI CADORE', 'PEDAVENA', 'PERAROLO DI CADORE', 'PIEVE DI CADORE', 'PONTE NELLE ALPI', 'RIVAMONTE AGORDINO', 'ROCCA PIETORE', 'SAN GREGORIO NELLE ALPI', 'SAN PIETRO DI CADORE', 'SAN TOMASO AGORDINO', 'SAN VITO DI CADORE', 'SANTA GIUSTINA', 'SANTO STEFANO DI CADORE', 'SAPPADA', 'SEDICO', 'SELVA DI CADORE', 'SEREN DEL GRAPPA', 'SOSPIROLO', 'SOVERZENE', 'SOVRAMONTE', 'TAIBON AGORDINO', "TAMBRE D'ALPAGO", 'TRICHIANA', 'VAL DI ZOLDO', 'VALLADA AGORDINA', 'VALLE DI CADORE', 'VIGO DI CADORE', 'VODO DI CADORE', 'VOLTAGO AGORDINO', "ZOPPE' DI CADORE"]
for i,comune in enumerate(listaComuni):

    webElement = driver.find_element_by_class_name( 'ui-select-placeholder' )
    driver.execute_script( "arguments[0].click();", webElement )
    #a = WebDriverWait( driver, 10 ).until(EC.presence_of_element_located(By.CSS_SELECTOR,'#analisiacque-page > div > div > div.params > div.ui-select-container.ui-select-bootstrap.dropdown.ng-valid.open > input.form-control.ui-select-search.ng-pristine.ng-valid.ng-touched'))
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

    for j, nomeVia in enumerate( listaVie ):
        webElement_vie = driver.find_element_by_xpath("/html/body/div[1]/section[1]/div/div/div[1]/section[1]/div/div/div/div[1]/div[2]/div/span/span[1]" )
        driver.execute_script( "arguments[0].click();", webElement_vie )
        # Estrazione dei web element dell'elenco delle vie
        webElement_vie = driver.find_element_by_id( "ui-select-choices-1" )
        webElement_listaVie = webElement_vie.find_elements_by_class_name( "ui-select-choices-row-inner" )
        via = webElement_listaVie[j]
        alias_address = via.text
        logging.info( "Estrazione parametri per '%s' del comune '%s' (%s,%s)", alias_address, alias_city, i, j )
        # print(j,via.text)
        # Seleizone della via e quindi attivazione della tabella dei parametri
        driver.execute_script( "arguments[0].click();", via )
        # Recupero della tabella dei parametri
        webElement_tabella = driver.find_element_by_xpath(
            '//*[@id="analisiacque-page"]/div/div/div[2]/div/div[1]/table' )
        tabella_html = webElement_tabella.get_attribute( 'outerHTML' )
        parametriRaw = (pd.read_html( tabella_html ,thousands='.',decimal=','))[0]
        parametri = parametriRaw[['Parametro', 'Rilevamento']]
        parametri.set_index( 'Parametro', inplace=True )

        webElement_data_report = driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/div[1]/section[1]/div/div/div/div[2]/div/div[2]/div/p' )
        data_report = webElement_data_report.text

        location = (alias_city, alias_address)
        report = {'data_report': data_report, 'parametri': parametri}
        foundReportList.update( {location: report} )
##
driver.close()
# %%
import pickle
with open( 'Definitions/FoundReportList.pickle', 'wb' ) as handle: pickle.dump( foundReportList, handle )
handle.close()

logging.info( 'Finish: %s', datetime.datetime.now() )