##
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging,pandas as pd
import acqua.aqueduct as aq
import time
site='http://77.242.187.172/itis/cordar/vedi_risultati2N.php?x=13&y=9&IdCertificato_='
gestore = "CordarBiella"
aq.setEnv('Piemonte//'+gestore)
url = 'http://77.242.187.172/itis/cordar/scelta_localitaN.php'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
#
selectAcquedottoWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "Acquedotto" ) ) )
AquedottiListWeElement = selectAcquedottoWebElement.find_elements_by_tag_name('option')
acquedottiList = [a.text for i,a in enumerate(AquedottiListWeElement) if i>0]
alias_city = [a.replace('Acquedotto di','').strip() for a in acquedottiList]
markerSign = 'http://77.242.187.172/itis/cordar/images/marker.png'
driver.close()
reportFoundList = pd.DataFrame()
for i,acquedotto in enumerate(acquedottiList):
    try:
        acquedotto = acquedottiList[i]
        driver = webdriver.Chrome( "chromedriver", options=options )
        driver.implicitly_wait( 10 )  # seconds
        driver.get( url )
        selectAcquedottoWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "Acquedotto" ) ) )
        Select(selectAcquedottoWebElement).select_by_visible_text(acquedotto)
        submitWebElement = driver.find_element_by_name('Submit')
        submitWebElement.click()
        time.sleep(3)
        ##
        div = driver.find_element_by_css_selector('#map > div > div > div:nth-child(1) > div:nth-child(3) > div > div:nth-child(3)')
        imgs = div.find_elements_by_tag_name("img")
        markers = [i for i in imgs if i.get_attribute('src')==markerSign]
        n=len(markers)
        for j in range(0,n,1):
            #j=5
            try:
                dismissButton = driver.find_element_by_class_name( 'dismissButton' )
                driver.execute_script( "arguments[0].click();", dismissButton )
            except:
                pass
            try:
                div = driver.find_element_by_css_selector('#map > div > div > div:nth-child(1) > div:nth-child(3) > div > div:nth-child(3)')
                imgs = div.find_elements_by_tag_name("img")
                markers = [i for i in imgs if i.get_attribute('src')==markerSign]
                time.sleep( 3 )
                driver.execute_script("arguments[0].click();", markers[j])
                time.sleep(1)
                rawTable = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_tag_name( "table" ) ) )
                tableHtml = rawTable.get_attribute('outerHTML')
                tableProperties_ = pd.read_html(tableHtml)[0]
                tableProperties = tableProperties_.T.copy()
                properties = tableProperties.set_index(tableProperties.columns[0]).to_dict()[1]
                alias_address = properties['Punto di prelievo']
                alias_city = acquedotto
                #
                inputWebElement = driver.find_element_by_name('IdCertificato_')
                IdCertificato = inputWebElement.get_attribute('value')
                urlReport = site+IdCertificato
                #
                row = {'alias_city':alias_city,'alias_address':alias_address,'urlReport':urlReport}
                reportFoundList = reportFoundList.append( row, ignore_index=True )
                logging.info('Hacked %s/%s (%s/%s)',alias_city,alias_address,n-j,len(acquedottiList)-i)
            except:
                logging.critical( "Skip for %s", j )
            driver.back()
        driver.close()
    except:
        logging.critical('Skip outer.')
##
reportFoundList.to_csv('Metadata/ReportFoundList.csv',index=False)
