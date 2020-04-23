#%%
from bs4 import BeautifulSoup,requests
import pandas as pd,datetime,os,logging
os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Veritas')
logging.basicConfig(level=logging.INFO)
url = "https://www.gruppoveritas.it/servizio-idrico-integrato/qualita-dell-acqua.html"
response  = requests.get(url)
htmlPage = response.text
soup = BeautifulSoup(htmlPage,"lxml")
tableHtml = soup.find_all("table",{"class":"table table-hover table-striped sticky-enabled"})[0]
listaComuniHtml = tableHtml.find_all("a")
listaComuni = [c.text.split('-')[-1].strip() for c in listaComuniHtml]
alias_city = {'alias_city':listaComuni}
locationList = pd.DataFrame(alias_city)
locationList['alias_address']='Territorio'
locationList['georeferencingString'] = locationList['alias_city']+', Venezia, Veneto, Italia'
locationList['type']='POINT'
locationList.to_csv('Medadata/LocationList.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
