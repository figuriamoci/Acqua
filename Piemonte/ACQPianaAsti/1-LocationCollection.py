##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "ACQPianaAsti"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.acquedottopiana.it/l-acqua'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
rows = soup.findAll("span", {"class": "name"})
anchors = [r.find("a") for r in rows]
alias_city = [a.text for a in anchors]
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", AT, Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
