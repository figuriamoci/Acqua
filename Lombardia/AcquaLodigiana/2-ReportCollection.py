##
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd,datetime,os,logging
#os.chdir('D://Python//Acqua')
os.chdir('//Users//andrea//PycharmProjects//Acqua')
os.chdir('Lombardia//AcquaLodigiana')
logging.basicConfig(level=logging.INFO)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(10)
driver.get('http://www.acqualodigiana.it/acqua-del-rubinetto/')
soup = BeautifulSoup(driver.page_source, 'html.parser')
##recupero del periodo di riferimento
premessa = soup.find("div", { "class" : "su-spoiler-content su-u-clearfix su-u-trim" }).get_text().split('.')
semestre = [p for p in premessa if "I valori sono riferiti al" in p]
data_report = semestre[0].strip()
locationList = pd.read_csv('Definitions/LocationList.csv')
reportFoundList = {}
for i,alias in locationList.iterrows():
    alias_city = alias['alias_city']
    alias_address = alias['alias_address']
    alias = (alias_city,alias_address)
    #Find html table refereterd to località
    html_table = soup.find(string=alias_city).findNext("table")
    rowTable = pd.read_html(str(html_table),decimal=',',thousands='.',index_col=0,header=0)[0]
    parameters = rowTable['Valori'].to_dict()
    report = {'data_report':data_report, 'parameters': parameters}
    reportFoundList.update({alias:report})
##
driver.close()
import pickle
f = open("Definitions/ReportListFound.pickle","wb")
pickle.dump(reportFoundList,f)
f.close()
logging.info('Finish: %s',datetime.datetime.now())
