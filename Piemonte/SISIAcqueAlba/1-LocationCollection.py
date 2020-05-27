##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "SISIAcqueAlba"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.sisiacque.it/?page_id=4117'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
div = soup.find("div", {"id": "main"})
anchors = div.findAll("a")
alias_city = [a.text.replace('Analisi','').strip() for a in anchors if 'Analisi' in a.text]
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", CN, Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
