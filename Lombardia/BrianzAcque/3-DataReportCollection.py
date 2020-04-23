##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging,pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
gestore = "BrianzAcque"
aq.setEnv('Lombardia//'+gestore)
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
#
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
#options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( "https://richiesteassistenza.brianzacque.it/servizi/punti-prelievo" )
time.sleep(10)
#
selectWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "comunePrelievo" ) ) )
elencoComuni_ = selectWebElement.text.split("\n")
elencoComuni = [c.strip() for i,c in enumerate(elencoComuni_) if i > 0 and c.strip()!=""]
driver.close()
dataReportCollection = pd.DataFrame()
#elencoComuni = elencoComuni[18:22]
#
for i,comune in enumerate(elencoComuni):
    try:
        driver = webdriver.Chrome( "chromedriver", options=options )
        driver.implicitly_wait( 10 )  # seconds
        driver.get( "https://richiesteassistenza.brianzacque.it/servizi/punti-prelievo" )
        time.sleep( 5 )
        selectWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "comunePrelievo" ) ) )
        Select(selectWebElement).select_by_visible_text(comune)
        buttonWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_css_selector( "body > div.c-container-flex > ui-view > ng-include:nth-child(3) > div > div > div > div.c-box-bordered.c-margin-top-2 > form > button" ) ) )
        driver.execute_script( "arguments[0].click();", buttonWebElement )
        #
        time.sleep(3)
        div = driver.find_element_by_css_selector("#map > div > div > div:nth-child(1) > div:nth-child(3) > div > div:nth-child(3)")
        time.sleep(3)
        puntoMonitoraggio = div.find_elements_by_tag_name("div")
        #
        for k,pm in enumerate(puntoMonitoraggio):
            try:
                driver.execute_script( "arguments[0].click();", pm )
                time.sleep(2)
                popUp = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_class_name( "infowindow" ) ) )
                alias_city = popUp.text.split("\n")[0]
                alias_address = popUp.text.split("\n")[1]
                #
                dettagliWebElement = driver.find_element_by_link_text("Dettagli")
                driver.execute_script( "arguments[0].click();", dettagliWebElement )
                time.sleep(2)
                #
                table = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_class_name( "c-box-analisi-container" ) ) )
                rawParms = table.text.split("\n")
                parms = {rawParms[i]:rawParms[i+2] for i in range(0,len(rawParms),4) if rawParms[i] in parametersAdmitted}
                stdParms = parm.standardize( useThisDictionary, parms )
                data_report = driver.find_element_by_css_selector("#dati-punto > div > p > strong").text
                row = {"alias_city":alias_city,"alias_address":alias_address,'data_report':data_report}
                row.update(stdParms)
                dataReportCollection = dataReportCollection.append( row, ignore_index=True )
                logging.info("Retrived %s/%s (%s,%s)",alias_city,alias_address,i+1,len(elencoComuni))
            except:
                logging.critical("Skip light %s/%s",alias_city,alias_address)
    except:
        logging.critical("Skip %s/%S",alias_city,alias_address)
    driver.close()
#
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)


