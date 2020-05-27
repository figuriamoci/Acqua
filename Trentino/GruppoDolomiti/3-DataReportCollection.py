#
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import acqua.aqueduct as aq
import time,logging,numpy as np
import acqua.parametri as parm
gestore = "GruppoDolomiti"
aq.setEnv('Trentino//'+gestore)
#url = 'https://www.gruppodolomitienergia.it/content/l-acqua-che-beviamo'
url = 'https://www.gruppodolomitienergia.it/content/mappa-di-trento'
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
marker = 'http://www.gruppodolomitienergia.it/upload/ent3/1/icon_water.png'
locationList = pd.read_csv('Metadata/LocationList.csv')
dataReportCollection = pd.DataFrame()
#
for i,location in locationList.iterrows():
    driver = webdriver.Chrome( "chromedriver", options=options )
    driver.implicitly_wait( 10 )  # seconds
    driver.get( url )
    try:
        alias_city = location['alias_city']
        alias_address = location['alias_address']
        logging.info( 'Processing %s/%s (%s/%s)', alias_city, alias_address, i, len( locationList ) - 1 )
        s = '//div[@title="'+alias_address+'"]'
        #a = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_xpath(s) ) )
        a = driver.find_elements_by_xpath(s)[0]
        driver.execute_script("arguments[0].click();", a)
        time.sleep(2)
        #
        popUp = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_class_name( "myInfoWindow" ) ) )
        d = "Data di prelievo:"
        riferimento_data = popUp.find_elements_by_xpath('//i[contains(text(), "' + d + '")]')[0].text
        data_report = riferimento_data.split(d)[1].strip()
        rawTable = popUp.find_element_by_tag_name( "table" )
        tableHtml = rawTable.get_attribute( 'outerHTML' )
        table = pd.read_html( tableHtml, decimal='.', thousands=',' )[0]
        #closeWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_tag_name( "button" ) ) )
        #driver.execute_script("arguments[0].click();",closeWebElement)
        #
        table.set_index(0,inplace=True)
        parms = table.loc[parametersAdmitted][1]
        stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
        row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        row.update( stdParms )
        dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    except:
        logging.critical('Skip %s/%s',alias_city,alias_address)
    driver.close()
#
dataReportCollection = dataReportCollection.replace('-',np.nan) #Data cleaning
dataReportCollection = dataReportCollection.replace('nan',np.nan)
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)