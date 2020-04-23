##
import pandas as pd, logging
import acqua.aqueduct as aq
aq.setEnv('Lombardia//MM')

def getParameters(address):

    from selenium import webdriver
    from bs4 import BeautifulSoup
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    #%%
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
    logging.info('Access web for %s',address)
    #%%
    listaVie_ = WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_id("lista-vie")))

    primaViaInElenco_ = WebDriverWait(driver, 10).until(EC.visibility_of(listaVie_.find_element_by_id("ui-id-1")))
    primaViaInElenco_ = WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_css_selector("li.ui-menu-item:nth-child(1)")))
    primaViaInElenco = WebDriverWait(driver, 10).until(EC.visibility_of(primaViaInElenco_.find_element_by_xpath(".//a")))
    driver.execute_script("arguments[0].click();", primaViaInElenco)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"select-number")))
    listSelect = driver.find_element_by_id("select-number")
    select = Select( listSelect )
    select.select_by_index(1)

    WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_css_selector("#lista-results > table:nth-child(1)")))
    soup = BeautifulSoup( driver.page_source, 'html.parser' )
    htmlTable = soup.find("div", { "id" : "lista-results" }).find("table")
    df = pd.read_html(str(htmlTable),decimal=',',thousands='.')[0]
    df.set_index('Parametro',inplace=True)

    item = soup.select( "html body.page.page-id-5.page-child.parent-pageid-250.page-template.page-template-acqua_page.page-template-acqua_page-php.custom-background div.wrapper div.article div.content-article p strong" )
    data_report = item[0].get_text()
    driver.close()

    return {'data_report':data_report, 'parameters':df['Campione'].to_dict()}
##
locationList = pd.read_csv('Definitions/LocationList.csv')
reportFoundList = pd.DataFrame()
alias_city = 'Milano'

for i,alias_address in enumerate(locationList['alias_address']):
    logging.info('Extract parameters for %s of %s...',i,len(locationList['alias_address']))
    try:
        parms = getParameters(alias_address)
        report = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': parms['data_report']}
        report.update( parms['parameters'] )
        reportFoundList = reportFoundList.append(report,ignore_index=True)
    except:
        logging.critical('Skip %s',alias_address)
##
reportFoundList.to_csv('Medadata/DataReportCollection.csv',index=False)


