##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging,pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
gestore = "IrenLiguria"
aq.setEnv('Liguria//'+gestore)
url = 'https://serviziweb.gruppoiren.it/QualitaAcqua/custom/VisualizzaAnalisi.aspx?codiceRegione=07'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
#
locationList = pd.read_csv('Metadata/LocationList.csv')
dataReportCollection = pd.DataFrame()
#locationList = locationList.iloc[39:40]
for i,location in locationList.iterrows():
    #location = locationList.iloc[66]
    driver = webdriver.Chrome( "chromedriver", options=options )
    driver.implicitly_wait( 10 )  # seconds
    driver.get( url )
    #time.sleep( 1 )
    alias_province = location['alias_province']
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    selectProvinceWebElement = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_id( "cmbProvincie" ) ) )
    Select( selectProvinceWebElement ).select_by_value( alias_province )
    time.sleep( 1 )
    #
    selectComuneWebElement = WebDriverWait( driver, 10 ).until(EC.visibility_of( driver.find_element_by_name( "cmbComuni" ) ) )
    Select( selectComuneWebElement ).select_by_visible_text( alias_city )
    time.sleep( 1 )
    ##
    #selectZoneWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_name( "cmbZone" ) ) )
    #selectZoneWebElement.text
    #Select( selectZoneWebElement ).select_by_visible_text( alias_address )
    #time.sleep( 1 )
    #
    try:
        tableWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "analisi" ) ) )
        tableHtml = tableWebElement.get_attribute( 'outerHTML' )
        table = pd.read_html( tableHtml, decimal='.', thousands=',' )[0]
        table.set_index( ['Parametro'], inplace=True )
        parms = table.loc[parametersAdmitted]['Media']
        ##
        stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
        data_report = driver.find_element_by_id("dtPeriodo").text
        #
        row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        row.update( stdParms )
        dataReportCollection = dataReportCollection.append( row, ignore_index=True )
        logging.info( "Hacked %s/%s (%s/%s)!",alias_city,alias_address, i + 1, len( locationList ) )
    except KeyError:
        logging.critical("Skiped %s/%s !",alias_city,alias_address)

    driver.close()
#
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
