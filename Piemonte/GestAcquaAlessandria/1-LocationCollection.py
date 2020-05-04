##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "GestAcquaAlessandria"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.gestioneacqua.it/servizi/qualita-dellacqua/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
div = soup.findAll("div", {"class": "elementor-row"})[0]
div = soup.select("section.elementor-element:nth-child(3) > div:nth-child(1) > div:nth-child(1)")[0]
anchors = div.findAll("a")
alias_city = [a.get_text().strip() for a in anchors]
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", AL, Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
