##
from selenium import webdriver
import time,numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging,pandas as pd
import acqua.aqueduct as aq
import  acqua.parametri as parm
gestore = "LarioLecco"
aq.setEnv('Lombardia//'+gestore)
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
locationList = pd.read_csv( 'Metadata/LocationList.csv' )
locationList = locationList[locationList['alias_city']=='Lecco']
reportFoundList = pd.DataFrame()
#
for i,location in locationList.iterrows():
    driver = webdriver.Chrome( "chromedriver", options=options )
    driver.implicitly_wait( 10 )  # seconds
    driver.get( "http://box.larioreti.it/Box7/#analisi" )
    time.sleep( 5 )
    try:
        alias_city = location['alias_city']
        alias_address = location['alias_address']
        logging.info( "Processing %s...", alias_city )
        inputComune = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_css_selector( "#gwt-uid-5 > div > div:nth-child(2) > div > input" ) ) )
        inputComune.send_keys( alias_city )
        time.sleep( 3 )
        inputComune.send_keys( Keys.ENTER )
        time.sleep( 3 )
        selectIndirizzi = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_css_selector( "#gwt-uid-5 > div > div:nth-child(3) > div > input" ) ) )
        selectIndirizzi.send_keys( alias_address )
        time.sleep( 3 )
        selectIndirizzi.send_keys( Keys.ENTER )
        time.sleep( 3 )
        #
        tableWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_css_selector("#Box7-2076652 > div > div.v-horizontallayout.v-layout.v-horizontal.v-widget.v-has-width.v-has-height > div > div > div > div > div.v-panel-content.v-panel-content-light.v-panel-content-white.v-scrollable > div > div:nth-child(2) > div > div.v-panel-content.v-panel-content-light.v-scrollable > div > div:nth-child(1) > div > div.v-scrollable.v-table-body-wrapper.v-table-body > div:nth-child(1) > table" ) ) )
        tableHtml = tableWebElement.get_attribute( 'outerHTML' )
        parametriRaw = pd.read_html( tableHtml, decimal=',', thousands='.' )[0]
        ##
        parametri = parametriRaw.iloc[:,0:2]
        parametri.rename(columns={0:'parametro',1:'valore'},inplace=True)
        parametri.set_index('parametro', inplace=True )
        stdParms = parm.standardize( useThisDictionary, parametri['valore'].to_dict() )
        #
        data_report = time.strftime( "%d/%m/%Y" )
        row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        row.update( stdParms )
        reportFoundList = reportFoundList.append( row, ignore_index=True )
        logging.info( "Hacked %s / %s (%s/%s)", alias_city, alias_address, i + 1, len( locationList ) )
    except:
        logging.critical("Skip %s/%s",alias_city,alias_address)

    driver.close()
#
reportFoundList = reportFoundList.replace('nan',np.nan)
reportFoundList.to_csv('Metadata/ReportFoundList.csv',index=False)


