# %%
from selenium import webdriver
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
webElement = driver.find_element_by_class_name( 'ui-select-placeholder' )
driver.execute_script( "arguments[0].click();", webElement )
webElement_comuni = driver.find_element_by_id( "ui-select-choices-0" )
webElement_listaComuni = webElement_comuni.find_elements_by_class_name( "ui-select-choices-row" )
###
listaComuni = [e.text for e in webElement_listaComuni]
for i, nomeComune in enumerate( listaComuni ):

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

        webElement_data_report = driver.find_element_by_xpath(
            '/html/body/div[1]/section[1]/div/div/div[1]/section[1]/div/div/div/div[2]/div/div[2]/div/p' )
        data_report = webElement_data_report.text

        location = (alias_city, alias_address)
        report = {'data_report': data_report, 'parametri': parametri}
        foundReportList.update( {location: report} )

driver.close()
# %%
import pickle
with open( 'Definitions/FoundReportList.pickle', 'wb' ) as handle: pickle.dump( foundReportList, handle )
handle.close()

logging.info( 'Finish: %s', datetime.datetime.now() )