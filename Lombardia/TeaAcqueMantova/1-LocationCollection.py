##
from bs4 import BeautifulSoup
import pandas as pd,requests,io
import acqua.aqueduct as aq
gestore = "TeaAcqueMantova"
aq.setEnv('Lombardia//'+gestore)
url = 'https://www.cometea.it/verifica-la-tua-acqua/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
map = soup.findAll("area", {"shape": "poly"})
comuniList = [comune['href'].split('/') for comune in list(map)]
alias_city = [comune[len(comune)-1].replace('-',' ') for comune in comuniList]
##
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = 'Comune'
locationList['georeferencingString'] = locationList['alias_city']+", Mantova, Italia"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
