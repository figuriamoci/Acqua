from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd,os,logging,datetime
os.chdir('//Users//andrea//PycharmProjects//Acqua')
#os.chdir('D://Python//Acqua')
os.chdir('Piemonte//SMATTorino')
logging.basicConfig(level=logging.INFO)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.get("https://www.smatorino.it/monitoraggio-acque/")
soup = BeautifulSoup(driver.page_source, 'html.parser')
##recupero del periodo di riferimento
premessa = soup.select(".page-text > h4:nth-child(2)")[0]
data_report = premessa.get_text().replace('CARATTERISTICHE DI QUALITA’ DELLE ACQUE EROGATE NEI COMUNI ATO 3','').replace('(','').replace(')','').strip()
##
soup = BeautifulSoup(driver.page_source, 'html.parser')
htmlTable = soup.find( "table", {"id": "lista-comuni"} )
df = pd.read_html( str( htmlTable ), decimal=',', thousands='.' )[0]
rawReport = df.T.reset_index().set_index('level_0').T.set_index('PARAMETRO')
##
locationList = pd.read_csv('Definitions/LocationList.csv')
locationList.set_index(['alias_city','alias_address'],inplace=True)
reportFoundList = {}
##
for alias in locationList.index:
    alias_city = alias[0]
    try:
        parameters = rawReport.loc[alias_city].to_dict()
        report = {'data_report':data_report,'parameters':parameters}
        reportFoundList.update({alias:report})
        logging.info("Updated reportFoundList for %s",alias)
    except KeyError:
        logging.critical("No label for %s. Skiped!",alias)
##
driver.close()
import pickle
f = open("Definitions/FoundReportList.pickle","wb")
pickle.dump(reportFoundList,f)
f.close()
logging.info('Finish: %s',datetime.datetime.now())

