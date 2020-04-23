##
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging,pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
gestore = "UniacqueBergamo"
aq.setEnv('Lombardia//'+gestore)
url = "https://www.uniacque.bg.it/qualita-dellacqua/i-parametri-del-tuo-comune/"
#
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
time.sleep(2)
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
dataReportCollection = pd.DataFrame()
#
selectHtml = WebDriverWait( driver, 10 ).until(EC.presence_of_element_located( (By.NAME, "comuneId") ) )
comuniWebElementList = selectHtml.find_elements_by_tag_name("option")
comuniList = [comune.text for i,comune in enumerate(comuniWebElementList) if i>0]
##
addressList = []
selectComuni = Select(selectHtml)
for i,alias_city in enumerate(comuniList):
    driver.get( url )
    selectComuni = WebDriverWait( driver, 10 ).until(EC.presence_of_element_located( (By.NAME, "comuneId") ) )
    Select(selectComuni).select_by_visible_text(alias_city)
    submit = WebDriverWait( driver, 10 ).until(EC.presence_of_element_located( (By.CSS_SELECTOR, "#page-complete > div > form > input[type=submit]") ) )
    submit.send_keys(Keys.ENTER)
    #
    indirizzoHtml = WebDriverWait( driver, 10 ).until(EC.presence_of_element_located( (By.CSS_SELECTOR, "#page-complete > div > form > label > select") ) )
    indirizziWebElementList = indirizzoHtml.find_elements_by_tag_name("option")
    indirizziList = [indirizzo.text for indirizzo in indirizziWebElementList]
    #
    for j,alias_address in enumerate(indirizziList):
        indirizzoHtml = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#page-complete > div > form > label > select" )))
        Select(indirizzoHtml).select_by_visible_text(alias_address)
        submit = WebDriverWait( driver, 10 ).until(EC.presence_of_element_located( (By.CSS_SELECTOR, "#page-complete > div > form > input[type=submit]") ) )
        submit.send_keys(Keys.ENTER)
        #
        rowTable = driver.find_element_by_css_selector("#page-complete > div > div > table")
        htmlTable = rowTable.get_attribute( 'outerHTML' )
        parametriRaw = (pd.read_html( htmlTable ,thousands='.',decimal=','))[0]
        #
        parametri = parametriRaw[['Parametro', 'Valore rilevato']]
        parametri.set_index( 'Parametro', inplace=True )
        stdParms = parm.standardize( useThisDictionary, parametri['Valore rilevato'].to_dict() )
        #
        premessa = WebDriverWait( driver, 10 ).until(EC.presence_of_element_located( (By.CSS_SELECTOR, "#page-complete > div > div > div > strong:nth-child(1)") ) )
        data_report = premessa.text.split(':')[1].strip()
        #
        row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        row.update( stdParms )
        dataReportCollection = dataReportCollection.append( row, ignore_index=True )
        logging.info("Hacked %s / %s (%s/%s/%s)", alias_city,alias_address,i+1,len(comuniList),len(indirizziList)-j)
        driver.back()
##
driver.close()
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)


