import pandas as pd,os,logging
from bs4 import BeautifulSoup
import requests,re,datetime
os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Veritas')
logging.basicConfig( level=logging.INFO )

url = "https://www.gruppoveritas.it/servizio-idrico-integrato/qualita-dell-acqua.html"
response  = requests.get(url)
htmlPage = response.text
soup = BeautifulSoup(htmlPage,"lxml")
##
premessa = soup.select("#node-80 > h4:nth-child(15) > a:nth-child(1)")[0].get_text()
data_report = premessa.replace("Analisi sull'acqua potabile - valori medi in tutti i Comuni serviti ","").replace('(','').replace(')','')
##
tableHtml = soup.find_all("table",{"class":"table table-hover table-striped sticky-enabled"})[0]
locationList = pd.read_csv('Definitions/LocationList.csv')
reportFoundList = pd.DataFrame()
for i,loc in locationList.iterrows():
    alias_city = loc['alias_city']
    alias_address = loc['alias_address']
    anchor = tableHtml.find_all('a',text=re.compile(alias_city))
    urlReport = anchor[0]['href']
    row = {'alias_city':alias_city, 'alias_address':alias_address,'data_report':data_report, 'url_report':urlReport}
    reportFoundList = reportFoundList.append(row,ignore_index=True)

reportFoundList.to_csv('Definitions/ReportFoundList.csv',index=False)
logging.info( 'Finish: %s', datetime.datetime.now() )