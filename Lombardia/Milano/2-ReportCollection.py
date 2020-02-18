##
import pandas as pd, datetime, os, logging
os.chdir( '/Users/andrea/PycharmProjects/Acqua/Lombardia/Milano' )

def getParameters(address):

    from selenium import webdriver
    from bs4 import BeautifulSoup
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    #%%
    logging.basicConfig(level=logging.INFO)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("chromedriver", options=options)
    driver.implicitly_wait(10) # seconds
    driver.get("https://www.milanoblu.com/la-tua-acqua/controlla-le-analisi/")
    address = address.lower()

    input = driver.find_element_by_id("tags")

    input.clear()
    input.send_keys(address)
    input.send_keys(Keys.ENTER)
    logging.info('Address: %s',address)
    #%%
    listaVie_ = WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_id("lista-vie")))

    primaViaInElenco_ = WebDriverWait(driver, 10).until(EC.visibility_of(listaVie_.find_element_by_id("ui-id-1")))
    primaViaInElenco_ = WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_css_selector("li.ui-menu-item:nth-child(1)")))
    primaViaInElenco = WebDriverWait(driver, 10).until(EC.visibility_of(primaViaInElenco_.find_element_by_xpath(".//a")))
    driver.execute_script("arguments[0].click();", primaViaInElenco)

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"select-number")))
    listSelect = driver.find_element_by_id("select-number")
    select = Select( listSelect )
    select.select_by_index(1)

    element = WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_css_selector("#lista-results > table:nth-child(1)")))
    soup = BeautifulSoup( driver.page_source, 'html.parser' )
    htmlTable = soup.find("div", { "id" : "lista-results" }).find("table")
    df = pd.read_html(str(htmlTable),decimal=',',thousands='.')[0]
    driver.close()
    return df
##
locationList = pd.read_csv('Definitions/LocationList.csv')
foundReportList = {}
i=0
for address in locationList['alias_address']:
    logging.info("Extract for %s",address)
    i=i+1
    logging.info("Extract for %s (%s)",address,i)
    try:
        report = {address:getParameters(address)}
        foundReportList.update( report )
    except:
        logging.critical('Skip %s',address)

import pickle
f = open("Definitions/FoundReportList.pkl","wb")
pickle.dump(foundReportList,f)
f.close()
##

