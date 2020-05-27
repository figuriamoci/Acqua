##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "SSISPAVercelli"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.siispa.it/qualita-acqua/laboratorio-analisi/qualita-dell-acqua-fornita'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
div = soup.find("div", {"class": "sppb-article-introtext"})
anchors = div.findAll("a")
alias_city = [a.text.strip() for a in anchors]
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city'].str.replace('V.se','Vercellese')+", Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
