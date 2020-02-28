##
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd,datetime,os,logging,time
os.chdir('//Users//andrea//PycharmProjects//Acqua')
os.chdir('Piemonte//SMATTorino')
logging.basicConfig(level=logging.INFO)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(10)
driver.get("https://www.smatorino.it/monitoraggio-acque/")
##
soup = BeautifulSoup(driver.page_source, 'html.parser')
data_report_ = soup.find(id="Semestre").findAll("option", {"selected": "selected"})
data_report = data_report_[0].get_text()
##
locationList = pd.read_csv('Definitions/LocationList.csv')
listaComuni = locationList['alias_city']
reportFoundList = {}
#%%
for i,loc in enumerate(listaComuni):
    location =  locationList.iloc[i]
    alias = (location.alias_city,location.alias_address)
    logging.info(">> %s (%s/%s)",alias,i,len(listaComuni))
    select_comuni_ = WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_id("Comune")))
    select_comuni = Select(select_comuni_)
    #select_comuni = Select(driver.find_element_by_id("Comune"))
    select_comuni.select_by_visible_text(location.alias_city)
    time.sleep(2)
    ##
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    htmlTable = soup.find("table", { "id" : "analisi_tables" })
    ##
    tags=htmlTable.findAll('img')
    parametri = [tag['src'].split('/')[-1] for tag in tags]
    ##
    df = pd.read_html(str(htmlTable),decimal=',',thousands='.')[0]
    column = ('U.M.','V.L.')
    df.set_index(column,inplace=True)
    df.columns = parametri
    try:
        parameters = df.loc[location.alias_city].to_dict()
        report = {'data_report':data_report,'parameters':parameters}
        reportFoundList.update({alias:report})
        logging.info("Updated reportFoundList for %s",alias)
    except KeyError:
        logging.critical("No label for %s. Skiped!",alias)
#%%
driver.close()
##
import pickle
f = open("Definitions/FoundReportList.pickle","wb")
pickle.dump(reportFoundList,f)
f.close()
logging.info('Finish: %s',datetime.datetime.now())
