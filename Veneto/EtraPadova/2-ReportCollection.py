##
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import pandas as pd,datetime,logging,time
import acqua.aqueduct as aq,acqua.parametri as parm
from selenium.webdriver.support import expected_conditions as EC
aq.setEnv('Veneto//EtraPadova')
url = 'https://www.etraspa.it/resana/impresa/acqua/analisi-dellacqua'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(40)
parametersAdmitted = parm.getParametersAdmitted('Definitions/SynParametri.csv')
locationList = pd.read_csv('Definitions/LocationList.csv')
##
reportFoundList = pd.DataFrame()
for i,alias_city in locationList.iterrows():
    #i=10
    driver.get(url)
    alias_city = locationList.iloc[i]['alias_city']
    alias_address = locationList.iloc[i]['alias_address']
    #
    selectComuniElement = Select(driver.find_element_by_class_name('form-wrapper').find_element_by_tag_name('select'))
    selectComuniElement.select_by_visible_text(alias_city)
    #
    time.sleep(5)
    WebDriverWait( driver, 40 ).until(EC.presence_of_element_located( (By.CSS_SELECTOR, "#casa > ul > li.first.collapsed.casa-acqua > a")))
    driver.find_element_by_css_selector('#casa > ul > li.first.collapsed.casa-acqua > a').click()
    try:
        time.sleep(5)
        WebDriverWait(driver, 40 ).until(EC.presence_of_element_located( (By.CSS_SELECTOR, "li.leaf:nth-child(4) > a:nth-child(1)")))
        driver.find_element_by_css_selector('li.leaf:nth-child(4) > a:nth-child(1)').click()
        time.sleep(5)
        #
        htmlTable = driver.find_element_by_id('ajax-result').find_element_by_tag_name('table')
        rowTable = htmlTable.get_attribute( 'outerHTML' )
        parametriRaw = (pd.read_html( rowTable, thousands='.', decimal=',',na_values='-' ))[0]
        #
        parIdx = parametriRaw['Parametro'].apply(lambda s: s.split()[0])
        parametri_ = pd.DataFrame(list(parametriRaw['valore']),index=parIdx).dropna()
        parametri = parametri_.reindex(parametersAdmitted)[0]
        data_report = '15/12/2019'
        report = {'alias_city':alias_city, 'alias_address':alias_address, 'data_report':data_report}
        report.update(parametri.to_dict())
        reportFoundList = reportFoundList.append(report,ignore_index=True)
        logging.info('Hacked %s/%s (%s/%s) ...',alias_city,alias_address,i,len(locationList)-1)
    except:
        logging.critical('Skip %s/%s !',alias_city,alias_address)
##
driver.close()
reportFoundList.to_csv('Definitions/ReportFoundList.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
