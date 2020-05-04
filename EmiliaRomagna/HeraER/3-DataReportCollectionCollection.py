##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging,pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
gestore = "HeraER"
aq.setEnv('EmiliaRomagna//'+gestore)
url = 'https://www.gruppohera.it/gruppo/attivita_servizi/business_acqua/canale_acqua/'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
#
locationList = pd.read_csv('Metadata/LocationList.csv')
dataReportCollection = pd.DataFrame()
#locationList = locationList.iloc[57:60]
for i,location in locationList.iterrows():
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    driver = webdriver.Chrome( "chromedriver", options=options )
    driver.implicitly_wait( 10 )  # seconds
    driver.get( url )
    time.sleep( 3 )
    #
    divWebElement = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_class_name( "form_scopricosabevi_campi" ) ) )
    inputWebElement = divWebElement.find_element_by_class_name( "ui-autocomplete-input" )
    inputWebElement.send_keys( alias_city.split("'")[0].split("ì")[0]  ) #workaround: Prende solo la prima parte, prima dell'eventuale apice
    time.sleep( 3 )
    #Putroppo non è sufficiente impostare la city, per due motivi: 1) non funziona con l'apice, 2) ci possono essere piu' città con lo stesso prefisso, per cui in alcuni casi bisogna selezionare la città dala lista.
    try:
        popUpWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "ui-id-2" ) ) )
        optionsWebElement = popUpWebElement.find_elements_by_tag_name("li")
        if len(optionsWebElement)>1:
            a = {we.text:we for we in optionsWebElement}
            driver.execute_script("arguments[0].click();", a[alias_city])
    except:
        pass
    submitWebElement = divWebElement.find_element_by_class_name( "submit" )
    driver.execute_script("arguments[0].click();", submitWebElement)
    #
    try:
        time.sleep( 2 )
        tableWebElement = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_id( "scopricosabevi-container" ) ) )
        tableHtml = tableWebElement.find_elements_by_tag_name("table")[0].get_attribute('outerHTML')
        #
        table = pd.read_html( tableHtml, decimal=',', thousands='.' )[0]
        table.set_index( table.columns[0], inplace=True )
        parms = table.loc[parametersAdmitted].iloc[:,0]
        #
        premessa = driver.find_element_by_class_name("tdclose")
        data_report = premessa.text.split("\n")[1]
        #
        row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
        row.update( stdParms )
        dataReportCollection = dataReportCollection.append( row, ignore_index=True )
        logging.info( "Hacked %s (%s/%s)!", alias_city, i + 1, len( locationList ) )
    except:
        logging.critical( "Skiped %s!", alias_city )
    driver.close()
##
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
