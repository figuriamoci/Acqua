##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "CALSOCuneo"
aq.setEnv('Piemonte//'+gestore)
url = 'https://calso.org/qualita-e-risorse/analisi-delle-acque/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
rows = soup.findAll("a", {"class": "heading-link"})
alias_city = [a.text.strip() for a in rows]
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", CN, Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
