##
from bs4 import BeautifulSoup
import pandas as pd,requests,logging
import acqua.aqueduct as aq
gestore = "AGSRiva"
aq.setEnv('Trentino//'+gestore)
url = 'https://www.altogardaservizi.com/acqua-fognatura/qualita-servizio'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
divAddressList = soup.findAll('div',{'class':'download-box_text'})
##
alias_address = [a.text for a in divAddressList]
locationList = pd.DataFrame({'alias_address':alias_address})
locationList['alias_city'] = 'Riva del Garda'
locationList['georeferencingString'] = locationList['alias_address']+', '+locationList['alias_city']+", TN, Trentino"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
