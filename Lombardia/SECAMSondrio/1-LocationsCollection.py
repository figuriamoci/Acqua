##
from bs4 import BeautifulSoup
import requests
import pandas as pd,logging
import acqua.aqueduct as aq
id_gestore = "SECAMSondrio"
aq.setEnv('Lombardia//'+id_gestore)
url = 'http://www.secam.net/2013-05-07-13-46-30/servizio-idrico-integrato/le-analisi-dell-acqua.html'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

tableHtml = soup.find('table')
table = pd.read_html( str(tableHtml))[0]
locationList = table.rename(columns = {0:'alias_city', 1:'alias_address'})

addressList_ = locationList['alias_address'].str.lower()
addressList = addressList_.str.replace('fontana','').str.replace('loc.','località ')#.str.replace('s.','san ')
locationList['georeferencingString'] = addressList.str.strip()+', '+locationList['alias_city']+', Sondrio, Lombardia, Italia'
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
